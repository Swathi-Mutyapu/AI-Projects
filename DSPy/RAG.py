import PyPDF2
import dspy

# -----------------------------
# Step 1: Configure LLM
# -----------------------------
dspy.configure(lm=dspy.LM(model="gpt-3.5-turbo"))

# -----------------------------
# Step 2: Read PDF and chunk text
# -----------------------------
pdf_path = r"C:\Users\mail2\Downloads\big-book-data-engineering.pdf"
reader = PyPDF2.PdfReader(pdf_path)

texts = []
for page in reader.pages:
    text = page.extract_text()
    if text:
        texts.append(text)

# Chunk text into smaller blocks
CHUNK_SIZE = 500
chunks = []
for t in texts:
    for i in range(0, len(t), CHUNK_SIZE):
        chunk = t[i:i+CHUNK_SIZE].strip()
        if chunk:
            chunks.append(chunk)

# -----------------------------
# Step 3: Create a custom local retriever
# -----------------------------
class LocalRetriever:
    """Simple local retriever from preloaded chunks."""
    def __init__(self, chunks, k=3):
        self.chunks = chunks
        self.k = k

    def __call__(self, query):
        # Very simple: return first k chunks for demonstration
        return dspy.Prediction(passages=self.chunks[:self.k])

# Instantiate retriever
retriever = LocalRetriever(chunks, k=3)

# -----------------------------
# Step 4: GenerateAnswer Signature
# -----------------------------
class GenerateAnswer(dspy.Signature):
    context = dspy.InputField(desc="may contain relevant facts")
    question = dspy.InputField()
    answer = dspy.OutputField(desc="short answer")

    def forward(self, context, question):
        ctx_text = "\n".join(context)
        prompt = f"Context:\n{ctx_text}\n\nQuestion: {question}\nAnswer briefly:"
        response = dspy.lm(prompt=prompt)
        return {"answer": response.text.strip()}

# -----------------------------
# Step 5: RAG Module
# -----------------------------
class RAG(dspy.Module):
    def __init__(self, retriever):
        super().__init__()
        self.retrieve = retriever
        self.generate_answer = dspy.ChainOfThought(GenerateAnswer)

    def forward(self, question):
        context = self.retrieve(question).passages  # list of strings
        prediction = self.generate_answer(context=context, question=question)
        return dspy.Prediction(context=context, answer=prediction.answer)

# -----------------------------
# Step 6: Run RAG
# -----------------------------
rag = RAG(retriever)
question = "What are the main components of a data engineering pipeline?"
output = rag(question)

print("\n=== Retrieved Contexts ===")
for i, p in enumerate(output.context, 1):
    print(f"{i}. {p}\n")

print("=== Answer ===")
print(output.answer)
