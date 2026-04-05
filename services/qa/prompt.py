def build_prompt(question, chunks):
    context = "\n\n".join(
        [f"{i+1}. {c.get('text','')}" for i, c in enumerate(chunks)]
    )
    return f"""
You are a strict AI assistant.

ONLY answer using the provided context.
If the answer is not in the context, say:
"I could not find this in the video."
---
Context:
{context}
---
Question:
{question}
---
Answer:
"""