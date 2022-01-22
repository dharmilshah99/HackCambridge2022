from wordcloud import WordCloud


def wordcloud_generator(audio_transcript):
    """Generate wordcloud image."""
    wordcloud_image = WordCloud(
        background_color="white"
    ).generate(audio_transcript)
    print(wordcloud_image)
    return wordcloud_image