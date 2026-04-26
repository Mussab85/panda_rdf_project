import os
import numpy as np


# =========================
# SAVE SUBJECT TABLE
# =========================
def save_subjects(subject_labels, path):
    with open(path, "w", encoding="utf-8") as f:
        for i in sorted(subject_labels):
            f.write(f"{i} {subject_labels[i]}\n")


# =========================
# SAVE PREDICATE TABLE
# =========================
def save_predicates(predicate_labels, path):
    with open(path, "w", encoding="utf-8") as f:
        for i in sorted(predicate_labels):
            f.write(f"{i} {predicate_labels[i]}\n")


# =========================
# SAVE PATTERNS (FINAL FORMAT)
# =========================
def save_patterns(patterns, path):
    import numpy as np

    with open(path, "w", encoding="utf-8") as f:

        for idx, p in enumerate(patterns, start=1):

            # 🔥 SAME as graph builder
            items = np.flatnonzero(p.items)
            subjects = np.flatnonzero(p.transactions)

            items = sorted(items)
            subjects = sorted(subjects)

            line = f"{idx} "
            line += " ".join(map(str, items))
            line += f" ({len(subjects)}) "
            line += " ".join(map(str, subjects))

            f.write(line + "\n")

# =========================
# SAVE EVERYTHING
# =========================
def save_all(patterns, predicate_labels, subject_labels, output_dir="output"):

    os.makedirs(output_dir, exist_ok=True)

    save_patterns(patterns, f"{output_dir}/patterns.txt")
    save_predicates(predicate_labels, f"{output_dir}/predicates.txt")
    save_subjects(subject_labels, f"{output_dir}/subjects.txt")

    print("✅ Results saved in /output/")