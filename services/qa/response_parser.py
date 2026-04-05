def parse_response(answer: str, chunks: list):
    return {
        "answer": answer.strip(),
        "sources": [
            {
                "start": c["start"],
                "end": c["end"]
            } for c in chunks
        ],
        "confidence": round(0.75 + (0.05 * len(chunks)), 2)
    }