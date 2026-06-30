import streamlit as st

from app.chatbot.chain import answer_question

st.set_page_config(page_title="Policy RAG Assistant", page_icon=":material/policy:", layout="wide")

st.title("Policy RAG Assistant")

with st.sidebar:
    st.header("Retrieval")
    top_k = st.slider("Context chunks", min_value=1, max_value=12, value=6)
    st.caption("Answers are grounded in locally ingested policy PDFs.")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        if message.get("citations"):
            with st.expander("Citations"):
                for citation in message["citations"]:
                    page = f", page {citation.page_number}" if citation.page_number else ""
                    st.write(f"- {citation.policy_name or citation.source_file}{page}")

question = st.chat_input("Ask a policy question")
if question:
    st.session_state.messages.append({"role": "user", "content": question})
    with st.chat_message("user"):
        st.markdown(question)

    with st.chat_message("assistant"):
        with st.spinner("Searching policies..."):
            response = answer_question(question, top_k=top_k)
        st.markdown(response.answer)
        if response.citations:
            with st.expander("Citations"):
                for citation in response.citations:
                    page = f", page {citation.page_number}" if citation.page_number else ""
                    st.write(f"- {citation.policy_name or citation.source_file}{page}")

    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": response.answer,
            "citations": response.citations,
        }
    )
