import streamlit as st
from textblob import TextBlob
import pandas as pd
import requests
from bs4 import BeautifulSoup

def scrape_amazon_reviews(url, num_pages=1):
    all_reviews = []
    
    for page in range(1, num_pages + 1):
        response = requests.get(url + f'?pageNumber={page}')
        soup = BeautifulSoup(response.content, 'html.parser')

        reviews = []
        for review in soup.find_all('span', class_='a-size-base review-text review-text-content'):
            reviews.append(review.get_text())

        all_reviews.extend(reviews)
    
    return all_reviews

def get_recommendation(total_sentiment_score):
    if total_sentiment_score > 0.4:
        return "Highly Recommended"
    elif total_sentiment_score > -0.4:
        return "Moderately Recommended"
    else:
        return "Not Recommended"

st.header("Sentiment Analysis and Overall Recommendation for Amazon Product Reviews")

amazon_url = st.text_input("Enter Amazon Product Review URL:")

num_pages = st.number_input("Enter Number of Pages to Scrape:", min_value=1, value=1)

if st.button("Scrape and Analyze Reviews"):
    if amazon_url:
        reviews = scrape_amazon_reviews(amazon_url, num_pages)
        reviews_df = pd.DataFrame({'Text': reviews})
        reviews_df.to_csv('amazon_reviews.csv', index=False)
        st.write(f"{len(reviews)} reviews scraped and saved to 'amazon_reviews.csv'")
        
        with st.expander("Analyze Amazon Reviews"):
            reviews_df = pd.read_csv('amazon_reviews.csv')
            
            total_sentiment_score = 0
            
            for i, review in enumerate(reviews_df['Text']):
                blob = TextBlob(review)
                sentiment_score = blob.sentiment.polarity
                total_sentiment_score += sentiment_score
            
            overall_recommendation = get_recommendation(total_sentiment_score)
            
            if len(reviews_df) > 0:
                overall_sentiment_percentage = (total_sentiment_score / len(reviews_df)) * 100
                st.write("Overall Sentiment Polarity Score (%):", round(overall_sentiment_percentage, 2))
            else:
                st.write("No reviews available.")
                
            st.write("Overall Recommendation:", overall_recommendation)
    else:
        st.write("Please enter an Amazon product review URL.")
