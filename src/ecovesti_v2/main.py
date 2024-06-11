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

templates = Jinja2Templates(directory="templates")
analysis_status = {}
app.mount("/static", StaticFiles(directory="static"), name="static")

class URLData(BaseModel):
    url: str

@app.get("/")
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/status/{url}")
async def get_status(url: str):
    status = analysis_status.get(url, "Not Started")
    return {"status": status}

@app.get("/result/{url}")
async def get_result(url: str):
    safe_url_name = "".join(x for x in url if x.isalnum())
    filename = f"{safe_url_name}_latest.txt"  # Assuming you save it with this pattern
    if os.path.exists(filename):
        with open(filename, "r") as file:
            content = file.read()
        return {"result": content}
    return {"result": "Analysis not complete or file not found"}

@app.post("/analyze/")
async def analyze_url(url_data: URLData, background_tasks: BackgroundTasks):
    url = url_data.url
    message = f"I've started the analysis for {url}"
    background_tasks.add_task(run_analysis, url)
    return {"message": message}

async def run_analysis(url):
    analysis_status[url] = "In Progress"
    try:
        inputs = {'user_URL': url}
        EcovestiV2Crew().crew().kickoff(inputs=inputs)

        safe_url_name = "".join(x for x in url if x.isalnum())
        filename = f"{safe_url_name}_latest.txt"

        result = "Sample result"  # Replace with actual result handling
        with open(filename, "w") as file:
            file.write(result)
        
        analysis_status[url] = "Complete"
    except Exception as e:
        analysis_status[url] = "Failed"
        print(f"An error occurred: {e}")

# Run with Uvicorn
# uvicorn main:app --reload