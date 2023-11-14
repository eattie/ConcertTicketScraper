import csv
from bs4 import BeautifulSoup
from datetime import datetime
import requests
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

client_id = 'MzgxNDIyODB8MTY5OTUwNTU5OS4xNTcxMzQ1'
client_secret = '50839cdc51be2d3727106c8a68480067b86c314c73fe4b564cf8e728e15c17c2'


def scrape_seatgeek_event_prices(url):
    options = Options()
    # Specify the path to your 'User Data' directory, not including the 'Profile 1' folder
    options.add_argument("user-data-dir=/Users/etai/Library/Application Support/Google/Chrome")
    # Now add the profile directory
    options.add_argument("profile-directory=Profile 1")

    # Initialize the Chrome driver with the specified options
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    
    driver.get(url)
    

    # Wait for the user to manually solve the CAPTCHA and then press Enter in the console
    input("Please solve the CAPTCHA and then press Enter here in the script...")
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "some-class-indicating-captcha-is-solved"))
    )

    soup = BeautifulSoup(driver.page_source, 'html.parser')

    # Scrape the concert name
    concert_name_element = soup.find('h1', class_='Typography__Text3-sc-1cd42027-8')
    concert_name = concert_name_element.get_text(strip=True) if concert_name_element else 'Concert name not found'

    # Scrape the section
    section_element = soup.find('p', {'data-testid': 'section'})
    section = section_element.get_text(strip=True) if section_element else 'Section not found'

    # Scrape prices
    price_class_start = 'PriceProminentListingInfo__Price'
    prices = soup.find_all('span', class_=lambda x: x and x.startswith(price_class_start))

    print("Found price elements:", len(prices))

    data = []
    for price in prices:
        price_text = price.get_text(strip=True)
        print("Price Found:", price_text)

        if price_text:
            data.append({
                'Concert Name': concert_name,
                'Section': section,
                'Price': price_text,
                'Scrape Date': datetime.now().strftime("%Y-%m-%d"),
                'Scrape Time': datetime.now().strftime("%H:%M:%S")
            })

    driver.quit()  # Close the driver after scraping
    return data


def write_to_csv(data, filename):
    if not data:
        print("No data to write to CSV.")
        return

    with open(filename, mode='w', newline='', encoding='utf-8') as file:
        fieldnames = ['Concert Name', 'Section', 'Price', 'Scrape Date', 'Scrape Time']
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        for row in data:
            writer.writerow(row)

event_url = input("Enter the SeatGeek event URL: ")
event_data = scrape_seatgeek_event_prices(event_url)

print("Data to be written:", event_data)

if event_data:
    csv_filename = 'event_data.csv'
    write_to_csv(event_data, csv_filename)
    print(f"Data has been written to {csv_filename}")
else:
    print("No data was scraped.")