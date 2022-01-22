import streamlit as st
import asyncio, json

from wordcloud import WordCloud
from deepgram import Deepgram
from matplotlib import pyplot as plt
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
    """Gets transcription of an audio byte stream."""
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

###
# Streamlit App
###

st.set_page_config(layout="centered", page_icon="💬", page_title="Audio Cloud")
st.title("Audio Cloud")
uploaded_file = st.file_uploader(label="Upload Audio Recording", )
if uploaded_file is not None:
    audio_transcript = asyncio.run(get_inference(uploaded_file.getvalue()))
    wordcloud = wordcloud_generator(audio_transcript)
    fig = plt.figure()
    plt.imshow(wordcloud)
    plt.axis("off")
    st.pyplot(fig)