import csv
from bs4 import BeautifulSoup
from datetime import datetime
import requests
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

client_id = 'MzgxNDIyODB8MTY5OTUwNTU5OS4xNTcxMzQ1'
client_secret = '50839cdc51be2d3727106c8a68480067b86c314c73fe4b564cf8e728e15c17c2'


def scrape_seatgeek_event_prices(url):
    headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
}
    response = requests.get(url, headers=headers)
    print("Response Status Code:", response.status_code)  # Should now be 200 if User-Agent helped
    print("URL Requested:", url)  # Debugging: Confirm the URL
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service)
    driver.get(url)
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    driver.quit()

    soup = BeautifulSoup(response.content, 'html.parser')

    # Using a CSS class pattern that starts with the given string for prices
    price_class_start = 'PriceProminentListingInfo__Price'
    prices = soup.find_all('span', class_=lambda x: x and x.startswith(price_class_start))

    print("Found price elements:", len(prices))  # Debugging: How many price elements were found

    data = []
    for price in prices:
        price_text = price.get_text(strip=True)
        print("Price Found:", price_text)  # Debugging: Output each found price

        # Only add to data if price_text is not empty
        if price_text:
            data.append({
                'Price': price_text,
                'Scrape Date': datetime.now().strftime("%Y-%m-%d"),
                'Scrape Time': datetime.now().strftime("%H:%M:%S")
            })

    return data

def write_to_csv(data, filename):
    if not data:
        print("No data to write to CSV.")  # Debugging: Inform if there's no data
        return

    with open(filename, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=['Price', 'Scrape Date', 'Scrape Time'])
        writer.writeheader()
        writer.writerows(data)

# User input for URL
event_url = input("Enter the SeatGeek event URL: ")
event_data = scrape_seatgeek_event_prices(event_url)

# Debugging: Print the data that will be written to CSV
print("Data to be written:", event_data)

# Write data to CSV if there is data
if event_data:
    csv_filename = 'event_data.csv'
    write_to_csv(event_data, csv_filename)
    print(f"Data has been written to {csv_filename}")
else:
    print("No data was scraped.")