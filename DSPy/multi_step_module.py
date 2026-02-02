import dspy

# -----------------------------
# Step 1: Configure the LLM
# -----------------------------
dspy.configure(lm=dspy.LM("openai/gpt-4o-mini"))

# -----------------------------
# Step 2: Define the multi-step CoT module
# -----------------------------
class MultiStepCoTModule(dspy.Module):
    def __init__(self):
        super().__init__()
        self.step_by_step_chain = dspy.ChainOfThought("question -> step_by_step_reasoning")
        self.final_answer_chain = dspy.ChainOfThought("question, step_by_step_reasoning -> final_answer")
    
    def forward(self, question):
        reasoning_output = self.step_by_step_chain(question=question)
        reasoning = reasoning_output.step_by_step_reasoning
        
        answer_output = self.final_answer_chain(question=question, step_by_step_reasoning=reasoning)
        answer = answer_output.final_answer
        
        return dspy.Prediction(reasoning=reasoning, answer=answer)

# -----------------------------
# Step 3: Instantiate the module
# -----------------------------
module = MultiStepCoTModule()

# -----------------------------
# Step 4: Correct way to call the module
# -----------------------------
question = "If a train travels 60 miles in 1.5 hours, what is its average speed?"

# ✅ Instead of module.forward(...), call the module like a function
result = module(question)

print("Question:", question)
print("Step-by-step Reasoning:\n", result.reasoning)
print("Answer:", result.answer)
