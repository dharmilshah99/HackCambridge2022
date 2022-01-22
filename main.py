import streamlit as st
import asyncio, json

from deepgram import Deepgram
from matplotlib import pyplot as plt
from utils.config import *
from utils import wordcloud, keywords, summary_functions

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

st.subheader("WordCloud")
if uploaded_file is not None:
    audio_transcript = asyncio.run(get_inference(uploaded_file.getvalue()))
    wordcloud = wordcloud.wordcloud_generator(audio_transcript)
    fig = plt.figure()
    plt.imshow(wordcloud)
    plt.axis("off")
    st.pyplot(fig)

    if analysis_mode == 'Lecture':
        st.subheader("Summary")
        num_sentences = st.slider('Please select number of sentences', 1, 10)
        summarised_text = summary_functions.generate_summary(num_sentences,audio_transcript)
        st.write(summarised_text)
        
        st.subheader("Keywords Extraction")
        keywords = keywords.extract_keywords(audio_transcript)
        st.write(keywords)
    