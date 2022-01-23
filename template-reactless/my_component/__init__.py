import os
import asyncio
import streamlit as st
import streamlit.components.v1 as components
from matplotlib import pyplot as plt
from wordcloud import WordCloud
from deepgram import Deepgram
from textblob import TextBlob

from config import *
# For DeepAI
import helper
import requests_async as requests

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

async def gen_img(transcript):
    transcript_split = transcript.split()
    if len(transcript_split) >= 4:
        sample = transcript_split[-4] + " " + transcript_split[-3] + " " + transcript_split[-2] + " " + transcript_split[-1]
    else:
        sample = transcript 
    r = await requests.post(
        "https://api.deepai.org/api/text2img",
        data={
            'text': sample,
        },
        headers={'api-key': '05fa4299-f2eb-407f-a55a-993bf7607693'})    
    url=r.json()["output_url"]
    st.image(url,width=600)
    st.write(f"Caption: {sample}")
    
###
# Streamlit App
###
st.set_page_config(layout="wide", page_icon="💬", page_title="Audio Cloud")

st.title("Audio Cloud")
st.write("""
        Gain insights to your speech!
        """)

input_mode = st.sidebar.selectbox('Type of input file', ('Live recording', 'Upload a recording'))



if input_mode == 'Live recording':
    
    with st.sidebar:
        st.write("Requires access to your microphone")
        transcript = real_time_speechbar("")
    
    if transcript is not (None or 0):
        col1, col2 = st.columns([2, 1])
        col1.subheader("WordCloud")
        wordcloud = helper.wordcloud_generator(transcript)
        fig = plt.figure()
        plt.imshow(wordcloud)
        plt.axis("off")
        col1.pyplot(fig)
        
        col2.subheader("Image")
        with col2:
            asyncio.run(gen_img(transcript))
        
        st.subheader("Transcript")
        st.write(transcript)

if input_mode == 'Upload a recording':
    
    with st.sidebar:    
        st.write("Accepts any .wav/.mp3 files")
        uploaded_file = st.file_uploader(label="Upload Audio Recording", )

    if uploaded_file is not None:
        col1,col2,col3 = st.columns([1,3,1])
        col2.subheader("WordCloud")
        audio_transcript = asyncio.run(get_inference(uploaded_file.getvalue()))
        wordcloud = helper.wordcloud_generator(audio_transcript)
        fig = plt.figure(figsize=[2,2])
        plt.imshow(wordcloud)
        plt.axis("off")
        col2.pyplot(fig)
        
        col2.subheader("Summary")
        num_sentences = col2.slider('Please select number of sentences', 1, 5)
        summarised_text = helper.generate_summary(num_sentences,audio_transcript)
        for sentence in summarised_text:
            col2.markdown(f"  -   {sentence}")
        
        col2.subheader("Keywords Extraction")
        num_keywords = col2.slider('Please select number of keywords', 1, 10)
        keywords = helper.extract_keywords(audio_transcript)
        for i in range(num_keywords):
            col2.markdown(f"  -   {keywords[i]}")
            
        col2.subheader("Sentiment Analysis")
        Blobject = TextBlob(audio_transcript)
        sentiment = Blobject.sentiment.polarity
        if sentiment >= 0:
            col2.write(f"{sentiment}: 😀") 
        else:
            col2.write(f"{sentiment}: ☹️")