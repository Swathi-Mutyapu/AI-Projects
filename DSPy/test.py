import requests
import dspy

def wiki_search_api(query, k=3):
    url = "https://search.genie.stanford.edu/wikipedia_20250320/"
    res = requests.post(url, json={"query": query, "num_blocks": k})
    res_json = res.json()
    # Example key — adjust after inspecting actual structure
    blocks = res_json.get("results", [])
    return [b.get("text", "") for b in blocks[:k]]

class WebRetriever:
    """Wraps an HTTP wiki search API for DSPy."""
    def __init__(self, k=3):
        self.k = k

    def __call__(self, query):
        texts = wiki_search_api(query, self.k)
        # Return list of DSPy docs
        return [dspy.Document(text=t) for t in texts]

# Configure DSPy with this retriever:
dspy.configure(
    lm=dspy.LM(model="gpt-3.5-turbo"),
    rm=WebRetriever()
)

retrieve = dspy.Retrieve(k=3)

# Now retrieval uses the free API
top_passages = retrieve("When was the first FIFA World Cup held?").passages
