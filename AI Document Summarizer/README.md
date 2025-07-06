# 📄 AI Document Summarizer 

This Streamlit app allows you to **summarize PDF documents** and **ask questions about them** using **locally running LLMs** via [Ollama](https://ollama.com).  
It's private, offline, and runs on your machine using models like **Mistral**.

---

## 🚀 Features

- 🔍 Extracts text from PDF files
- 🧠 Summarizes using local LLM (e.g., Mistral)
- ❓ Lets you ask questions about the document
- 🎛️ Adjustable creativity (`temperature`) and response length (`max_tokens`)
- 💡 Simple, clean UI built with Streamlit

---

## 🧰 Installation and Usage

Run the following commands in your terminal to install dependencies, install Ollama, and start the Mistral model locally:

```bash
pip install streamlit PyPDF2 requests

# Install Ollama (Linux/macOS)
curl -fsSL https://ollama.com/install.sh | sh

# Start the Mistral model locally
ollama run mistral

---

## 🧰 Installation

1. Make sure the Mistral model is running locally:

ollama run mistral

2. Run the Streamlit app:

streamlit run app.py

3. Open your browser to the displayed URL (default: http://localhost:8501).

4. Upload a PDF document.
