import streamlit as st
import google.generativeai as genai
import os
from dotenv import load_dotenv
load_dotenv()  ## load all the environment variables..

from youtube_transcript_api import YouTubeTranscriptApi

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

prompt="You are a youtube video summarizer, you will be taking the transcript text and summaring the entire video and providing the important summary in points within 250 words . Please provide the summary of the text here : "

#### Getting the transcript data from yt videos
def extract_transcript_details(youtube_video_url):
    try:
        video_id = youtube_video_url.split("=")[1]
        transcript_text = YouTubeTranscriptApi.get_transcript(video_id)

        transcript = ""
        for i in transcript_text:
            transcript += " " + i["text"]

        return transcript

    except Exception as e:
        raise e
    
### Getting the summary based on prompt from google gemini 
def generate_gemini_content(transcript_text, prompt):

    model = genai.GenerativeModel("gemini-pro")
    response = model.generate_content(prompt+ transcript_text)

    return response.text


st.title("youtube Transcript to Detailed Notes Convertor")
youtube_link = st.text_input("Enter youTube video Link: ")

if youtube_link:
    video_id = youtube_link.split("=")[1]
    st.image(f"http://img.youtube.com/vi/{video_id}/0.jpg", use_container_width=True)

if st.button("Get Detailed Notes"):
    transcript_text = extract_transcript_details(youtube_link)
    
    if transcript_text:
        summary = generate_gemini_content(transcript_text, prompt)
        st.markdown("## Detailed NOte: ")
        st.write(summary)
    