import streamlit as st
from PIL import Image
import instaloader
from nltk.sentiment import SentimentIntensityAnalyzer
import nltk
nltk.download('vader_lexicon')

sia = SentimentIntensityAnalyzer()

def analyze_sentiment(comment):
    sentiment_scores = sia.polarity_scores(comment)
    return sentiment_scores

def display_sentiment_chart(commentslst):
    sentiments = []
    for comment in commentslst:
        sentiment_scores = analyze_sentiment(comment)
        sentiments.append(sentiment_scores)

    # Prepare data for the chart
    data = {
        'Positive': [sentiment['pos'] for sentiment in sentiments],
        'Negative': [sentiment['neg'] for sentiment in sentiments],
        'Neutral': [sentiment['neu'] for sentiment in sentiments]
    }

    # Display the bar chart
    st.bar_chart(data)

def display_sentiment_summary(commentslst):
    num_comments = len(commentslst)
    positive_count = 0
    neutral_count = 0
    negative_count = 0

    for comment in commentslst:
        sentiment_scores = analyze_sentiment(comment)
        compound_score = sentiment_scores['compound']

        if compound_score >= 0.05:
            positive_count += 1
        elif compound_score <= -0.05:
            negative_count += 1
        else:
            neutral_count += 1

    positive_percentage = (positive_count / num_comments) * 100
    neutral_percentage = (neutral_count / num_comments) * 100
    negative_percentage = (negative_count / num_comments) * 100

    st.title("Sentiment Summary")
    st.write(f"Total Comments: {num_comments}")
    st.write(f"Positive Comments: {positive_percentage:.2f}%")
    st.write(f"Neutral Comments: {neutral_percentage:.2f}%")
    st.write(f"Negative Comments: {negative_percentage:.2f}%")

comments = []

def HomePage():
    comments.clear()  # Clear the comments list
    st.title("Get the sentimental analysis of any profile you want")
    insta_id = st.text_input("Enter the Instagram ID: ")
    if st.button("Get"):
        loader = instaloader.Instaloader()
        profile = instaloader.Profile.from_username(loader.context, insta_id)
        for post in profile.get_posts():
            post_comments = post.get_comments()
            for comment in post_comments:
                comments.append(comment.text)
        st.title("Comments")
        st.text_area(label='', value='\n'.join(comments), height=300)
        display_sentiment_chart(comments)
        display_sentiment_summary(comments)

def main_page():
    st.title("Enter the login details of your Instagram ID")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        try:
            loader = instaloader.Instaloader()
            st.write("logging in")
            loader.login(username, password)
            st.success("Logged in as {}".format(username))
            st.write("Redirecting to home page...")
            st.session_state.runpage = HomePage
            st.experimental_rerun()
        except:
            st.error("Invalid username or password")

if "runpage" not in st.session_state:
    st.session_state.runpage = main_page
st.session_state.runpage()
