from fastapi import FastAPI # framework for building APIs
from openai import OpenAI # OpenAI API client
from pydantic import BaseModel # data validation / request models and settings management
import os # to read environment variables

app = FastAPI() # create FastAPI app instance


