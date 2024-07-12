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
    
    # Strip the ID from the player name
    if '#' in player_info:
        player_info = player_info.split('#')[0].strip()
    
    # Extract additional player information
    player_info_div = soup.find('ul', class_='player-info info-list')
    player_details = {}
    membership_expired = False
    if player_info_div:
        for li in player_info_div.find_all('li'):
            li_class = li.get('class', [])
            if any(cls in li_class for cls in ['classification', 'membership-status', 'current-rating', 'career-events', 'career-wins']):
                strong_tag = li.find('strong')
                if strong_tag:
                    key = strong_tag.text.strip().replace(':', '').replace(' ', '_')
                    value = li.get_text(strip=True).replace(strong_tag.text, '').strip()
                    # Remove parentheses and anything inside them from value
                    value = value.split('(')[0].strip()
                    # Clean up the value to remove redundant prefixes
                    if key == 'Classification' or key == 'Membership_Status':
                        value = value.replace(f'{key.replace("_", " ")}:', '').strip()
                    if key == 'Current_Rating':
                        value = value.split('+')[0].split('-')[0].strip()
                    player_details[key] = value
                    if key == 'Membership_Status' and 'Expired' in value:
                        membership_expired = True
    
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
        'history_data': history_data,
        'membership_expired': membership_expired,
        **player_details  # Include additional player details in the returned dictionary
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
    active_players_data = []
    all_player_info_dict = {}
    active_player_info_dict = {}
    consolidated_data = defaultdict(lambda: defaultdict(lambda: None))
    error_messages = []
    
    if request.method == 'POST':
        form = PlayerNumberForm(request.POST)
        if form.is_valid():
            player_numbers = form.cleaned_data['player_number'].split(',')
            for player_number in player_numbers:
                player_number = player_number.strip()
                if player_number in all_player_info_dict:
                    continue  # Skip if the player data is already in the dictionary
                player_data = scrape_player_history(player_number)
                if player_data is None:
                    error_messages.append(f"Player {player_number} was not found")
                else:
                    all_player_info_dict[player_data['player_number']] = player_data['player_info']
                    players_data.append(player_data)
                    if player_data['membership_expired']:
                        error_messages.append(f"Player {player_data['player_info']} #{player_data['player_number']} has an expired PDGA membership")
                    else:
                        active_players_data.append(player_data)
                        active_player_info_dict[player_data['player_number']] = player_data['player_info']
                        for entry in player_data['history_data']:
                            date_str = entry['date'].strftime('%Y-%m-%d')
                            consolidated_data[date_str]['date'] = date_str
                            consolidated_data[date_str][player_data['player_number']] = entry['player_rating']
            plot_url = plot_player_ratings(active_players_data)
            # Sort consolidated_data by date in descending order
            consolidated_data = sorted(consolidated_data.items(), key=lambda x: x[0], reverse=True)

            # Sort players_data by Current Rating in descending order
            players_data.sort(key=lambda x: int(x.get('Current_Rating', 0)), reverse=True)
    else:
        form = PlayerNumberForm()
        plot_url = None
    
    return render(request, 'history/index.html', {
        'form': form,
        'plot_url': plot_url,
        'consolidated_data': consolidated_data,
        'all_player_info_dict': all_player_info_dict,
        'active_player_info_dict': active_player_info_dict,
        'error_messages': error_messages,
        'players_data': players_data,  # Pass the players_data to the template
        'active_players_data': active_players_data  # Pass the active_players_data to the template
    })
