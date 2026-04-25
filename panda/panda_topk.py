import numpy as np


# ===============================
# PATTERN CLASS
# ===============================
class Pattern:
    def __init__(self, items, transactions):
        self.items = items
        self.transactions = transactions


# ===============================
# MDL-LIKE COST FUNCTION
# ===============================
def compute_cost(patterns, data, lambda_):
    covered = np.zeros_like(data, dtype=bool)

    for p in patterns:
        covered[p.transactions] |= p.items

    noise = np.sum(covered ^ data)

    # 🔥 MDL-inspired cost (log encoding)
    pattern_cost = sum(
        np.log2(1 + np.sum(p.items)) +
        np.log2(1 + np.sum(p.transactions))
        for p in patterns
    )

    return noise + lambda_ * pattern_cost


# ===============================
# PAIR-BASED ORDERING (CHARM-like)
# ===============================
def compute_pair_scores(data):
    n_items = data.shape[1]
    scores = np.zeros(n_items)

    for i in range(n_items):
        for j in range(i + 1, n_items):
            cooccur = np.sum(data[:, i] & data[:, j])
            scores[i] += cooccur
            scores[j] += cooccur

    return np.argsort(-scores)  # descending


# ===============================
# CORE DISCOVERY (ADVANCED)
# ===============================
def find_core(data, residual, sorted_items, lambda_):

    best_core = None
    best_cost = float("inf")

    for item in sorted_items:

        core_items = np.zeros(data.shape[1], dtype=bool)
        core_items[item] = True

        core_trans = residual[:, item].copy()

        # 🔥 try adding multiple items
        for other in sorted_items:

            if other == item:
                continue

            candidate_trans = core_trans & residual[:, other]

            # pruning: ignore weak intersections
            if np.sum(candidate_trans) < 2:
                continue

            new_items = core_items.copy()
            new_items[other] = True

            candidate = Pattern(new_items, candidate_trans)

            cost = compute_cost([candidate], data, lambda_)

            if cost < best_cost:
                best_cost = cost
                core_items = new_items
                core_trans = candidate_trans
                best_core = candidate

    return best_core


# ===============================
# TRANSACTION EXPANSION (ε_r)
# ===============================
def expand_transactions(pattern, residual, epsilon_r):

    trans = pattern.transactions.copy()

    for i in range(residual.shape[0]):

        if not trans[i]:

            overlap = np.sum(residual[i] & pattern.items)
            total = np.sum(pattern.items)

            # 🔥 STRICT condition
            if total > 0 and overlap >= max(1, int(total * (1 - epsilon_r))):
                trans[i] = True

    return Pattern(pattern.items, trans)


# ===============================
# PRUNING STRATEGY
# ===============================
def should_prune(pattern, residual):

    # remove tiny patterns
    if np.sum(pattern.items) < 2:
        return True

    if np.sum(pattern.transactions) < 2:
        return True

    # low coverage pruning
    coverage = np.sum(residual[pattern.transactions][:, pattern.items])
    if coverage == 0:
        return True

    return False


# ===============================
# RESIDUAL UPDATE
# ===============================
def update_residual(residual, pattern):
    residual[pattern.transactions] &= ~pattern.items


# ===============================
# MAIN ALGORITHM
# ===============================
def run_panda_plus_fast(k, data, epsilon_r=1.0, lambda_=0.4):

    patterns = []
    residual = data.copy()

    # 🔥 PAIR-BASED ORDERING
    sorted_items = compute_pair_scores(data)

    for _ in range(k):

        core = find_core(data, residual, sorted_items, lambda_)

        if core is None:
            break

        core = expand_transactions(core, residual, epsilon_r)

        # 🔥 pruning step
        if should_prune(core, residual):
            continue

        patterns.append(core)

        update_residual(residual, core)

    return patterns