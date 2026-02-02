import dspy
import os

# Initialize the LLM
lm = dspy.LM(model="openai/gpt-3.5-turbo")

# Attach the LM to DSPy
dspy.settings.configure(lm=lm)

# Define a Chain-of-Thought signature
cot = dspy.ChainOfThought("question -> answer, reasoning_steps")

# Run inference with chain-of-thought reasoning
result = cot(question="If you have 12 apples and give 5 to your friend, how many do you have left?")

# Print the final answer
print("Answer:", result.answer)

# Optional: Inspect the reasoning steps
print("\nReasoning Steps:")
for step in result.reasoning_steps:
    print("-", step)

# Inspect last LM call
lm.inspect_history(n=3)



#Comment the below section when running the code above and vice versa 

#Class based version 
import dspy

class AppleProblemSolver:
    def __init__(self, model_name="openai/gpt-3.5-turbo"):
        self.lm = dspy.LM(model=model_name)
        dspy.settings.configure(lm=self.lm)
        self.cot = dspy.ChainOfThought("question -> answer, reasoning_steps")

    def solve(self, question):
        result = self.cot(question=question)
        return result

solver = AppleProblemSolver()
result = solver.solve("If you have 12 apples and give 5 to your friend, how many do you have left?")

print(result.answer)
print("\nReasoning Steps:")
for step in result.reasoning_steps:
    print("-", step)