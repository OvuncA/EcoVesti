#!/usr/bin/env python
from fastapi import FastAPI, BackgroundTasks, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
import os
from dotenv import load_dotenv
from ecovesti_v2.crew import EcovestiV2Crew 

load_dotenv()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)


# Get the directory of the current file
current_file_path = os.path.dirname(os.path.abspath(__file__))

# Use absolute paths for the static and templates directories
templates_path = os.path.join(current_file_path, "./templates")
static_path = os.path.join(current_file_path, "./static")

templates = Jinja2Templates(directory=templates_path)
app.mount("/static", StaticFiles(directory=static_path), name="static")

class URLData(BaseModel):
    url: str

@app.get("/")
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/analyze/")
async def analyze_url(url_data: URLData, background_tasks: BackgroundTasks):
    url = url_data.url
    message = f"I've started the analysis for {url}"
    background_tasks.add_task(run_analysis, url)
    return {"message": message}

async def run_analysis(url):
    try:
        inputs = {'user_URL': url}
        crewResult = EcovestiV2Crew().crew().kickoff(inputs=inputs)

        safe_url_name = "final_product_report"
        filename = os.path.join(static_path, f"{safe_url_name}_latest.txt")

        result = crewResult
        with open(filename, "w") as file:
            file.write(result)
        
    except Exception as e:
        print(f"An error occurred: {e}")

# Run with Uvicorn
# uvicorn main:app --reload