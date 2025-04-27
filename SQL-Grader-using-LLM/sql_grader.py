import os
import re
from dotenv import load_dotenv
from openai import OpenAI

# Load environment variables from .env
load_dotenv()

# Initialize OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def grade_sql_answer(question, user_answer):
    system_prompt = (
        "You are a SQL expert and an examiner. You will receive a SQL question and a user's SQL answer.\n"
        "Your task is to:\n"
        "- Grade the SQL answer strictly on correctness (out of 10)\n"
        "- Provide detailed feedback under:\n"
        "    - Correctness\n"
        "    - Query structure\n"
        "    - SQL formatting and readability\n"
        "    - Query optimization if applicable\n"
        "- End with an overall comment.\n\n"
        "IMPORTANT:\n"
        "- Be strict but helpful.\n"
        "- If the SQL is wrong, explain where.\n"
        "- If there are optimization tips, suggest them.\n"
        "- Keep the feedback clear and beginner-friendly.\n"
    )

    user_prompt = (
        f"SQL Question:\n{question}\n\n"
        f"User's SQL Answer:\n{user_answer}\n\n"
        "Now grade this answer following the instructions."
    )

    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0
        )

        grading_response = response.choices[0].message.content

        score = extract_score(grading_response)
        detailed_feedback = extract_detailed_feedback(grading_response)

        return {
            "score": score,
            "feedback": grading_response,
            "detailed_feedback": detailed_feedback
        }

    except Exception as e:
        return {
            "score": 0,
            "feedback": f"Error grading answer: {e}",
            "detailed_feedback": {}
        }

def extract_score(text):
    """
    Extracts a score out of 10 from the text returned by the LLM.
    """
    match = re.search(r"(\d+)\s*/\s*10", text)
    if match:
        return int(match.group(1))
    return 0

def extract_detailed_feedback(text):
    """
    Extracts detailed feedback into sections like correctness, structure, etc.
    """
    sections = {
        "Correctness": "",
        "Query Structure": "",
        "Formatting and Readability": "",
        "Optimization Tips": ""
    }

    current_section = None
    for line in text.splitlines():
        line = line.strip()
        if not line:
            continue

        for key in sections.keys():
            if key.lower() in line.lower():
                current_section = key
                break
        else:
            if current_section:
                sections[current_section] += line + " "

    # Clean up spaces
    for key in sections:
        sections[key] = sections[key].strip()

    return sections
