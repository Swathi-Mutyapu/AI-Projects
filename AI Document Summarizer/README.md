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

## 🧰 Installation

Install required Python libraries:

```bash
pip install streamlit PyPDF2 requests

# Install Ollama (Linux/macOS)
curl -fsSL https://ollama.com/install.sh | sh

# Start the Mistral model locally
ollama run mistral

Project Structure

📁 ai-doc-summarizer/
├── app.py           # Streamlit app with summarizer and Q&A
└── README.md        # You’re reading it 🙂
