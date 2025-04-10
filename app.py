import streamlit as st
st.set_page_config(page_title="AI Interviewer", layout="centered")

import openai
import os
from PyPDF2 import PdfReader
from dotenv import load_dotenv

# 🛠️ Set page config (must be first Streamlit command)

# 🧪 Sidebar Restart Button
st.sidebar.button("🔄 Restart Interview", on_click=lambda: st.session_state.clear())

# 🔐 Load environment variables and setup OpenAI
load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")
openai.api_key = openai_api_key  # ✅ setup like this


# 📄 Utility to extract text from uploaded resume
def extract_text_from_pdf(pdf):
    text = ""
    reader = PdfReader(pdf)
    for page in reader.pages:
        text += page.extract_text()
    return text

# 🧠 Generate interview question from resume
def generate_question(profile_text):
    prompt = f"""You are a technical interviewer.
Given the following resume content, generate a relevant technical question:
{profile_text}
Only return the question."""
    try:
        response = openai.ChatCompletion.create(  # ✅ updated usage
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            timeout=60
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"⚠️ Could not generate question: {e}"

# ✅ Evaluate user's answer
def evaluate_answer(question, answer):
    prompt = f"""
You are a senior software engineer interviewing a candidate.
Evaluate the following answer to the question and give a score out of 10 with a reason.

Question: {question}
Answer: {answer}

Give a brief reason and a score out of 10.
"""
    try:
        response = openai.ChatCompletion.create(  # ✅ updated usage
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            timeout=60
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"⚠️ Could not evaluate answer: {e}"

# 🧠 App Title
st.title("🧠 Virtual AI Interviewer")

# 🚀 Initialize session state
for key in ["resume_text", "question_index", "questions", "evaluations", "interview_started", "last_evaluation"]:
    if key not in st.session_state:
        if key in ["questions", "evaluations"]:
            st.session_state[key] = []
        elif key == "question_index":
            st.session_state[key] = 0
        else:
            st.session_state[key] = False

# 🧾 Step 1: Upload Resume
st.header("Step 1: Upload Your Resume")
uploaded_file = st.file_uploader("Upload your resume (PDF only)", type=["pdf"])

if uploaded_file and not st.session_state.resume_text:
    st.session_state.resume_text = extract_text_from_pdf(uploaded_file)
    st.success("✅ Resume uploaded successfully.")
    with st.expander("🔍 Preview Resume Text"):
        st.text_area("Extracted Resume Content", st.session_state.resume_text, height=250)

if uploaded_file and st.session_state.resume_text and not st.session_state.interview_started:
    if st.button("🎯 Start Interview"):
        with st.spinner("Generating first question..."):
            first_question = generate_question(st.session_state.resume_text)
            st.session_state.questions.append(first_question)
            st.session_state.interview_started = True
            st.rerun()

# 🧪 Step 2: Interview
if st.session_state.interview_started and st.session_state.questions:
    st.header(f"Step 2: Interview - Question {st.session_state.question_index + 1}")
    current_question = st.session_state.questions[st.session_state.question_index]
    st.markdown(f"**🤖 AI Interviewer:** {current_question}")
    user_answer = st.text_area("✍️ Your Answer", height=150, key=f"answer_input_{st.session_state.question_index}")

    if st.button("📤 Submit Answer"):
        with st.spinner("Evaluating your answer..."):
            evaluation = evaluate_answer(current_question, user_answer)
            st.session_state.evaluations.append({
                "question": current_question,
                "answer": user_answer,
                "evaluation": evaluation
            })
            st.session_state.last_evaluation = evaluation
            st.rerun()

    if st.session_state.last_evaluation:
        st.markdown("### 💬 Evaluation:")
        st.write(st.session_state.last_evaluation)
        if st.button("➡️ Next Question"):
            next_question = generate_question(st.session_state.resume_text)
            st.session_state.questions.append(next_question)
            st.session_state.question_index += 1
            st.session_state.last_evaluation = None
            st.rerun()
