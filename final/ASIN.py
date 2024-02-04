import requests
from bs4 import BeautifulSoup
import csv

# Function to retrieve Amazon ASIN numbers based on a search query
def get_amazon_asin(search_query, num_pages=1, items_per_page=48):
    # Base URL for Amazon
    base_url = "https://www.amazon.com"
    # List to store ASIN numbers
    asin_list = []

    # Headers to mimic a user's request 
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Accept-Language': 'en-US,en;q=0.9',
    }

    try:
        # Loop through specified number of search result pages
        for page in range(1, num_pages + 1):
            # Construct the search URL for the current page
            search_url = f"{base_url}/s?k={search_query}&page={page}"

            # Send a GET request to Amazon search results page with headers
            response = requests.get(search_url, headers=headers)
            response.raise_for_status()

            # Parse the HTML content of the page using BeautifulSoup
            soup = BeautifulSoup(response.text, 'html.parser')

            # Find ASIN numbers in the search results using the 'data-asin' attribute
            results = soup.find_all('div', {'data-asin': True})
            for result in results:
                asin = result['data-asin']
                asin_list.append(asin)

            # Break if there are no more results
            if not results:
                break

    except requests.exceptions.RequestException as e:
        # Handle request exceptions, if any
        print(f"Error: {e}")

    # Return ASIN numbers, limited to the specified number of pages and items per page
    return asin_list[:num_pages * items_per_page]

# Function to save ASIN numbers to a CSV file
def save_asin_to_csv(search_query, asin_numbers):
    # Create a CSV file with the search query in the filename
    filename = f"ASIN.csv"
    
    # Exclude empty ASIN values
    non_empty_asin_numbers = [asin for asin in asin_numbers if asin]
    
    # Write ASIN numbers to the CSV file
    with open(filename, 'w', newline='', encoding='utf-8') as csv_file:
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow(['ASIN'])
        csv_writer.writerows([[asin] for asin in non_empty_asin_numbers])

# Main program execution
if __name__ == "__main__":
    # Example usage:
    search_query = "monitor"
    num_pages = 20
    items_per_page = 16
    
    # Get ASIN numbers based on the search query and parameters
    asin_numbers = get_amazon_asin(search_query, num_pages=num_pages, items_per_page=items_per_page)

    # Check if ASIN numbers were retrieved successfully
    if asin_numbers:
        print("ASIN numbers:")
        for asin in asin_numbers:
            print(asin)
        
        # Save ASIN numbers to a CSV file
        save_asin_to_csv(search_query, asin_numbers)
        print(f"ASIN numbers saved to ASIN.csv")
    else:
        print("Failed to retrieve ASIN numbers.")
