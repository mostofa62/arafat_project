import os
from dotenv import load_dotenv

load_dotenv()
from langchain_openai import ChatOpenAI

from langchain.prompts import ChatPromptTemplate
import os

# Set your OpenRouter key and endpoint
#os.environ["OPENAI_API_KEY"] = "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"
OPENROUTER_BASE_URL = "https://openrouter.ai/api/v1"

llm = ChatOpenAI(
    model="mistralai/mistral-7b-instruct",
    base_url=OPENROUTER_BASE_URL,
    api_key=os.environ["OPENAI_API_KEY"]
)

schema_description = """
Database Schema:
- Table: courses(id, title, description, teacher_id, price)
- Table: orders(id, amount, payment_status, course_id)
Each order has a course_id linking to the course.
"""

prompt_template = ChatPromptTemplate.from_template(
    "Given the schema:\n{schema}\n\nWrite a SQL query to answer the question:\n'{question}'"
)

question = "Which course sold the most (based on completed orders)?"

messages = prompt_template.format_messages(
    schema=schema_description,
    question=question
)

response = llm(messages)
print("Generated SQL Query:\n", response.content)
