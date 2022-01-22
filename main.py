import streamlit as st
import asyncio, json
import pydub
import numpy as np
from wordcloud import WordCloud
from deepgram import Deepgram
from matplotlib import pyplot as plt
from streamlit_webrtc import (
    AudioProcessorBase,
    ClientSettings,
    WebRtcMode,
    webrtc_streamer,
)

from config import *

###
# Global Variables
###
DG_CLIENT = Deepgram({"api_key": DEEPGRAM_API_KEY, "api_url": DEEPGRAM_API_URL})

###
# Helpers
###


async def get_inference(audio_bytestream):
    """Gets transcription of an audio byte stream."""
    source = {"buffer": audio_bytestream, "mimetype": "audio/wav"}
    response = await DG_CLIENT.transcription.prerecorded(source, {"punctuate": True})
    return response["results"]["channels"][0]["alternatives"][0]["transcript"]


def wordcloud_generator(audio_transcript):
    """Generate wordcloud image."""
    wordcloud_image = WordCloud(background_color="white").generate(audio_transcript)
    return wordcloud_image


def stream_audio():
    """Streams audio from Mic to WebApp"""

    webrtc_ctx = webrtc_streamer(
        key="Audio Input",
        mode=WebRtcMode.SENDONLY,
        audio_receiver_size=1024,
        rtc_configuration=ClientSettings(
            media_stream_constraints={"video": False, "audio": True},
        ),
    )

    while True:
        sound_chunk = pydub.AudioSegment.empty()
        audio_frames = webrtc_ctx.audio_receiver.get_frames(timeout=1)
        for audio_frame in audio_frames:
            sound = pydub.AudioSegment(
                data=audio_frame.to_ndarray().tobytes(),
                sample_width=audio_frame.format.bytes,
                frame_rate=audio_frame.sample_rate,
                channels=len(audio_frame.layout.channels),
            )
            sound_chunk += sound
        hehexd = sound_chunk.get_array_of_samples()
        lol = asyncio.run(get_inference(hehexd))
        print(lol)

    


    



###
# Streamlit App
###

st.set_page_config(layout="centered", page_icon="💬", page_title="Audio Cloud")
st.title("Audio Cloud")
uploaded_file = st.file_uploader(
    label="Upload Audio Recording",
)
stream_audio()
if uploaded_file is not None:
    audio_transcript = asyncio.run(get_inference(uploaded_file.getvalue()))
    wordcloud = wordcloud_generator(audio_transcript)
    fig = plt.figure()
    plt.imshow(wordcloud)
    plt.axis("off")
    st.pyplot(fig)
