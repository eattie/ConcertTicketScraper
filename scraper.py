import requests
from bs4 import BeautifulSoup

url = 'https://www.seatgeek.com'
response = requests.get(url)
soup = BeautifulSoup(response.content, 'html.parser')
events = soup.find_all('class_or_id_related_to_events')
for event in events: