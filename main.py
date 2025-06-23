import os
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize OpenAI client
client = OpenAI()

user_input = input("Enter a input: ")
research_question = ""
# Make an API call for the research question
try:
    response = client.chat.completions.create(
        model="gpt-4.1",
        messages=[
            {
                "role": "developer",
                "content": f"turn this input into a prompt for a LLM with the instructions: 'You are an expert prompt engineer specializing in creating prompts for research purposes. You are given a input which you will need to rephrase into a research input within the context of medical research using the PICO framework. The input is: {user_input}'"
            },
            {
                "role": "user",
                "content": user_input
            }
        ]
    )
    # Get the assistant's reply
    print("Assistant:", response.choices[0].message.content)
    research_question = response.choices[0].message.content
except Exception as e:
    print(f"An error occurred: {e}")

# Make an API call for literature review/introduction

intro_prompt = (
    f"You are an expert academic writer specializing in the writing of systematic reviews and original research articles for peer-reviewed medical journals.\n\n"
    f"Your task is to write an *Introduction* section for a paper that addresses the following research question:\n"
    f"{research_question}\n\n"
    "The Introduction should:\n"
    "1. Be roughly **500–800 words** in length.\n"
    "2. Include approximately **15–20 citations** from **recent (last 10 years if possible), peer-reviewed journal articles**.\n"
    "   - Format citations as simple (Author, Year) inline, so that they can be manually inserted into a reference manager later.\n"
    "3. Clearly lay out:\n"
    "   - **Background** of the topic — the existing state of knowledge.\n"
    "   - **Context** — why this is an important area of study.\n"
    "   - **Rationale** — what gap in the literature or clinical practice this study seeks to address.\n"
    "   - **Primary objective(s)** of the paper.\n"
    "   - **Secondary objective(s)** if applicable.\n\n"
    "Maintain a formal academic tone appropriate for submission to a leading medical journal (such as NEJM, The Lancet, JAMA, BMJ, or Nature Medicine).\n\n"
    "Do not fabricate references — only use plausible, realistic references that exist in the literature (you may provide a placeholder author and year if needed)."
)

try:
    response = client.chat.completions.create(
        model="gpt-4.1",
        messages=[
            {
                "role": "developer",
                "content": intro_prompt
            },
            {
                "role": "user",
                "content": "write an introduction for the following research question: {research_question}"
            },
        ]
    )
    print("Assistant:", response.choices[0].message.content)
except Exception as e:
    print(f"An error occurred: {e}")

