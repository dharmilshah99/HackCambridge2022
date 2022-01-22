import streamlit as st
from deepgram import Deepgram
import asyncio, json

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
    print(json.dumps(response, indent=4))


###
# Streamlit App
###

st.set_page_config(layout="centered", page_icon="💬", page_title="Audio Cloud")
st.title("Audio Cloud")
uploaded_file = st.file_uploader(label="Upload Audio Recording", )
if uploaded_file is not None:
    asyncio.run(get_inference(uploaded_file.getvalue()))
add_selectbox = st.sidebar.selectbox(
    "How would you like to be contacted?",
    ("Email", "Home phone", "Mobile phone")
)