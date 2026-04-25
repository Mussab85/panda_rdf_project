# 🧠 PaNDa+ RDF Summary Generator

This project implements **RDF graph summarization** using the **PaNDa+ algorithm**, transforming RDF datasets into compact, interpretable summaries through approximate pattern mining.

---

## 📌 Overview

The pipeline follows three main steps:

1. **Binary Matrix Mapping**
   RDF graph → binary matrix (subjects × predicates)

2. **Pattern Mining (PaNDa+)**
   Extract top-k approximate patterns describing the dataset

3. **Summary Graph Construction**
   Build a compact RDF summary graph and visualize it

---

## 🧩 Architecture

### 🔹 Pipeline Overview

![Pipeline](docs/pipeline.png)

---

## 📊 Example Visualization

### 🔹 RDF Summary Graph

![Graph](docs/graph.png)

---

## 🚀 Features

* RDF → Binary matrix transformation
* Support for:

  * Types (`::C`)
  * Properties
  * Reverse properties (`::R`)
* Approximate Top-K pattern mining
* Pattern size encoded as node size
* Interactive graph visualization (PyVis)

---

## 🛠️ Tech Stack

* Python
* NumPy
* rdflib
* Streamlit
* PyVis

---

## 📦 Installation

```bash
pip install -r requirements.txt
```

---

## ▶️ Run the Application

```bash
python -m streamlit run app.py
```

---

## 📁 Project Structure

```
panda_rdf_project/
│
├── app.py
├── README.md
├── requirements.txt
├── .gitignore
│
├── panda/
│   ├── __init__.py
│   ├── rdf_loader.py
│   ├── matrix_builder.py
│   ├── panda_topk.py
│   ├── summary_builder.py
│   └── graph_visualizer.py
│
├── data/
├── output/
└── docs/
    ├── pipeline.png
    └── graph.png
```

---

## 🧠 Pattern Representation

Each pattern consists of:

* **Items** → predicates (columns)
* **Transactions** → subjects (rows)

Pattern size is visualized using node size.

---

## 🎨 Visualization

* 🔴 Red nodes → Patterns
* 🟣 Purple nodes → Classes (`rdf:type`)
* 🔵 Blue nodes → Other entities
* Node size → number of subjects

---

## 📌 Notes

* This implementation follows a simplified version of the PaNDa+ algorithm
* Designed for experimentation and visualization
* Works without schema information

---

## 📚 Reference

Summarizing linked data RDF graphs using approximate graph pattern mining
Authors
Mussab Zneika, Claudio Lucchese, Dan Vodislav, Dimitris Kotzinos
---

## 👨‍💻 Author

Mussab Zneika

---

## ⭐ If you like this project

Give it a star on GitHub ⭐
