# -*- coding: utf-8 -*-
"""
Created on Thu Jun  1 20:32:36 2023

@author: sone
"""

import streamlit as st
import pandas as pd
from wordcloud import WordCloud
from textblob import TextBlob
def main():
    st.title("Sentiments with Word Cloud")
    
    # Add a file uploader
    uploaded_file = st.file_uploader("Upload a text file", type=["txt"])
    
    if uploaded_file is not None:
        text = uploaded_file.read().decode("utf-8")
        sentiment = get_sentiment(text)
        
        # Filter positive, negative, and neutral sentiments
        positive_words = ' '.join(sentiment[sentiment['Sentiment'] == 'positive']['Word'].tolist())
        negative_words = ' '.join(sentiment[sentiment['Sentiment'] == 'negative']['Word'].tolist())
        neutral_words = ' '.join(sentiment[sentiment['Sentiment'] == 'neutral']['Word'].tolist())
        
        # Create word clouds
        st.subheader("Positive Sentiment")
        create_wordcloud(positive_words)
        
        st.subheader("Negative Sentiment")
        create_wordcloud(negative_words)
        
        st.subheader("Neutral Sentiment")
        create_wordcloud(neutral_words)

def get_sentiment(text):
    blob = TextBlob(text)
    sentiment = pd.DataFrame(blob.sentences, columns=['Sentence'])
    sentiment['Polarity'] = sentiment['Sentence'].apply(lambda x: TextBlob(x).sentiment.polarity)
    sentiment['Sentiment'] = sentiment['Polarity'].apply(get_sentiment_label)
    sentiment['Word'] = sentiment['Sentence'].apply(lambda x: ' '.join(TextBlob(x).words.lower()))
    return sentiment

def get_sentiment_label(polarity):
    if polarity > 0:
        return 'positive'
    elif polarity < 0:
        return 'negative'
    else:
        return 'neutral'

def create_wordcloud(words):
    wordcloud = WordCloud(width=800, height=400, background_color='white').generate(words)
    st.image(wordcloud.to_array())

if __name__ == '__main__':
    main()