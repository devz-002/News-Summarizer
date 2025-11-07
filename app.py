from fastapi import FastAPI # framework for building APIs
from openai import OpenAI # OpenAI API client
from pydantic import BaseModel # data validation / request models and settings management
import os # to read environment variables

app = FastAPI() # create FastAPI app instance

# Initialize OpenAI client with the API key from the env variable
client = OpenAI(api_key = os.getenv("OPENAI_API_KEY"))

class NewsText(BaseModel):
    news_source: str | None = None
    news_text: str

@app.post("/summarize")
def summarize(news: NewsText):
    # Prompt for ChatGPT
    prompt = f"""Summarize the following economic news and answer:
    1. What happened?
    2. Why it matters?
    3. What happens next?

    Keep it simple, short and easy to understand, use bullet points.

    Text:
    {news.news_text}
    """