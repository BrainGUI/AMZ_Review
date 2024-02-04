import requests
from bs4 import BeautifulSoup
import csv

# Function to retrieve Amazon reviews based on ASIN
def get_amazon_reviews(asin):
    # Construct the URL for the Amazon product reviews page
    url = f'https://www.amazon.com/product-reviews/{asin}'
    
    # Headers to mimic a user's request
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    }

    # Send a GET request to the Amazon product reviews page
    response = requests.get(url, headers=headers)

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Parse the HTML content of the page using BeautifulSoup
        soup = BeautifulSoup(response.content, 'html.parser')
        reviews = []

        # Adjust the CSS selector based on the structure of the Amazon product page
        review_elements = soup.select('.review-text-content')

        # Extract text content of each review element
        for review_element in review_elements:
            review = review_element.get_text(strip=True)
            reviews.append(review)

        return reviews
    else:
        # Print an error message if the request fails
        print(f"Failed to retrieve reviews for ASIN {asin}. Status code: {response.status_code}")
        return None

# Main function to process input CSV and retrieve reviews for each ASIN
def main(input_csv_path, output_csv_path):
    # Read ASINs from the input CSV file
    with open(input_csv_path, 'r') as input_file:
        reader = csv.reader(input_file)
        asins = [row[0] for row in reader]

    # Dictionary to store ASINs and their corresponding reviews
    all_reviews = {}

    # Loop through each ASIN and retrieve reviews
    for asin in asins:
        reviews = get_amazon_reviews(asin)
        if reviews:
            all_reviews[asin] = reviews

    # Write ASINs and their reviews to the output CSV file
    with open(output_csv_path, 'w', newline='', encoding='utf-8') as output_file:
        writer = csv.writer(output_file)
        writer.writerow(['ASIN', 'Reviews'])

        for asin, reviews in all_reviews.items():
            writer.writerow([asin, '\n'.join(reviews)])

# Entry point of the script
if __name__ == '__main__':
    # Replace these paths with your actual input and output CSV file paths
    input_csv_path = 'ASIN.csv'
    output_csv_path = 'reviews.csv'
    
    # Call the main function to retrieve reviews and save them to the output CSV file
    main(input_csv_path, output_csv_path)
