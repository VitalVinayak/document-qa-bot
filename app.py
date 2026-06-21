import streamlit as st
from src.query import ask_question

st.set_page_config(page_title="Document QA Bot")

st.title("📄 Document Q&A Bot")
st.write("Ask questions from uploaded documents")

question = st.text_input("Enter your question")

if st.button("Ask"):

    if question.strip() == "":
        st.warning("Please enter a question.")
    else:
        answer, citations = ask_question(question)

        st.subheader("Answer")
        st.success(answer)

        st.subheader("Sources")

        for citation in citations:
            st.write("•", citation)