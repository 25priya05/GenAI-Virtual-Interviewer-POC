# from dotenv import load_dotenv
# load_dotenv()

# import os
# from openai import OpenAI

# openai_api_key = os.getenv("OPENAI_API_KEY")
# client = OpenAI(api_key=openai_api_key)

# def evaluate_answer(question, answer):
#     prompt = f"""
# You are a senior software engineer interviewing a candidate.
# Evaluate the following answer to the question and give a score out of 10 with a reason.

# Question: {question}
# Answer: {answer}

# Give a brief reason and a score out of 10.
# """
#     response = client.chat.completions.create(
#         model="gpt-3.5-turbo",
#         messages=[{"role": "user", "content": prompt}]
#     )
#     return response.choices[0].message.content
from dotenv import load_dotenv
load_dotenv()

import os
from openai import OpenAI, RateLimitError, AuthenticationError, OpenAIError

openai_api_key = os.getenv("OPENAI_API_KEY")

if openai_api_key:
    client = OpenAI(api_key=openai_api_key)
else:
    client = None

def evaluate_answer(question, answer):
    prompt = f"""
You are a senior software engineer interviewing a candidate.
Evaluate the following answer to the question and give a score out of 10 with a reason.

Question: {question}
Answer: {answer}

Give a brief reason and a score out of 10.
"""

    if not client:
        return "Mock evaluation: The answer shows a basic understanding but lacks depth. Score: 6/10"

    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}]
        )
        return response.choices[0].message.content

    except (RateLimitError, AuthenticationError, OpenAIError) as e:
        print(f"⚠️ OpenAI API error: {e}")
        return "Mock evaluation: The answer shows a basic understanding but lacks depth. Score: 6/10"


