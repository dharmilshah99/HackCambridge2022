import os
import asyncio
import streamlit as st
import streamlit.components.v1 as components
from matplotlib import pyplot as plt
from wordcloud import WordCloud
from deepgram import Deepgram

from config import *

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

def wordcloud_generator(audio_transcript):
    """Generate wordcloud image."""
    wordcloud_image = WordCloud(
        background_color="white"
    ).generate(audio_transcript)
    return wordcloud_image

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
         Gets transcription of an audio byte stream.
         Add more description here at the end
         """)
uploaded_file = st.sidebar.file_uploader(label="Upload Audio Recording", )
    
analysis_mode = st.sidebar.selectbox('Analysis Mode', ('Lecture', 'Interview', 'IDK'))
st.write(f"## {analysis_mode} Analysis")

transcript = real_time_speechbar("")
st.write(transcript)
if transcript is not None:
    # audio_transcript = asyncio.run(get_inference(uploaded_file.getvalue()))
    wordcloud = wordcloud_generator(transcript)
    fig = plt.figure()
    plt.imshow(wordcloud)
    plt.axis("off")
    st.pyplot(fig)