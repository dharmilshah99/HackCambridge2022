from email.mime import audio
import os
import asyncio
import streamlit as st
import streamlit.components.v1 as components
from matplotlib import pyplot as plt
from wordcloud import WordCloud
from deepgram import Deepgram

from config import *
import helper

from textblob import TextBlob
import sys

###
# Global Variables
### 
DG_CLIENT = Deepgram({
    'api_key': DEEPGRAM_API_KEY,
    'api_url': DEEPGRAM_API_URL
})

###
# Helpers
###

async def get_inference(audio_bytestream):
    source = {'buffer': audio_bytestream, 'mimetype': 'audio/wav'}
    response = await DG_CLIENT.transcription.prerecorded(source, {'punctuate': True})
    return response["results"]["channels"][0]["alternatives"][0]["transcript"]

_real_time_speechbar = components.declare_component(
    "real_time_speechbar",
    url="http://localhost:3001",
)

def real_time_speechbar(name, key=None):
    """Creates a real-time speechbar"""
    return _real_time_speechbar(name=name, key=key, default=0)

###
# Streamlit App
###
st.set_page_config(layout="centered", page_icon="💬", page_title="Audio Cloud")

st.title("Audio Cloud")
st.write("""
        Gain insights to your speech!
        """)

input_mode = st.selectbox('Type of input file', ('Live recording', 'Upload a recording'))

if input_mode == 'Live recording':
    
    with st.sidebar:
        st.write("Requires access to your microphone")
        transcript = real_time_speechbar("")
        
    if transcript is not (None or 0):
        st.subheader("WordCloud")
        wordcloud = helper.wordcloud_generator(transcript)
        fig = plt.figure()
        plt.imshow(wordcloud)
        plt.axis("off")
        st.pyplot(fig)
        
        st.subheader("Transcript")
        st.write(transcript)

if input_mode == 'Upload a recording':
    
    with st.sidebar:    
        st.write("Accepts any .wav/.mp3 files")
        uploaded_file = st.file_uploader(label="Upload Audio Recording", )

    if uploaded_file is not None:
        st.subheader("WordCloud")
        audio_transcript = asyncio.run(get_inference(uploaded_file.getvalue()))
        wordcloud = helper.wordcloud_generator(audio_transcript)
        fig = plt.figure()
        plt.imshow(wordcloud)
        plt.axis("off")
        st.pyplot(fig)
        
        st.subheader("Summary")
        num_sentences = st.slider('Please select number of sentences', 1, 5)
        summarised_text = helper.generate_summary(num_sentences,audio_transcript)
        for sentence in summarised_text:
            st.markdown(f"  -   {sentence}")
        
        st.subheader("Keywords Extraction")
        keywords = helper.extract_keywords(audio_transcript)
        num_keywords = st.slider('Please select number of keywords', 1, 10)
        for i in range(num_keywords):
            if i >= num_keywords:
                st.markdown(f"  -   {keywords[i]}")

        st.subheader("Sentiment Analysis")
        Blobject = TextBlob(audio_transcript)
        sentiment = Blobject.sentiment.polarity
        if sentiment >= 0.5:
            st.write(f"{sentiment}: 😀") 
        else:
            st.write(f"{sentiment}: ☹️")


