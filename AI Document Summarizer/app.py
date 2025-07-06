import streamlit as st
import requests
from PyPDF2 import PdfReader


def extract_text(pdf_file):
    pdf = PdfReader(pdf_file)
    text = ""
    for page in pdf.pages:
        text += page.extract_text() + "\n"
    return text

def summarize_text(text, temperature=0.5, max_tokens=300):
    prompt = f"Summarize the following text:\n\n{text}"
    payload = {
        "model": "mistral",
        "prompt": prompt,
        "temperature": temperature,
        "max_tokens": max_tokens,
        "stream": False
    }
    response = requests.post("http://localhost:11434/api/generate", json=payload)
    if response.status_code == 200:
        return response.json().get("response", "No response received.")
    else:
        return f"Error: {response.status_code} - {response.text}"

def ask_question(document_text, question, temperature=0.5, max_tokens=300):
    prompt = f"""
You are an assistant who answers questions based on the following document:

{document_text}

Question: {question}

Answer:
"""
    payload = {
        "model": "mistral",
        "prompt": prompt,
        "temperature": temperature,
        "max_tokens": max_tokens,
        "stream": False
    }
    response = requests.post("http://localhost:11434/api/generate", json=payload)
    if response.status_code == 200:
        return response.json().get("response", "No response received.")
    else:
        return f"Error: {response.status_code} - {response.text}"

st.title("AI Document Summarizer")

uploaded_file = st.file_uploader("Upload a PDF document", type=["pdf"])

temperature = st.slider("Temperature (Creativity)", 0.0, 1.0, 0.5)
max_tokens_summary = st.slider("Max Tokens for Summary", 50, 500, 300)
max_tokens_answer = st.slider("Max Tokens for Answers", 50, 300, 150)

if uploaded_file is not None:
    with st.spinner("Extracting text from document..."):
        document_text = extract_text(uploaded_file)
    st.success("Document loaded!")

    if st.button("Summarize Document"):
        with st.spinner("Generating summary..."):
            summary = summarize_text(document_text, temperature, max_tokens_summary)
        st.subheader("Summary")
        st.write(summary)

    question = st.text_input("Ask a question about the document:")

    if st.button("Get Answer") and question.strip() != "":
        with st.spinner("Generating answer..."):
            answer = ask_question(document_text, question, temperature, max_tokens_answer)
        st.subheader("Answer")
        st.write(answer)
