import requests
from bs4 import BeautifulSoup

# URL of the page to scrape
url = 'https://www.pdga.com/player/236811/history'

# Send a GET request to the page
response = requests.get(url)
response.raise_for_status()  # Check if the request was successful

# Parse the HTML content of the page
soup = BeautifulSoup(response.text, 'html.parser')

# Find the table with the specific ID
table = soup.find('table', id='player-results-history')

# Initialize lists to hold the scraped data
dates = []
player_ratings = []
rounds = []

# Iterate over each row in the table body
for row in table.find('tbody').find_all('tr'):
    date_td = row.find('td', class_='date')
    player_rating_td = row.find('td', class_='player-rating')
    round_td = row.find('td', class_='round')

    if date_td and player_rating_td and round_td:
        dates.append(date_td.text.strip())
        player_ratings.append(player_rating_td.text.strip())
        rounds.append(round_td.text.strip())

# Print the scraped data
for date, player_rating, round_ in zip(dates, player_ratings, rounds):
    print(f"Date: {date}, Player Rating: {player_rating}, Round: {round_}")
