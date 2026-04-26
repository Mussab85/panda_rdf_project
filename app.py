
import streamlit as st
import numpy as np
import pandas as pd

# ✅ NEW import (no deprecation)
from streamlit.components.v1 import html

from panda.rdf_loader import load_rdf
from panda.matrix_builder import build_matrix
from panda.panda_plus_advanced import run_panda_plus_exact
from panda.export_utils import save_all

# RDF pipeline
from panda.summary_builder import build_summary
from panda.graph_visualizer import visualize_rdf_graph


# =========================
# PAGE CONFIG
# =========================
st.set_page_config(page_title="PaNDa+ RDF Dashboard", layout="wide")

# =========================
# HEADER
# =========================
st.title("🐼 PaNDa+ RDF Dashboard")
st.markdown(
    "Interactive tool for **RDF graph summarization** using the **PaNDa+ algorithm**."
)

# =========================
# SIDEBAR
# =========================
st.sidebar.header("⚙️ Parameters")

lambda_val = st.sidebar.slider("Lambda", 0.0, 5.0, 1.0)
epsilon_r = st.sidebar.slider("Row Noise εr", 0.0, 1.0, 0.5)
epsilon_c = st.sidebar.slider("Column Noise εc", 0.0, 1.0, 0.5)
k = st.sidebar.number_input("Top-K", 1, 100, 20)

min_size = st.sidebar.slider("Min Pattern Size", 0, 2000, 50)

uploaded_file = st.file_uploader("📂 Upload RDF file")

# =========================
# MAIN
# =========================
if uploaded_file:

    with open("temp.rdf", "wb") as f:
        f.write(uploaded_file.read())

    if st.button("🚀 Run PANDA+"):

        with st.spinner("Processing RDF and extracting patterns..."):

            graph = load_rdf("temp.rdf")
            matrix, subj_map, pred_map = build_matrix(graph)

            data = np.array(matrix, dtype=bool)

            patterns, logs = run_panda_plus_exact(
                k,
                data,
                epsilon_r=epsilon_r,
                epsilon_c=epsilon_c,
                lambda_=lambda_val
            )

        # =========================
        # FILTER
        # =========================
        patterns = [
            p for p in patterns
            if np.sum(p.transactions) >= min_size
        ]

        predicate_labels = {i: p for p, i in pred_map.items()}
        subject_labels = {i: s for s, i in subj_map.items()}

        # =========================
        # SAVE FILES ✔
        # =========================
        save_all(patterns, predicate_labels, subject_labels)

        # =========================
        # BUILD RDF SUMMARY ✔
        # =========================
        summary_graph, pattern_nodes = build_summary(patterns, predicate_labels)

        # save RDF
        summary_graph.serialize("output/summary.ttl", format="turtle")

        # =========================
        # METRICS
        # =========================
        total_patterns = len(patterns)
        total_subjects = len(subject_labels)
        total_predicates = len(predicate_labels)
        total_cells = int(np.sum(data))

        col1, col2, col3, col4 = st.columns(4)

        col1.metric("Patterns", total_patterns)
        col2.metric("Subjects", total_subjects)
        col3.metric("Predicates", total_predicates)
        col4.metric("Data Size (1s)", total_cells)

        # =========================
        # TABS
        # =========================
        tab1, tab2, tab3 = st.tabs(["🌐 RDF Graph", "📊 Patterns Table", "🧪 Debug"])

        # -------------------------
        # GRAPH TAB ✔ (UPDATED)
        # -------------------------
        with tab1:

            visualize_rdf_graph(summary_graph)

            with open("output/rdf_graph.html", "r", encoding="utf-8") as f:
                html(f.read(), height=750, scrolling=True)

        # -------------------------
        # TABLE TAB ✔ (UPDATED)
        # -------------------------
        with tab2:

            table_data = []

            for i, p in enumerate(patterns):
                rows = np.where(p.transactions)[0]
                cols = np.where(p.items)[0]

                table_data.append({
                    "Pattern": i,
                    "Subjects": len(rows),
                    "Items": len(cols),
                    "Predicates": ", ".join(
                        [str(predicate_labels[c]) for c in cols[:5]]
                    )
                })

            df = pd.DataFrame(table_data)

            # ✅ FIXED (no warning)
            st.dataframe(df, width="stretch")

        # -------------------------
        # DEBUG TAB ✔
        # -------------------------
        with tab3:

            st.subheader("Execution Logs")

            for line in logs:
                st.text(line)
