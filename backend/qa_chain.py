# from dotenv import load_dotenv
# load_dotenv()
# import os
# from openai import OpenAI

# openai_api_key = os.getenv("OPENAI_API_KEY")
# client = OpenAI(api_key=openai_api_key)

# def generate_question(profile_text):
#     prompt = f"""You are a technical interviewer.
# Given the following resume content, generate a relevant technical question:
# {profile_text}
# Only return the question."""
    
#     response = client.chat.completions.create(
#         model="gpt-3.5-turbo",
#         messages=[{"role": "user", "content": prompt}],
#         timeout=60
#     )
#     return response.choices[0].message.content
from dotenv import load_dotenv
load_dotenv()
import os
from openai import OpenAI, RateLimitError, AuthenticationError, OpenAIError

openai_api_key = os.getenv("OPENAI_API_KEY")

# Optional safety check for missing key
if openai_api_key:
    client = OpenAI(api_key=openai_api_key)
else:
    client = None

def generate_question(profile_text):
    prompt = f"""You are a technical interviewer.
Given the following resume content, generate a relevant technical question:
{profile_text}
Only return the question."""

    if not client:
        return "Mock question: What is the time complexity of your most optimized sorting algorithm?"

    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            timeout=60
        )
        return response.choices[0].message.content

    except (RateLimitError, AuthenticationError, OpenAIError) as e:
        print(f"⚠️ OpenAI API error: {e}")
        return "Mock question: What is the time complexity of your most optimized sorting algorithm?"


