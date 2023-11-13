from bs4 import BeautifulSoup
import time
import requests

client_id = 'MzgxNDIyODB8MTY5OTUwNTU5OS4xNTcxMzQ1'
client_secret = '50839cdc51be2d3727106c8a68480067b86c314c73fe4b564cf8e728e15c17c2'


def scrape_seatgeek_event(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    # Example: Extracting the event title and date
    title = soup.select_one('h1.event-title').get_text(strip=True) if soup.select_one('h1.event-title') else 'N/A'
    date = soup.select_one('time').get_text(strip=True) if soup.select_one('time') else 'N/A'

    # Prepare data for CSV
    data = {
        'Title': title,
        'Date': date
    }

    return data

def write_to_csv(data, filename):
    with open(filename, 'w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=data.keys())
        writer.writeheader()
        writer.writerow(data)

# User input for URL
event_url = input("Enter the SeatGeek event URL: ")
event_data = scrape_seatgeek_event(event_url)

# Write data to CSV
csv_filename = 'event_data.csv'
write_to_csv(event_data, csv_filename)
print(f"Data has been written to {csv_filename}")