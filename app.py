# Main Streamlit App
import streamlit as st
import numpy as np

from panda.rdf_loader import load_rdf
from panda.matrix_builder import build_matrix
from panda.panda_topk import run_panda_plus_fast
from panda.summary_builder import build_summary
from panda.graph_visualizer import visualize_graph

st.set_page_config(page_title="PaNDa+ RDF Dashboard", layout="wide")
st.title("PaNDa+ RDF Summary Generator")

lambda_val = st.sidebar.slider("Lambda", 0.0, 1.0, 0.4)
epsilon_r = st.sidebar.slider("Epsilon Rows", 0.0, 1.0, 0.2)
k = st.sidebar.number_input("Top-K patterns", 1, 500, 20)

uploaded_file = st.file_uploader("Upload RDF file")

if uploaded_file:
    with open("temp.rdf", "wb") as f:
        f.write(uploaded_file.read())

    if st.button("Run"):
        graph = load_rdf("temp.rdf")
        matrix, subj_map, pred_map = build_matrix(graph)
        data = np.array(matrix, dtype=bool)

        patterns = run_panda_plus_fast(k, data, epsilon_r, lambda_val)

        predicate_labels = {i: p for p, i in pred_map.items()}
        subject_labels = {i: s for s, i in subj_map.items()}

        summary_graph, pattern_nodes = build_summary(patterns, predicate_labels)

        visualize_graph(summary_graph, patterns, predicate_labels, subject_labels, pattern_nodes)
