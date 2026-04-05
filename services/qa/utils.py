def select_diverse_chunks(chunks, limit=3, min_gap=10):
    """
    Select top diverse chunks based on score + temporal distance
    """

    if not chunks:
        return []

    # 🔥 Sort by score (descending)
    chunks = sorted(chunks, key=lambda x: x.get("score", 0), reverse=True)

    selected = []
    used_starts = []

    for c in chunks:
        start = c.get("start", 0)

        # 🔥 Check temporal diversity
        if all(abs(start - s) >= min_gap for s in used_starts):
            selected.append(c)
            used_starts.append(start)

        if len(selected) >= limit:
            break

    return selected