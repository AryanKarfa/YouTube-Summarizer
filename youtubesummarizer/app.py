import os
from youtube_transcript_api import YouTubeTranscriptApi
from google import genai
from google.genai import types
from fastapi import FastAPI
import json
import re

app = FastAPI()

def get_transcript(video_id):
    try:
        transcript = YouTubeTranscriptApi.get_transcript(video_id)
        full_text = "\n".join([entry['text'] for entry in transcript])
        return full_text
    except Exception as e:
        return f"Error fetching transcript: {e}"


def call_gemini_with_transcript(transcript_text):
    client = genai.Client(api_key="AIzaSyDxyWNLUrRf1F1HbK5zFl8mPv23P7BRShc")
    model = "gemini-2.0-flash"
    prompt = f"""
Based on the below YouTube transcription, return me a brief summary of the topic
in the following JSON format only:
{{
    "topic_name":"name of the topic",
    "topic_summary":"summaty of the topic"
}}

Transcript:
\"\"\"{transcript_text}\"\"\"
"""

    contents = [
        types.Content(
            role="user",
            parts=[types.Part.from_text(text = prompt)],
        )
    ]

    config = types.GenerateContentConfig(
        temperature=0.5,
        response_mime_type="text/plain",
    )

    response = client.models.generate_content(
        model=model,
        contents=contents,
        config=config,
    )

    print(response.text)
    return response.text


def parse_json_block(code_block_str):
    """
    Converts a string formatted like a markdown code block into a Python dict.
    Removes triple backticks and language hints (like ```json).
    """
    # Remove triple backticks and optional language hint like ```json
    cleaned = re.sub(r"^```(?:json)?\n|\n```$", "", code_block_str.strip(), flags=re.IGNORECASE)
    cleaned = cleaned.replace('\n', '').replace('\\n', '').strip()
    
    # Convert to dictionary
    try:
        return json.loads(cleaned)
    except json.JSONDecodeError as e:
        print("JSON decoding failed:", e)
        return None



def extract_youtube_id(url):
    if "youtube.com/watch?v=" in url:
        return url.split("=")[1].split("&")[0]
    elif "youtu.be/" in url:
        return url.split("/")[-1]
    else:
        raise ValueError("Invalid YouTube URL")


@app.get("/summarize")
def get_summary(url: str):
    video_id = extract_youtube_id(url)
    transcript = get_transcript(video_id)
    if transcript:
        summary = call_gemini_with_transcript(transcript)
        print("Summary:", summary)
        return parse_json_block(summary)
    else:
        return {"error": "Transcript not found"}