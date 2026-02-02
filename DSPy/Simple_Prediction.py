

import dspy
import os

lm = dspy.LM(model="openai/gpt-3.5-turbo")

# Attach the LM to DSPy
dspy.settings.configure(lm=lm)

# Define prediction signature
predict = dspy.Predict("question -> answer")

# Run inference
prediction = predict(question="Who is the first president of the UK")

print(prediction.answer)

lm.inspect_history(n=1) 


#Comment the below section when running the code above and vice versa 

#Class based version 

import dspy
import os
 
class DSPyPredictor:
    """
    A class-based wrapper for DSPy single-turn predictions using a Signature.
    
    Features:
    - Initializes a language model.
    - Defines a reusable prediction signature.
    - Provides methods to ask questions and inspect prediction history.
    """

    def __init__(self, model_name="openai/gpt-3.5-turbo"):
        # Initialize the language model
        self.lm = dspy.LM(model=model_name)
        # Attach the LM to DSPy
        dspy.settings.configure(lm=self.lm)
        # Define a reusable prediction signature
        self.predict = dspy.Predict("question -> answer")

    def ask(self, question: str):
        """
        Run inference using the prediction signature.
        
        Args:
            question (str): The input question.
            
        Returns:
            str: The model's answer.
        """
        result = self.predict(question=question)
        return result.answer

    def history(self, n: int = 1):
        """
        Inspect past predictions made by this LM.
        
        Args:
            n (int): Number of recent predictions to show.
        """
        self.lm.inspect_history(n=n)


# === Example usage ===
if __name__ == "__main__":
    predictor = DSPyPredictor()

    # Ask a question
    answer = predictor.ask("Who is the first president of the UK?")
    print("Answer:", answer)


    # Inspect prediction history
    predictor.history(n=2)

