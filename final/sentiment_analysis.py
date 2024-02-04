import pandas as pd
from nltk.sentiment.vader import SentimentIntensityAnalyzer

# Download NLTK data (uncomment the line below if not already downloaded)
import nltk
nltk.download('vader_lexicon')

# Function to perform sentiment analysis on a given text
def analyze_sentiment(text):
    # Create a SentimentIntensityAnalyzer instance
    sid = SentimentIntensityAnalyzer()
    
    # Get sentiment scores for the input text
    sentiment_scores = sid.polarity_scores(text)
    
    # Classify the sentiment based on the compound score
    if sentiment_scores['compound'] >= 0.05:
        return 'Positive'
    elif sentiment_scores['compound'] <= -0.05:
        return 'Negative'
    else:
        return 'Neutral'

# Function to perform sentiment analysis on a CSV file containing cleaned reviews
def perform_sentiment_analysis(input_csv, output_csv):
    # Read the CSV file into a Pandas DataFrame
    df = pd.read_csv(input_csv)
    
    # Perform sentiment analysis on the 'cleaned_review' column
    df['sentiment'] = df['cleaned_review'].apply(analyze_sentiment)
    
    # Save the results to a new CSV file
    df.to_csv(output_csv, index=False)

# Entry point of the script
if __name__ == "__main__":
    # Replace 'input_file.csv' and 'output_file.csv' with your file names
    input_file = 'cleaned_reviews.csv'
    output_file = 'sentiment.csv'
    
    # Call the perform_sentiment_analysis function to analyze sentiments and save results
    perform_sentiment_analysis(input_file, output_file)
    print(f"Sentiment analysis completed. Results saved to '{output_file}'.")
