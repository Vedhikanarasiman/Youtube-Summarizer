from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel
from dotenv import load_dotenv
import os
from youtube_transcript_api import YouTubeTranscriptApi
import google.generativeai as genai

# Load environment variables
load_dotenv()

# Configure Google Generative AI
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

app = FastAPI()

# Root endpoint for testing
@app.get("/")
def read_root():
    return {"message": "Welcome to my FastAPI application!"}

# Endpoint to handle favicon requests
@app.get("/favicon.ico")
def get_favicon():
    raise HTTPException(status_code=404, detail="No favicon")

# Pydantic model for video link input
class VideoLink(BaseModel):
    url: str

# Prompt for Gemini model
prompt = """
You are a YouTube video summarizer. Please summarize the transcript text in a structured format with the following sections:
1. Overview: A brief introduction to the topic.
2. Implementation: Key steps or methods used.
3. Challenges and Solutions: Challenges faced and how they were resolved.

Use bullet points for the details under each section. Use HTML tags to bold section headings.
"""


# Configure CORS middleware
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Replace with your React app's URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def extract_transcript_details(video_id):
    try:
        transcript_list = YouTubeTranscriptApi.get_transcript(video_id)
        transcript_text = " ".join([item['text'] for item in transcript_list])
        return transcript_text
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error extracting transcript: {str(e)}")

def generate_gemini_content(transcript_text, prompt):
    try:
        model = genai.GenerativeModel("gemini-pro")
        response = model.generate_content(prompt + transcript_text)
        final_summary = response.text.strip()
        return final_summary
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating summary: {str(e)}")

@app.get("/summary")
async def summarize(video_id: str = Query(..., description="YouTube video ID")):
    try:
        transcript_text = extract_transcript_details(video_id)
        summary = generate_gemini_content(transcript_text, prompt)
        return {"summary": summary}
    except HTTPException as http_err:
        raise http_err
    except Exception as err:
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {str(err)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
