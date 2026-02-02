import dspy
import os


# Configure the language model (NEW WAY)
lm = dspy.LM(model="openai/gpt-3.5-turbo")

# Attach the LM to DSPy
dspy.settings.configure(lm=lm)

# Define prediction signature
predict = dspy.Predict("question -> answer")

# Run inference
prediction = predict(question="How many e's are in the word Strawberry")

print(prediction.answer)
