import numpy as np

from panda.rdf_loader import load_rdf
from panda.matrix_builder import build_matrix
from panda.panda_plus_advanced import run_panda_plus_exact
from panda.summary_builder import build_summary
from panda.export_utils import save_all


# =========================
# CONFIG (editable)
# =========================
INPUT_FILE = "Data/example.rdf"

K = 20
EPS_R = 0.5
EPS_C = 0.5
LAMBDA = 1.0
MIN_SIZE = 50


def main():
    print("📥 Loading RDF...")
    graph = load_rdf(INPUT_FILE)

    print("🔧 Building matrix...")
    matrix, subj_map, pred_map = build_matrix(graph)
    data = np.array(matrix, dtype=bool)

    print("🚀 Running PANDA+...")
    patterns, _ = run_panda_plus_exact(
        K,
        data,
        epsilon_r=EPS_R,
        epsilon_c=EPS_C,
        lambda_=LAMBDA
    )

    # Filter
    patterns = [
        p for p in patterns
        if np.sum(p.transactions) >= MIN_SIZE
    ]

    print(f"✔ Found {len(patterns)} patterns")

    predicate_labels = {i: p for p, i in pred_map.items()}
    subject_labels = {i: s for s, i in subj_map.items()}

    # Save outputs
    save_all(patterns, predicate_labels, subject_labels)

    print("🧠 Building RDF summary...")
    summary_graph, _ = build_summary(patterns, predicate_labels)
    summary_graph.serialize("output/summary.ttl", format="turtle")

    print("✅ Done. Check /output folder")


if __name__ == "__main__":
    main()