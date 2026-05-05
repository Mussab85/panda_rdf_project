# 🐼 PaNDa+ RDF Pattern Mining Dashboard

A **Streamlit-based implementation** of the **PaNDa+ algorithm** for
**approximate mining of top-K patterns from RDF data**, including
**RDF summarization, visualization, and quality analysis**.

---

## 📄 Related Publication

This project is based on our published research:

👉 https://hal.science/hal-01418255/document

---

## 📌 Overview

This project implements a **research-oriented adaptation of PaNDa+ for RDF graphs**.

It allows you to:

* Load RDF data (`.rdf`)
* Transform RDF into a **binary matrix representation**
* Extract **top-K approximate patterns**
* Build a **compact RDF summary graph**
* Visualize patterns interactively
* Analyze results using **coverage and quality metrics**
* Export all outputs (patterns, mappings, RDF summary)

---

## 🖼️ Pipeline

<p align="center">
  <img src="docs/pipeline.png" width="700">
</p>

---

## 🧠 How It Works

### 1. RDF Input

The system takes RDF triples:

```text
(subject, predicate, object)
```

---

### 2. Matrix Construction

The RDF graph is converted into a **binary matrix**:

* Rows → Subjects
* Columns → Predicates
* Value = 1 → subject has that predicate

---

### 3. Pattern Mining (PaNDa+)

The algorithm extracts **top-K approximate patterns**:

* Each pattern = subset of subjects + subset of predicates
* Allows **controlled noise (εr, εc)**
* Uses a **residual matrix (DR)**
* Optimizes an **XOR-based cost function**

---

### 4. RDF Summary

Patterns are transformed into a **semantic RDF summary graph**:

* Pattern → node
* Predicate → edge
* `rdf:type` → class nodes
* Pattern relationships are preserved

---

### 5. Visualization & Analysis

The system provides:

* Interactive graph visualization (PyVis)
* Pattern statistics and insights
* Quality metrics (precision, recall, noise)

---

## 🚀 How to Run

### 1. Clone the repository

```bash
git clone https://github.com/Mussab85/panda_rdf_project.git
cd panda_rdf_project
```

---

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

---

### 3. Run the application

```bash
streamlit run app.py
```

---

### 4. Use the app

* Upload an RDF file (`.rdf`)
* Adjust parameters in the sidebar
* Click **Run PANDA+**

You will see:

* Extracted patterns
* RDF graph visualization
* Insights (coverage, precision, etc.)
* Debug logs

---

## ⚙️ Parameters

All parameters are controlled from the **Streamlit sidebar**.

---

### 🔹 `k` — Top-K Patterns

Maximum number of patterns to extract
**Default:** `20`

---

### 🔹 `epsilon_r (εr)` — Row Noise

Controls tolerance for incorrect subjects in patterns

* Lower → stricter patterns
* Higher → more flexible

**Range:** `0.0 – 1.0`
**Default:** `0.5`

---

### 🔹 `epsilon_c (εc)` — Column Noise

Controls tolerance for missing/spurious predicates

* Lower → strict patterns
* Higher → more variation

**Range:** `0.0 – 1.0`
**Default:** `0.5`

---

### 🔹 `lambda` — Complexity Penalty

Balances pattern size vs noise
**Default:** `1.0`

---

### 🔹 `min_size`

Minimum number of subjects per pattern
**Default:** `50`

---

## 📈 Visualization

The graph shows:

* 🔵 Pattern nodes
* 🟠 Class nodes (`rdf:type`)
* 🟢 Entity nodes
* Edges = RDF predicates

Node size reflects **pattern extent (number of subjects)**.

---

## 🌐 Graph Example

<p align="center">
  <img src="docs/graph.png" width="800">
</p>

---

## 📊 Output Files

After running, results are saved in `/output`:

* `patterns.txt` → pattern definitions
* `subjects.txt` → subject mapping
* `properties.txt` → predicate mapping
* `summary.ttl` → RDF summary graph
* `rdf_graph.html` → interactive visualization

---

## 📈 Quality Metrics

The system evaluates pattern quality using:

* **Recall (Coverage)** → how much real RDF data is explained
* **Precision** → how accurate patterns are
* **F1 Score** → balance between precision and recall
* **Noise** → proportion of false positives

⚠️ Coverage is computed on **real RDF facts (1s only)**, not the full matrix.

---

## 🧪 Example Dataset

Generate a dataset with 1000+ triples:

```bash
python scripts/generate_rdf.py
```

---

## 🧪 Example Workflow

1. Upload RDF dataset
2. Run with default parameters
3. Inspect extracted patterns
4. Adjust εr / εc
5. Analyze metrics (precision / recall)
6. Export results

---

## ⚠️ Notes

* Patterns may **share subjects (overlap is allowed)**
* Each matrix cell is covered at most once in residual updates
* Results depend strongly on parameter tuning
* Large datasets may require more computation time

---

## 📚 References

### 🔹 RDF Graph Summarization

**Mussab Zneika**, Claudio Lucchese, Dan Vodislav, Dimitris Kotzinos
*RDF Graph Summarization Based on Approximate Patterns*
ISIP 2015, Springer

🔗 https://hal.science/hal-01418255/document

---

### 🔹 PaNDa+ Algorithm

Lucchese, Orlando, Perego
*A Unifying Framework for Mining Approximate Top-K Binary Patterns*
IEEE TKDE, 2014

---

## 📖 Citation

```bibtex
@inproceedings{zneika2015rdf,
  author    = {Zneika, Mussab and Lucchese, Claudio and Vodislav, Dan and Kotzinos, Dimitris},
  title     = {RDF Graph Summarization Based on Approximate Patterns},
  booktitle = {International Workshop on Information Search, Integration, and Personalization},
  pages     = {69--87},
  year      = {2015},
  publisher = {Springer, Cham},
  url       = {https://hal.science/hal-01418255/document}
}
```

---

## 👨‍💻 Author

**Mussab Zneika**

---

## ⭐ License

This project is intended for **academic and research purposes**.
