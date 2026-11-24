
import streamlit as st
import os
import tempfile
import hashlib

from report_generator import generate_chat_report
from rag_pipeline import create_rag_pipeline, ask_question


# --------------------------------
# PAGE CONFIGURATION
# --------------------------------

st.set_page_config(
    page_title="AI Document Q&A Chatbot",
    page_icon="📄",
    layout="centered"
)


# --------------------------------
# APPLICATION TITLE
# --------------------------------

st.title("📄 AI Document Q&A Chatbot")

st.write(
    "Upload multiple PDF documents and ask questions "
    "across all your documents."
)


# --------------------------------
# INITIALIZE SESSION STATE
# --------------------------------

if "vector_store" not in st.session_state:
    st.session_state.vector_store = None

if "document_signature" not in st.session_state:
    st.session_state.document_signature = None

if "document_names" not in st.session_state:
    st.session_state.document_names = []

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []


# --------------------------------
# MULTIPLE PDF UPLOAD
# --------------------------------

uploaded_files = st.file_uploader(
    "Upload PDF documents",
    type=["pdf"],
    accept_multiple_files=True
)


# --------------------------------
# PROCESS UPLOADED DOCUMENTS
# --------------------------------

if uploaded_files:

    file_data = [
        (file.name, file.getvalue())
        for file in uploaded_files
    ]

    signature = hashlib.sha256(
        b"".join(
            name.encode("utf-8") + content
            for name, content in file_data
        )
    ).hexdigest()

    if signature != st.session_state.document_signature:

        with st.spinner("Processing your PDF documents..."):

            combined_vector_store = None

            try:

                for file_name, file_content in file_data:

                    with tempfile.NamedTemporaryFile(
                        delete=False,
                        suffix=".pdf"
                    ) as temp_file:

                        temp_file.write(file_content)
                        temp_pdf_path = temp_file.name

                    try:

                        document_vector_store = create_rag_pipeline(
                            temp_pdf_path,
                            source_name=file_name
                        )

                        if combined_vector_store is None:

                            combined_vector_store = document_vector_store

                        else:

                            combined_vector_store.merge_from(
                                document_vector_store
                            )

                    finally:

                        if os.path.exists(temp_pdf_path):
                            os.remove(temp_pdf_path)

                st.session_state.vector_store = combined_vector_store

                st.session_state.document_signature = signature

                st.session_state.document_names = [
                    name for name, content in file_data
                ]

                st.session_state.chat_history = []

                st.success(
                    f"{len(uploaded_files)} PDF document(s) "
                    "processed successfully!"
                )

            except Exception as e:

                st.session_state.vector_store = None
                st.session_state.document_signature = None

                st.error(f"Error processing documents: {e}")


# --------------------------------
# DISPLAY UPLOADED DOCUMENTS
# --------------------------------

if st.session_state.vector_store is not None:

    st.subheader("📚 Uploaded Documents")

    for name in st.session_state.document_names:

        st.write("📄", name)

    st.divider()


    # --------------------------------
    # CHAT INTERFACE
    # --------------------------------

    st.subheader("💬 Chat with Your Documents")

    # Display previous conversations

    for message in st.session_state.chat_history:

        with st.chat_message(message["role"]):

            st.markdown(message["content"])

            if (
                message["role"] == "assistant"
                and message.get("sources")
            ):

                with st.expander("📚 View Sources"):

                    for source in message["sources"]:

                        st.markdown(
                            f"**Document:** {source['source']}"
                        )

                        st.markdown(
                            f"**Page:** {source['page']}"
                        )

                        st.caption(
                            source["content"][:500]
                        )

                        st.divider()


    # --------------------------------
    # USER QUESTION
    # --------------------------------

    question = st.chat_input(
        "Ask a question about your uploaded documents..."
    )

    if question:

        with st.chat_message("user"):

            st.markdown(question)

        st.session_state.chat_history.append(
            {
                "role": "user",
                "content": question
            }
        )


        # --------------------------------
        # GENERATE AI RESPONSE
        # --------------------------------

        with st.chat_message("assistant"):

            with st.spinner(
                "Searching documents and generating answer..."
            ):

                try:

                    result = ask_question(
                        st.session_state.vector_store,
                        question
                    )

                    answer = result["answer"]
                    sources = result["sources"]

                    st.markdown(answer)


                    # Display source references

                    with st.expander("📚 View Sources"):

                        for source in sources:

                            st.markdown(
                                f"**Document:** {source['source']}"
                            )

                            st.markdown(
                                f"**Page:** {source['page']}"
                            )

                            st.caption(
                                source["content"][:500]
                            )

                            st.divider()


                    # Save answer and sources

                    st.session_state.chat_history.append(
                        {
                            "role": "assistant",
                            "content": answer,
                            "sources": sources
                        }
                    )

                except Exception as e:

                    st.error(
                        f"Error generating answer: {e}"
                    )


    # --------------------------------
    # DOWNLOAD CHAT REPORT
    # --------------------------------

    if st.session_state.chat_history:

        st.divider()

        st.subheader("📥 Download Your Report")

        report = generate_chat_report(
            st.session_state.document_names,
            st.session_state.chat_history
        )

        st.download_button(
            label="📄 Download Chat Report (PDF)",
            data=report,
            file_name="AI_Document_QA_Report.pdf",
            mime="application/pdf"
        )


    # --------------------------------
    # CLEAR CHAT HISTORY
    # --------------------------------

    if st.session_state.chat_history:

        if st.button("🗑️ Clear Chat History"):

            st.session_state.chat_history = []

            st.rerun()


    # --------------------------------
    # RESET DOCUMENTS
    # --------------------------------

    if st.button("🔄 Reset Documents"):

        st.session_state.vector_store = None
        st.session_state.document_signature = None
        st.session_state.document_names = []
        st.session_state.chat_history = []

        st.rerun()
