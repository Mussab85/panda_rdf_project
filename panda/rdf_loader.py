from rdflib import Graph


def detect_format(file_path):
    with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
        start = f.read(500).lower()

    if "<?xml" in start:
        return "xml"
    elif "@prefix" in start or "prefix" in start:
        return "turtle"
    else:
        return "nt"


def load_rdf(file_path):
    g = Graph()

    # Step 1 — detect format
    fmt = detect_format(file_path)
    print(f"Detected RDF format: {fmt}")

    # Step 2 — try normal parsing (fast path)
    try:
        g.parse(file_path, format=fmt)
        print(f"Loaded RDF normally ✅ ({len(g)} triples)")
        return g
    except Exception as e:
        print("⚠️ Normal parsing failed, switching to safe mode...")
        print(f"Error: {e}")

    # Step 3 — SAFE MODE (robust fallback)
    valid = 0
    skipped = 0

    with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
        for line in f:
            line = line.strip()

            # Skip empty or obviously invalid lines
            if not line or not line.endswith("."):
                skipped += 1
                continue

            try:
                g.parse(data=line, format="nt")
                valid += 1
            except Exception:
                skipped += 1

    print("Loaded RDF in safe mode ✅")
    print(f"Valid triples: {valid}")
    print(f"Skipped lines: {skipped}")

    if valid == 0:
        print("⚠️ WARNING: No valid triples found. Dataset may be severely corrupted.")

    return g