
import streamlit as st
import numpy as np
import pandas as pd
from streamlit.components.v1 import html

from panda.rdf_loader import load_rdf
from panda.matrix_builder import build_matrix
from panda.panda_plus_advanced import run_panda_plus_exact
from panda.export_utils import save_all
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
k = st.sidebar.number_input("Top-K", 1, 500, 20)

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

        st.write("DEBUG patterns:", len(patterns))

        predicate_labels = {i: p for p, i in pred_map.items()}
        subject_labels = {i: s for s, i in subj_map.items()}

        # =========================
        # SAVE OUTPUT FILES
        # =========================
        save_all(patterns, predicate_labels, subject_labels)

        # =========================
        # BUILD RDF SUMMARY
        # =========================
        summary_graph, pattern_nodes = build_summary(patterns, predicate_labels)
        summary_graph.serialize("output/summary.ttl", format="turtle")

        # =========================
        # METRICS
        # =========================
        total_patterns = len(patterns)
        total_subjects = len(subject_labels)
        total_predicates = len(predicate_labels)
        total_cells = int(np.sum(data))  # number of TRUE cells

        col1, col2, col3, col4 = st.columns(4)

        col1.metric("Patterns", total_patterns)
        col2.metric("Subjects", total_subjects)
        col3.metric("Predicates", total_predicates)
        col4.metric("True Cells (1s)", total_cells)

        # =========================
        # TABS
        # =========================
        tab_graph, tab_table, tab_insights, tab_debug = st.tabs([
            "🌐 RDF Graph",
            "📊 Patterns Table",
            "📈 Insights",
            "🧪 Debug"
        ])

        # -------------------------
        # GRAPH TAB
        # -------------------------
        with tab_graph:

            visualize_rdf_graph(summary_graph)

            with open("output/rdf_graph.html", "r", encoding="utf-8") as f:
                html(f.read(), height=750, scrolling=True)

        # -------------------------
        # TABLE TAB
        # -------------------------
        with tab_table:

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
            st.dataframe(df, width="stretch")

        # -------------------------
        # INSIGHTS TAB (CORRECTED ✔)
        # -------------------------
        with tab_insights:

            st.subheader("📈 Pattern Insights")

            if len(patterns) == 0:
                st.warning("No patterns found — cannot compute insights.")
            else:

                # =========================
                # SIZE DISTRIBUTION
                # =========================
                sizes = [np.sum(p.transactions) for p in patterns]
                st.markdown("### Pattern Size Distribution")
                st.bar_chart(sizes)

                items = [np.sum(p.items) for p in patterns]
                st.markdown("### Items per Pattern")
                st.bar_chart(items)

                # =========================
                # COVERAGE (REAL DATA ✔)
                # =========================
                covered_matrix = np.zeros_like(data, dtype=bool)

                for p in patterns:
                    rows = np.where(p.transactions)[0]
                    cols = np.where(p.items)[0]
                    covered_matrix[np.ix_(rows, cols)] = True

                true_cells = np.sum(data)
                covered_true = np.sum(covered_matrix & data)

                true_coverage = covered_true / true_cells if true_cells else 0

                st.markdown("### Coverage (Real Data)")
                st.progress(min(true_coverage, 1.0))
                st.write(f"{true_coverage:.2%} of actual data covered")
                
                
                tp = np.sum(covered_matrix & data)
                # False positives (covered but not real)
                fp = np.sum(covered_matrix & ~data)
                # False negatives (real but not covered)
                fn = np.sum(data & ~covered_matrix)
                # -------------------------
                # # Noise (FP relative to predicted)
                # # -------------------------
                predicted = tp + fp
                noise_ratio = fp / predicted if predicted else 0
                # -------------------------
                # # Precision (cleanliness)
                # # -------------------------
                precision = tp / predicted if predicted else 0
                # -------------------------
                # # Recall (coverage of real data)
                # # -------------------------
                total_real = np.sum(data)
                recall = tp / total_real if total_real else 0
                # -------------------------# F1 Score (balance)
                # -------------------------
                f1 = 2 * precision * recall / (precision + recall) if (precision + recall) else 0

                # =========================
                   # DISPLAY
                # =========================

                st.markdown("### Quality Metrics")
                st.write(f"Precision: {precision:.2%}")
                st.write(f"Recall (Coverage): {recall:.2%}")
                st.write(f"F1 Score: {f1:.2%}")
               
               
                # =========================
                # TOP PREDICATES
                # =========================
                pred_count = {}

                for p in patterns:
                    cols = np.where(p.items)[0]
                    for c in cols:
                        label = str(predicate_labels[c])
                        pred_count[label] = pred_count.get(label, 0) + 1

                top_preds = sorted(pred_count.items(), key=lambda x: -x[1])[:10]
                df_preds = pd.DataFrame(top_preds, columns=["Predicate", "Frequency"])

                st.markdown("### Top Predicates")
                st.dataframe(df_preds, width="stretch")

                # =========================
                # PATTERN PREVIEW (WITH SLIDER ✔)
                # =========================
                max_show = st.slider("Number of patterns to display", 1, len(patterns), 5)

                st.markdown("### Patterns Preview")

                for i, p in enumerate(patterns[:max_show]):
                    rows = np.sum(p.transactions)
                    cols = np.sum(p.items)
                    st.write(f"Pattern {i}: {rows} subjects × {cols} items")

        # -------------------------
        # DEBUG TAB
        # -------------------------
        with tab_debug:

            st.subheader("Execution Logs")

            for line in logs:
                st.text(line)

