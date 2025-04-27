import streamlit as st
import random
from sql_grader import grade_sql_answer

# ------------------------------
# Define questions with sample data
# ------------------------------
questions_dict = {
    "Q1": {
        "question": "Write a SQL query to SELECT all columns from the employees table.",
        "sample_data": """
**Table: employees**
+----+----------+-------------+--------+
| id | name     | department  | salary |
+----+----------+-------------+--------+
| 1  | Alice    | HR          | 50000  |
| 2  | Bob      | Engineering | 75000  |
| 3  | Charlie  | Marketing   | 60000  |
+----+----------+-------------+--------+
"""
    },
    "Q2": {
        "question": "Find the employee with the maximum salary.",
        "sample_data": """
**Table: employees**
+----+----------+--------+
| id | name     | salary |
+----+----------+--------+
| 1  | Alice    | 50000  |
| 2  | Bob      | 75000  |
| 3  | Charlie  | 60000  |
+----+----------+--------+
"""
    },
    "Q3": {
        "question": "Count the number of employees in each department.",
        "sample_data": """
**Table: employees**
+----+----------+--------------+
| id | name     | department_id|
+----+----------+--------------+
| 1  | Alice    | 101          |
| 2  | Bob      | 102          |
| 3  | Charlie  | 101          |
| 4  | David    | 103          |
+----+----------+--------------+
"""
    },
    "Q4": {
        "question": "List employees who earn more than $50,000.",
        "sample_data": """
**Table: employees**
+----+----------+--------+
| id | name     | salary |
+----+----------+--------+
| 1  | Alice    | 50000  |
| 2  | Bob      | 75000  |
| 3  | Charlie  | 60000  |
+----+----------+--------+
"""
    },
    "Q5": {
        "question": "Show total sales by each region.",
        "sample_data": """
**Table: Sales**
+---------+-------------+
| region  | sales_amount |
+---------+-------------+
| East    | 120000       |
| West    | 95000        |
| North   | 87000        |
| South   | 76000        |
+---------+-------------+
"""
    },
    "Q6": {
        "question": "Retrieve all products priced above $100.",
        "sample_data": """
**Table: Products**
+------------+----------------+-------+
| product_id | product_name    | price |
+------------+----------------+-------+
| 1          | Laptop          | 1200  |
| 2          | Phone           | 800   |
| 3          | Headphones      | 150   |
| 4          | Mouse           | 25    |
+------------+----------------+-------+
"""
    },
    "Q7": {
        "question": "Get the average salary per department.",
        "sample_data": """
**Table: employees**
+--------------+--------+
| department_id| salary |
+--------------+--------+
| 101          | 50000  |
| 102          | 75000  |
| 101          | 60000  |
+--------------+--------+
"""
    },
    "Q8": {
        "question": "Select customers who joined in the year 2023.",
        "sample_data": """
**Table: customers**
+-------------+----------+------------+
| customer_id | name     | join_date  |
+-------------+----------+------------+
| 1           | John     | 2022-05-10 |
| 2           | Lisa     | 2023-03-22 |
| 3           | Mike     | 2023-07-15 |
| 4           | Sophia   | 2021-11-02 |
+-------------+----------+------------+
"""
    },
}

# ------------------------------
# Helper function to get random questions
# ------------------------------
def get_random_questions(all_questions, num_questions=3):
    return random.sample(list(all_questions.items()), num_questions)

# ------------------------------
# Streamlit App
# ------------------------------

st.set_page_config(page_title="SQL Grader", layout="wide")

st.title("🧠 SQL Grader using LLM")
st.write("Answer the following SQL questions. After submitting, you will receive scores and detailed feedback!")

# --- Get user name ---
user_name = st.text_input("👤 Enter your Name:")

# --- Initialize random questions once ---
if "selected_questions" not in st.session_state:
    st.session_state.selected_questions = get_random_questions(questions_dict, 3)

# --- User answers dict ---
user_answers = {}

# --- Display Questions ---
for idx, (question_key, question_data) in enumerate(st.session_state.selected_questions):
    st.header(f"Question {idx+1}:")
    st.write(f"**Question:** {question_data['question']}")
    st.code(question_data['sample_data'], language="sql")

    user_input = st.text_area(f"✏️ Your SQL Answer for Question {idx+1}", key=f"answer_{idx}")
    user_answers[question_key] = user_input

# --- Submit Button ---
if st.button("🚀 Submit Answers"):
    if not user_name:
        st.warning("⚠️ Please enter your name before submitting.")
    else:
        st.success(f"✅ Answers submitted by {user_name}! Here's your feedback:")

        total_score = 0
        max_total = len(user_answers) * 10

        for idx, (question_key, question_data) in enumerate(st.session_state.selected_questions):
            user_sql = user_answers[question_key]
            grading_result = grade_sql_answer(question_data['question'], user_sql)

            with st.expander(f"📋 Feedback for Question {idx+1}"):
                st.subheader(f"Score: {grading_result['score']} / 10")

                detailed = grading_result.get("detailed_feedback", {})

                if detailed:
                    st.markdown("### 🧠 Detailed Feedback:")
                    for aspect, feedback in detailed.items():
                        if feedback:
                            st.markdown(f"**{aspect}:** {feedback}")

                st.markdown("### 📢 Overall Comment:")
                st.write(grading_result['feedback'])

            total_score += grading_result['score']

        # --- Final Scorecard ---
        st.markdown("---")
        st.title("🏆 Final Results")
        st.metric(label="Total Score", value=f"{total_score} / {max_total}")

        if total_score / max_total >= 0.8:
            st.success("🎉 Great job! You're strong in SQL!")
        elif total_score / max_total >= 0.5:
            st.info("👍 Good effort! Some improvements needed.")
        else:
            st.warning("🛠️ Keep practicing! Review the feedback carefully.")

