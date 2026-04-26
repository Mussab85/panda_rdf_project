import numpy as np


# =========================
# PATTERN CLASS
# =========================
class Pattern:
    def __init__(self, items, transactions):
        self.items = items
        self.transactions = transactions


# =========================
# XOR COST (paper definition)
# =========================
def cost(D, pattern):
    cover = np.outer(pattern.transactions, pattern.items)
    return np.sum(cover ^ D)


# =========================
# NOT TOO NOISY
# =========================
def not_too_noisy(D, pattern, epsilon_r, epsilon_c):
    rows = np.flatnonzero(pattern.transactions)
    cols = np.flatnonzero(pattern.items)

    if len(rows) == 0 or len(cols) == 0:
        return False

    sub = D[np.ix_(rows, cols)]

    if np.any(np.sum(sub, axis=1) < (1 - epsilon_r) * len(cols)):
        return False

    if np.any(np.sum(sub, axis=0) < (1 - epsilon_c) * len(rows)):
        return False

    return True


# =========================
# FIND CORE (paper-aligned)
# =========================
def find_core(DR):

    N, M = DR.shape

    CI = np.zeros(M, dtype=bool)
    CT = np.zeros(N, dtype=bool)

    EI = []
    ET = []

    # initialize with best item
    for j in range(M):
        if np.sum(DR[:, j]) > 0:
            CI[j] = True
            CT = DR[:, j].copy()
            ET.append(j)
            break

    current = Pattern(CI.copy(), CT.copy())
    current_cost = cost(DR, current)

    for j in range(M):

        if CI[j]:
            continue

        CI_star = CI.copy()
        CI_star[j] = True

        CT_star = CT & DR[:, j]

        if np.sum(CT_star) == 0:
            EI.append(j)
            continue

        candidate = Pattern(CI_star, CT_star)
        new_cost = cost(DR, candidate)

        if new_cost <= current_cost:
            CI = CI_star
            CT = CT_star
            current_cost = new_cost
        else:
            EI.append(j)

    return Pattern(CI, CT), EI, ET


# =========================
# EXTEND CORE (paper-aligned)
# =========================
def extend_core(pattern, EI, ET, D, epsilon_r, epsilon_c):

    CI = pattern.items.copy()
    CT = pattern.transactions.copy()

    current = Pattern(CI.copy(), CT.copy())
    current_cost = cost(D, current)

    # === extend transactions ===
    while ET:
        t = ET.pop(0)

        CT_star = CT.copy()
        CT_star[t] = True

        candidate = Pattern(CI.copy(), CT_star)

        if not_too_noisy(D, candidate, epsilon_r, epsilon_c):
            new_cost = cost(D, candidate)

            if new_cost <= current_cost:
                CT = CT_star
                current_cost = new_cost

    # === extend items ===
    while EI:
        e = EI.pop(0)

        CI_star = CI.copy()
        CI_star[e] = True

        candidate = Pattern(CI_star, CT.copy())

        if not_too_noisy(D, candidate, epsilon_r, epsilon_c):
            new_cost = cost(D, candidate)

            if new_cost <= current_cost:
                CI = CI_star
                current_cost = new_cost
                break  # important (matches pseudo)

    return Pattern(CI, CT)


# =========================
# MAIN PANDA+ (paper version)
# =========================
def run_panda_plus_exact(k, data, epsilon_r, epsilon_c, lambda_=None):

    # NOTE: lambda_ is accepted but NOT used (paper version)

    D = data.astype(bool)
    DR = D.copy()

    patterns = []
    logs = []

    for step in range(k):

        logs.append(f"\n=== Pattern {step+1} ===")

        core, EI, ET = find_core(DR)

        if core is None:
            logs.append("No more patterns")
            break

        pattern = extend_core(core, EI, ET, DR, epsilon_r, epsilon_c)

        rows = np.flatnonzero(pattern.transactions)
        cols = np.flatnonzero(pattern.items)

        logs.append(f"Pattern size: items={len(cols)}, rows={len(rows)}")

        if len(rows) == 0 or len(cols) == 0:
            logs.append("Empty pattern → stop")
            break

        # =========================
        # RESIDUAL UPDATE (correct)
        # =========================
        removed = 0
        for i in rows:
            for j in cols:
                if DR[i, j]:
                    DR[i, j] = False
                    removed += 1

        logs.append(f"Removed: {removed}")
        logs.append(f"Remaining: {np.sum(DR)}")

        patterns.append(pattern)

        if np.sum(DR) == 0:
            logs.append("Matrix empty → stop")
            break

    logs.append(f"\nTotal patterns: {len(patterns)}")

    return patterns, logs