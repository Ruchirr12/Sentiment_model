# -*- coding: utf-8 -*-
"""
Created on Sat Jun  3 21:29:07 2023

@author: SONE
"""

import streamlit as st
page_bg_img = f"""
<style>
[data-testid="stAppViewContainer"]{{
    background-image: url("https://www.freecodecamp.org/news/content/images/2021/06/w-qjCHPZbeXCQ-unsplash.jpg");
    }}
[data-testid="stHeader"]{{
    background-image: url("https://www.freecodecamp.org/news/content/images/2021/06/w-qjCHPZbeXCQ-unsplash.jpg");
    }}
</style>
"""
st.markdown(page_bg_img, unsafe_allow_html = True)

import nltk
import plotly.express as px
from nltk.sentiment import SentimentIntensityAnalyzer
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

nltk.download('vader_lexicon')
def analyze_sentiment(text):
    analyzer = SentimentIntensityAnalyzer()
    scores = analyzer.polarity_scores(text)
    
    if scores['compound'] > 0.05:
        return 'Positive'
    elif scores['compound'] < -0.05:
        return 'Negative'
    elif scores['compound'] >= -0.05 and scores['compound'] < 0.05:
        return 'Neutral'
    
def generate_wordcloud(text):
    wordcloud = WordCloud(width=800, height=400).generate(text)
    sns.histplot(bins=10, kde=True)
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis('off')
    st.pyplot()
    
def main():
    st.title('Sentiment Analysis App')
    
    # Input text box
    text = st.text_area('Enter some text')
    
    st.set_option('deprecation.showPyplotGlobalUse', False)

    if st.button('Analyze'):
        # Perform sentiment analysis
        sentiment = analyze_sentiment(text)
        
        # Display the result
        st.write('Sentiment:', sentiment)
        
        sentiments = SentimentIntensityAnalyzer()
        st.write('Sentiment polarity score', sentiments.polarity_scores(text))
        
        # Generate word cloud
        generate_wordcloud(text)
        

        # Plot sentiment distribution
        data = {'Sentiment': ['Positive', 'Negative', 'Neutral'],
                'Count': [0, 0, 0]}
        data['Count'][['Positive', 'Negative', 'Neutral'].index(sentiment)] = 1
        df = pd.DataFrame(data)
        
        fig = px.bar(df, x='Sentiment', y='Count', color='Sentiment',
                     labels={'Sentiment': 'Sentiment', 'Count': 'Count'})
        fig.update_layout(showlegend=False)
        st.plotly_chart(fig)
if __name__ == '__main__':
    main()