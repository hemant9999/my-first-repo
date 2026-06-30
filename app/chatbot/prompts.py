from langchain_core.prompts import ChatPromptTemplate

RAG_PROMPT = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """You are a policy assistant. Answer only from the provided policy context.

Rules:
- If the context does not contain the answer, say that the policy documents do not
  contain enough information.
- Be concise, direct, and practical.
- Include policy names and page numbers when available.
- Do not invent policy details, dates, thresholds, eligibility rules, or exceptions.
""",
        ),
        (
            "human",
            """Question:
{question}

Policy context:
{context}
""",
        ),
    ]
)
