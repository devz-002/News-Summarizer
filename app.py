from fastapi import FastAPI, HTTPException # framework for building APIs
from openai import OpenAI # OpenAI API client
from pydantic import BaseModel # data validation / request models and settings management
import os # to read environment variables
import requests # to make HTTP requests

app = FastAPI() # create FastAPI app instance

# Initialize OpenAI client with the API key from the env variable
# client = OpenAI(api_key = os.getenv("APYHUB_API_KEY"))

APYHUB_URL = "https://api.apyhub.com/ai/summarize-text" # ApyHub endpoint for text summarization
APYHUB_API_KEY = os.getenv("APYHUB_API_KEY")


class NewsText(BaseModel):
    news_source: str | None = None
    news_text: str


@app.get("/")
def root():
    return {"ok": True, "msg": "News Summarizer API (ApyHub) is running. Use POST /summarize"}

@app.post("/summarize")
def summarize(news:NewsText):
    """Summarize the news text using ApyHub API."""

    if not APYHUB_API_KEY:
        raise HTTPException(status_code=500, detail = "APYHUB_API_KEY environment variable is missing")
    
    try:
        #prepare the payload for ApyHub API
        payload = {
            "text": news.news_text,
            "summary_length": "medium",
            "output_language": "en"
        }

        headers = {
            "apy-token": APYHUB_API_KEY,
            "Content-Type": "application/json"
        }

        # Send POST request to ApyHub API
        response = requests.post(APYHUB_URL, json=payload, headers=headers)

        if response.status_code != 200:
            raise HTTPException(status_code=response.status_code, detail=f"ApyHub API error: {response.text}")
        
        
        data = response.json()

        #Extract summary from response
        summary  = data.get("data", {}).get("summary", "No summary returned")

        return {
            "news_source": news.news_source,
            "news_result": summary
            }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"{type(e).__name__}: {e}")







# @app.post("/summarize")
# def summarize(news: NewsText):
#     # Prompt for ChatGPT
#     prompt = f"""Summarize the following economic news and answer:
#     1. What happened?
#     2. Why it matters?
#     3. What happens next?

#     Keep it simple, short and easy to understand, use bullet points.

#     Text:
#     {news.news_text}
#     """

#     try:
#         # Call the ChatGPT API (chat.completions)
#         response = client.chat.completions.create(
#             model = "gpt-4o-mini",
#             messages= [{"role":"user", "content": prompt}],
#             temperature=0.3
#         )

#         # Extract and return the summary from the response
#         summary = response.choices[0].message.content

#         # Return JSON to phone/HTTP shortcuts
#         # ..to be copied  to clipboard
#         return {"result": summary}

#     except Exception as e:
#         # Return a readable error instead of a blank 500
#         raise HTTPException(status_code=500, detail=f"{type(e).__name__}: {e}")