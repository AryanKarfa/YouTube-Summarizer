# 🎥 YouTube Transcript Analyzer with Gemini AI ✨

This project fetches transcripts from YouTube videos using `youtube-transcript-api`, then analyzes them using Google's Gemini 2.5 Pro API to extract insights, summaries, or any other interpretation you want.

---

## 🚀 Features

- ✅ Extracts auto-generated or manual transcripts from YouTube videos.
- 🤖 Sends full transcript to Gemini AI (Google GenAI) for analysis.
- 📄 Clean, readable output of Gemini's response.
- 🛠️ Modular and easily extendable.

---

## 🧠 How It Works

- You provide a YouTube video ID.
- The script fetches the transcript (if available).
- The transcript is sent to Gemini 2.5 Flash using the Google-Genai SDK.
- The response is printed in the console (or used further).

## 📦 Dependencies

Install all required packages with:

```bash
pip install youtube-transcript-api google-genai
export GEMINI_API_KEY=your-api-key-here  # macOS/Linux
# OR
set GEMINI_API_KEY=your-api-key-here     # Windows CMD
# OR
$env:GEMINI_API_KEY="your-api-key-here"  # PowerShell
