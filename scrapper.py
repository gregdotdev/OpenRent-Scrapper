import requests
from bs4 import BeautifulSoup
import re

def scrape_openrent():
    url = input("Enter openrent URL: ")
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Find all elements that have 'banda pt listing-title'
    listings = soup.find_all('span', class_='banda pt listing-title')

    # Creating a list to storage the data
    data = []

    for listing in listings:
        # Getting the text from tag span
        name = listing.get_text(strip=True)
        # Verifying if the text have'2 Bed Flat'
        if name.startswith('2 Bed Flat'):
            # Find the element (<div>) that contains the price
            price_div = listing.find_previous('div', class_='pim pl-title')
            # Getting the price from tag h2
            price_text = price_div.h2.get_text(strip=True)
            # Removing the (£) symbol and 'per month'
            price_text = re.sub(r'[£,]|per month', '', price_text)
            # Converting to a full price
            price = int(price_text.strip())
            # Add the name and the price to data table
            data.append((name, price))

    # Sorting data stating from the most cheap
    sorted_data = sorted(data, key=lambda x: x[1])

    # printing the data sorted
    for name, price in sorted_data:
        print(f"{name}: £{price:,} per month")

if __name__ == "__main__":
    scrape_openrent()
