from pyvis.network import Network
import math


def clean(uri):
    uri = str(uri)
    for sep in ['#', '/', ':']:
        if sep in uri:
            uri = uri.split(sep)[-1]
    return uri


def visualize_rdf_graph(g):

    net = Network(
        height="750px",
        width="100%",
        bgcolor="#f5f7fa",
        font_color="#222222"
    )

    # =========================
    # PRECOMPUTE DEGREE
    # =========================
    node_sizes = {}

    for s, p, o in g:
        node_sizes[str(s)] = node_sizes.get(str(s), 0) + 1
        node_sizes[str(o)] = node_sizes.get(str(o), 0) + 1

    # =========================
    # ADD NODES (FORCE LABELS)
    # =========================
    added = set()

    for s, p, o in g:

        for node in [s, o]:

            node_str = str(node)

            if node_str in added:
                continue

            added.add(node_str)

            label = clean(node_str)
            size = 15 + 8 * math.log1p(node_sizes[node_str])

            color = "#4e79a7" if "pattern" in node_str else "#59a14f"

            net.add_node(
                node_str,
                label=label,
                title=label,
                size=size,
                color=color,
                font={
                    "size": 18,
                    "color": "#222222",
                    "face": "arial"
                }
            )

    # =========================
    # ADD EDGES (LABEL ON HOVER ✔)
    # =========================
    for s, p, o in g:

        net.add_edge(
            str(s),
            str(o),
            title=clean(p),   # 👈 SHOW ON HOVER (better than inline)
            color="#999999",
            width=2
        )

    # =========================
    # OPTIONS (KEY FIX)
    # =========================
    net.set_options("""
    var options = {
      "nodes": {
        "font": {
          "size": 18,
          "color": "#222222",
          "face": "arial"
        }
      },
      "edges": {
        "font": {
          "size": 14,
          "align": "middle"
        }
      },
      "physics": {
        "barnesHut": {
          "gravitationalConstant": -3000,
          "centralGravity": 0.1,
          "springLength": 200,
          "springConstant": 0.02,
          "damping": 0.2
        }
      },
      "interaction": {
        "hover": true,
        "tooltipDelay": 100,
        "navigationButtons": true
      }
    }
    """)

    net.save_graph("output/rdf_graph.html")