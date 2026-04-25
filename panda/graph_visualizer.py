from pyvis.network import Network
import numpy as np
import math
import os
import webbrowser


def visualize_graph(summary_graph, patterns, predicate_labels, subject_labels, pattern_nodes):

    net = Network(height="800px", width="100%", directed=True)

    added_nodes = set()

    # =========================
    # STEP 1 — DETECT CLASS NODES
    # =========================
    class_nodes = set()

    for s, p, o in summary_graph:
        if "type" in str(p):
            class_nodes.add(str(o))

    # =========================
    # STEP 2 — ADD NODES
    # =========================
    for s, p, o in summary_graph:

        for node in [s, o]:

            node_str = str(node)

            if node_str in added_nodes:
                continue

            label = node_str.split("/")[-1]

            # -------------------------
            # PATTERN NODE (SIZE = EXTENT)
            # -------------------------
            if "pattern/" in node_str:

                idx = int(node_str.split("/")[-1])
                subjects = np.flatnonzero(patterns[idx].transactions)

                size = int(10 + min(40, math.log(len(subjects) + 1) * 5))

                net.add_node(
                    node_str,
                    label=f"P{idx+1}",
                    title=f"Subjects: {len(subjects)}",
                    color="red",
                    size=size
                )

            # -------------------------
            # CLASS NODE
            # -------------------------
            elif node_str in class_nodes:

                net.add_node(
                    node_str,
                    label=label,
                    color="purple",
                    size=30
                )

            # -------------------------
            # OTHER NODE
            # -------------------------
            else:
                net.add_node(
                    node_str,
                    label=label,
                    color="blue",
                    size=10
                )

            added_nodes.add(node_str)

    # =========================
    # STEP 3 — ADD EDGES
    # =========================
    for s, p, o in summary_graph:

        s_str = str(s)
        o_str = str(o)
        p_label = str(p).split("/")[-1]

        net.add_edge(s_str, o_str, label=p_label)

    # =========================
    # STEP 4 — SAVE + OPEN
    # =========================
    os.makedirs("output", exist_ok=True)

    path = "output/graph.html"
    net.save_graph(path)

    webbrowser.open("graph.html")