from rdflib import Graph, URIRef, Literal, Namespace
import numpy as np

BC = Namespace("http://example.org/bc#")
RDF_TYPE = URIRef("http://www.w3.org/1999/02/22-rdf-syntax-ns#type")


def build_summary(patterns, predicate_labels):
    """
    Build RDF summary graph from patterns
    """

    g = Graph()
    g.bind("bc", BC)

    pattern_nodes = []

    # =========================
    # STEP 1 — CREATE PATTERN NODES
    # =========================
    for i, p in enumerate(patterns):

        pattern_node = URIRef(f"http://example.org/pattern/{i}")
        pattern_nodes.append(pattern_node)

        subjects = np.flatnonzero(p.transactions)
        extent_value = len(subjects)

        # 🔥 unique extent node per pattern
        extent_node = URIRef(f"http://example.org/pattern/{i}/extent")

       

    # =========================
    # STEP 2 — ADD ITEMS (IMPORTANT)
    # =========================
    for i, p in enumerate(patterns):

        pattern_node = pattern_nodes[i]
        items = np.flatnonzero(p.items)

        for item in items:

            label = predicate_labels[item]

            # -------------------------
            # TYPE (::C)
            # -------------------------
            if label.endswith("::C"):
                uri = label.replace("::C", "")
                g.add((pattern_node, RDF_TYPE, URIRef(uri)))

            # -------------------------
            # REVERSE (::R)
            # -------------------------
            elif label.endswith("::R"):
                base = label.replace("::R", "")

                # connect to another pattern if exists
                for j, p2 in enumerate(patterns):
                    if j != i:
                        items2 = np.flatnonzero(p2.items)
                        labels2 = [predicate_labels[x] for x in items2]

                        if base in labels2:
                            g.add((pattern_node, URIRef(base), pattern_nodes[j]))

            # -------------------------
            # NORMAL PROPERTY
            # -------------------------
            else:
                target_node = URIRef(f"http://example.org/node/{item}")
                g.add((pattern_node, URIRef(label), target_node))

    return g, pattern_nodes