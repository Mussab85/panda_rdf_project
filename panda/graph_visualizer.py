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
        bgcolor="#eef2f7",   # light modern background
        font_color="#222222"
    )

    # =========================
    # DETECT NODE TYPES
    # =========================
    class_nodes = set()
    pattern_nodes = set()

    for s, p, o in g:
        if "pattern" in str(s):
            pattern_nodes.add(str(s))
        if str(p).endswith("type"):
            class_nodes.add(str(o))

    # =========================
    # DEGREE (for size)
    # =========================
    node_sizes = {}

    for s, p, o in g:
        node_sizes[str(s)] = node_sizes.get(str(s), 0) + 1
        node_sizes[str(o)] = node_sizes.get(str(o), 0) + 1

    # =========================
    # ADD NODES
    # =========================
    added = set()

    for s, p, o in g:
        for node in [s, o]:

            node_str = str(node)

            if node_str in added:
                continue

            added.add(node_str)

            label = clean(node_str)

            # smart size scaling
            size = 25 + 15 * math.log1p(node_sizes[node_str])

            # 🎨 COLORS
            if node_str in pattern_nodes:
                color = "#4e79a7"   # 🔵 pattern
                node_type = "Pattern"
            elif node_str in class_nodes:
                color = "#f28e2b"   # 🟠 class
                node_type = "Class"
            else:
                color = "#59a14f"   # 🟢 normal
                node_type = "Node"

            # 🔥 rich hover (acts like "click info")
            title = f"""
            {label}
            Type: {node_type}
            Connections: {node_sizes[node_str]}
            """

            net.add_node(
                node_str,
                label=label,
                title=title,
                size=size,
                color=color,
                font={"size": 18}
            )

    # =========================
    # ADD EDGES
    # =========================
    for s, p, o in g:

        net.add_edge(
            str(s),
            str(o),
            title=clean(p),   # hover label
            color="#888888",
            width=2
        )

    # =========================
    # OPTIONS (layout + labels)
    # =========================
    net.set_options("""
    var options = {
      "nodes": {
        "shape": "dot",
        "font": {
          "size": 18,
          "color": "#222222"
        }
      },
      "edges": {
        "font": {
          "size": 14,
          "align": "middle"
        },
        "smooth": {
          "type": "dynamic"
        }
      },
      "physics": {
        "barnesHut": {
          "gravitationalConstant": -3500,
          "centralGravity": 0.2,
          "springLength": 180,
          "springConstant": 0.03,
          "damping": 0.15
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