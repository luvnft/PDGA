# history/views.py

import requests
from bs4 import BeautifulSoup
from django.shortcuts import render
from .forms import PlayerNumberForm
import matplotlib.pyplot as plt
import io
import urllib, base64
from datetime import datetime
from collections import defaultdict

def scrape_player_history(player_number):
    url = f'https://www.pdga.com/player/{player_number}/history'
    response = requests.get(url)
    if response.status_code != 200:
        return None
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Extract player information directly from the h1 tag
    h1_tag = soup.find('h1')
    player_info = h1_tag.text.strip() if h1_tag else 'N/A'
    
    table = soup.find('table', id='player-results-history')
    history_data = []
    if table:
        for row in table.find('tbody').find_all('tr'):
            date_td = row.find('td', class_='date')
            player_rating_td = row.find('td', class_='player-rating')
            round_td = row.find('td', class_='round')
            if date_td and player_rating_td and round_td:
                history_data.append({
                    'date': datetime.strptime(date_td.text.strip(), '%d-%b-%Y'),
                    'player_rating': int(player_rating_td.text.strip()),  # Ensure player_rating is an integer
                    'round': round_td.text.strip()
                })
    
    return {
        'player_info': player_info,
        'player_number': player_number,
        'history_data': history_data
    }

def plot_player_ratings(players_data):
    plt.figure(figsize=(10, 6))
    colors = ['b', 'g', 'r', 'c', 'm', 'y', 'k', 'orange', 'purple', 'pink', 'brown', 'gray']
    
    for idx, player in enumerate(players_data):
        if player['history_data']:  # Only plot if there is history data
            history_data = sorted(player['history_data'], key=lambda x: x['date'])
            dates = [entry['date'] for entry in history_data]
            ratings = [entry['player_rating'] for entry in history_data]
            color = colors[idx % len(colors)]
            plt.plot(dates, ratings, marker='o', color=color, label=player['player_info'])
    
    plt.xlabel('Date')
    plt.ylabel('Player Rating')
    plt.title('Player Ratings Over Time')
    plt.legend()
    plt.xticks(rotation=45)
    plt.ylim(750, None)  # Set the minimum y-axis limit to 750
    plt.axhline(850, color='gray', linestyle='--', linewidth=1)  # Add a gray dashed line at rating 850
    plt.tight_layout()
    
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    string = base64.b64encode(buf.read())
    uri = urllib.parse.quote(string)
    
    return uri

def index(request):
    players_data = []
    consolidated_data = defaultdict(lambda: defaultdict(lambda: None))
    player_info_dict = {}
    error_messages = []
    if request.method == 'POST':
        form = PlayerNumberForm(request.POST)
        if form.is_valid():
            player_numbers = form.cleaned_data['player_number'].split(',')
            for player_number in player_numbers:
                player_number = player_number.strip()
                player_data = scrape_player_history(player_number)
                if player_data is None:
                    error_messages.append(f"Player {player_number} was not found")
                    player_info_dict[player_number] = None
                else:
                    player_info_dict[player_data['player_number']] = player_data['player_info']
                    players_data.append(player_data)
                    for entry in player_data['history_data']:
                        date_str = entry['date'].strftime('%Y-%m-%d')
                        consolidated_data[date_str]['date'] = date_str
                        consolidated_data[date_str][player_data['player_number']] = entry['player_rating']
            plot_url = plot_player_ratings(players_data)
            # Sort consolidated_data by date in descending order
            consolidated_data = sorted(consolidated_data.items(), key=lambda x: x[0], reverse=True)
    else:
        form = PlayerNumberForm()
        plot_url = None
    
    return render(request, 'history/index.html', {
        'form': form,
        'plot_url': plot_url,
        'consolidated_data': consolidated_data,
        'player_info_dict': player_info_dict,
        'error_messages': error_messages
    })
