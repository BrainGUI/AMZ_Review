import pandas as pd
import nltk
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer, WordNetLemmatizer
import string
import re

# Download NLTK resources
nltk.download('stopwords')
nltk.download('wordnet')

# Function to clean text data
def clean_text(text):
    # Normalize text (convert to lowercase)
    text = text.lower()

    # Remove Unicode characters
    text = text.encode('ascii', 'ignore').decode()

    # Remove punctuation
    text = re.sub('[%s]' % re.escape(string.punctuation), '', text)

    return text

# Function to process a single review
def process_review(review):
    # Tokenize and remove stopwords
    stop_words = set(stopwords.words('english'))
    words = nltk.word_tokenize(review)
    words = [word for word in words if word.lower() not in stop_words]

    # Perform stemming
    porter_stemmer = PorterStemmer()
    words = [porter_stemmer.stem(word) for word in words]

    # Perform lemmatization
    lemmatizer = WordNetLemmatizer()
    words = [lemmatizer.lemmatize(word) for word in words]

    # Join the processed words back into a sentence
    cleaned_review = ' '.join(words)

    return cleaned_review

# Function to process a CSV file containing reviews
def process_csv(input_file, output_file):
    # Read the CSV file into a Pandas DataFrame
    df = pd.read_csv(input_file)

    # Clean the 'Reviews' column using the process_review function
    df['cleaned_review'] = df['Reviews'].apply(lambda x: process_review(clean_text(str(x))))

    # Save the cleaned data to a new CSV file
    df[['ASIN', 'cleaned_review']].to_csv(output_file, index=False)

# Entry point of the script
if __name__ == "__main__":
    # Replace 'input.csv' and 'output.csv' with your file names
    input_file_path = 'reviews.csv'
    output_file_path = 'cleaned_reviews.csv'

    # Call the process_csv function to clean and process the input CSV file
    process_csv(input_file_path, output_file_path)
