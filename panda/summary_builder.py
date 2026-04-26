from rdflib import Graph, URIRef, Literal, Namespace
import numpy as np

BC = Namespace("http://example.org/bc#")
RDF_TYPE = URIRef("http://www.w3.org/1999/02/22-rdf-syntax-ns#type")


def clean_label(label):
    label = str(label)

    for sep in ['#', '/', ':']:
        if sep in label:
            label = label.split(sep)[-1]

    return label.strip()


def build_summary(patterns, predicate_labels):

    g = Graph()
    g.bind("bc", BC)

    pattern_nodes = []

    # =========================
    # STEP 1 — CREATE PATTERN NODES
    # =========================
    for i, p in enumerate(patterns):

        pattern_node = URIRef(f"http://example.org/pattern{i}")
        pattern_nodes.append(pattern_node)

        subjects = np.flatnonzero(p.transactions)
        extent_value = len(subjects)

        # ✔ Add extent
        g.add((pattern_node, BC.extent, Literal(extent_value)))

    # =========================
    # STEP 2 — ADD ITEMS
    # =========================
    for i, p in enumerate(patterns):

        pattern_node = pattern_nodes[i]
        items = np.flatnonzero(p.items)

        for item in items:

            raw_label = predicate_labels[item]

            # -------------------------
            # TYPE (::C)
            # -------------------------
            if str(raw_label).endswith("::C"):
                uri = str(raw_label).replace("::C", "")
                g.add((pattern_node, RDF_TYPE, URIRef(uri)))

            # -------------------------
            # REVERSE (::R)
            # -------------------------
            elif str(raw_label).endswith("::R"):
                base = str(raw_label).replace("::R", "")

                for j, p2 in enumerate(patterns):
                    if j == i:
                        continue

                    items2 = np.flatnonzero(p2.items)

                    for it2 in items2:
                        if str(predicate_labels[it2]) == base:
                            g.add((pattern_node, URIRef(base), pattern_nodes[j]))

            # -------------------------
            # NORMAL PROPERTY
            # -------------------------
            else:
                target_node = URIRef(f"http://example.org/node/{item}")
                g.add((pattern_node, URIRef(raw_label), target_node))

    return g, pattern_nodes