import streamlit as st
import asyncio, json

from wordcloud import WordCloud
from deepgram import Deepgram
from matplotlib import pyplot as plt
from config import *

import requests

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
    print(wordcloud_image)
    return wordcloud_image

# async def get_url(in_string):
#     r = await requests.post(
#     "https://api.deepai.org/api/text2img",
#     data={
#         'text': in_string,
#     },
#     headers={'api-key': '05fa4299-f2eb-407f-a55a-993bf7607693'})
#     return r.json()["output_url"]

# async def display_img():
#     out = await get_url("big man")
#     st.markdown(f"![Alt Text]" + out)

def get_url(in_string):
    r = requests.post(
    "https://api.deepai.org/api/text2img",
    data={
        'text': in_string,
    },
    headers={'api-key': '05fa4299-f2eb-407f-a55a-993bf7607693'})
    return r.json()["output_url"]

def display_img(x):
    out = get_url(x)
    st.write(x)
    st.markdown(f"![Alt Text]({out})")


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

input_string = st.sidebar.text_input(label="input text")

if input_string != None:
    display_img(input_string)

if uploaded_file is not None:
    audio_transcript = asyncio.run(get_inference(uploaded_file.getvalue()))
    wordcloud = wordcloud_generator(audio_transcript)
    fig = plt.figure()
    plt.imshow(wordcloud)
    plt.axis("off")
    st.pyplot(fig)






