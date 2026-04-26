import streamlit as st
import numpy as np

from panda.rdf_loader import load_rdf
from panda.matrix_builder import build_matrix
from panda.panda_plus_advanced import run_panda_plus_exact
from panda.summary_builder import build_summary
from panda.graph_visualizer import visualize_graph
from panda.export_utils import save_all

st.set_page_config(page_title="PaNDa+ RDF", layout="wide")
st.title("PaNDa+ RDF Summary Generator")

# =========================
# PARAMETERS (USER CONTROL)
# =========================
st.sidebar.header("Parameters")

lambda_val = st.sidebar.slider("Lambda", 0.0, 5.0, 1.0, 0.1)
epsilon_r = st.sidebar.slider("Row Noise εr", 0.0, 1.0, 0.5, 0.05)
epsilon_c = st.sidebar.slider("Column Noise εc", 0.0, 1.0, 0.5, 0.05)
k = st.sidebar.number_input("Top-K", 1, 100, 20)

# show parameters
st.sidebar.write("### Current values")
st.sidebar.write({
    "lambda": lambda_val,
    "epsilon_r": epsilon_r,
    "epsilon_c": epsilon_c,
    "k": k
})

uploaded_file = st.file_uploader("Upload RDF")

if uploaded_file:
    with open("temp.rdf", "wb") as f:
        f.write(uploaded_file.read())

    if st.button("Run PANDA+"):

        graph = load_rdf("temp.rdf")

        matrix, subj_map, pred_map = build_matrix(graph)
        data = np.array(matrix, dtype=bool)
        patterns, logs = run_panda_plus_exact(k, data, epsilon_r, epsilon_c)

        st.success(f"Patterns found: {len(patterns)}")

        # =========================
        # DEBUG LOGS
        # =========================
        with st.expander("Debug Execution"):
            for line in logs:
                st.text(line)

        predicate_labels = {i: p for p, i in pred_map.items()}
        subject_labels = {i: s for s, i in subj_map.items()}

        save_all(patterns, predicate_labels, subject_labels)

        summary_graph, pattern_nodes = build_summary(patterns, predicate_labels)

        visualize_graph(
            summary_graph,
            patterns,
            predicate_labels,
            subject_labels,
            pattern_nodes
        )