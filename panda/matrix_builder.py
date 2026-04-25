from urllib.parse import quote
from rdflib.namespace import RDF


def clean_uri(uri):
    """
    Normalize URI:
    - convert to string
    - encode unsafe characters
    """
    try:
        uri_str = str(uri)
        return quote(uri_str, safe=":/#?&=%")
    except:
        return None


def build_matrix(graph):
    """
    Build binary matrix:
    rows = subjects
    cols = predicates (+ type + reverse)
    """

    subjects_set = set()
    predicates_set = set()
    cleaned_triples = []

    # =========================
    # STEP 1 — CLEAN TRIPLES
    # =========================
    for s, p, o in graph:

        s_clean = clean_uri(s)
        p_clean = clean_uri(p)

        if s_clean is None or p_clean is None:
            continue

        # =========================
        # TYPE → ::C
        # =========================
        if str(p) == str(RDF.type):

            o_clean = clean_uri(o)
            if o_clean is None:
                continue

            col = f"{o_clean}::C"

            cleaned_triples.append((s_clean, col))
            subjects_set.add(s_clean)
            predicates_set.add(col)

        else:
            # =========================
            # PROPERTY
            # =========================
            col = p_clean

            cleaned_triples.append((s_clean, col))

            subjects_set.add(s_clean)
            predicates_set.add(col)

            # =========================
            # REVERSE PROPERTY → ::R
            # =========================
            o_clean = clean_uri(o)

            if o_clean and o_clean.startswith("http"):
                col_r = f"{p_clean}::R"

                cleaned_triples.append((o_clean, col_r))

                subjects_set.add(o_clean)
                predicates_set.add(col_r)

    # =========================
    # STEP 2 — SORT (IMPORTANT)
    # =========================
    subjects = sorted(list(subjects_set))
    predicates = sorted(list(predicates_set))

    # stable indices
    subj_index = {s: i for i, s in enumerate(subjects)}
    pred_index = {p: i for i, p in enumerate(predicates)}

    # =========================
    # STEP 3 — BUILD MATRIX
    # =========================
    matrix = [
        [0 for _ in range(len(predicates))]
        for _ in range(len(subjects))
    ]

    for s, p in cleaned_triples:
        i = subj_index[s]
        j = pred_index[p]
        matrix[i][j] = 1

    return matrix, subj_index, pred_index