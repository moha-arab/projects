from requests import get
from pprint import PrettyPrinter

# Base URL for the Ball Don't Lie API
BASE_URL = "https://www.balldontlie.io/api/v1/"
printer = PrettyPrinter()

def get_games(date="2024-09-25"):
    """Fetches games played on a given date."""
    response = get(BASE_URL + f"games?dates[]={date}")
    
    if response.status_code != 200:
        print(f"Failed to fetch data: {response.status_code}")
        print(response.text)  # Print the response content for debugging
        return
    
    try:
        games = response.json()['data']
    except ValueError:
        print("Response content is not valid JSON")
        print(response.text)  # Print the raw response text
        return

    for game in games:
        home_team = game['home_team']
        away_team = game['visitor_team']
        home_score = game['home_team_score']
        away_score = game['visitor_team_score']
        status = game['status']

        print("------------------------------------------")
        print(f"{home_team['full_name']} vs {away_team['full_name']}")
        print(f"{home_score} - {away_score}")
        print(f"Status: {status}")

def get_team_stats():
    """Fetches team stats leaders."""
    response = get(BASE_URL + "stats?per_page=100")
    
    if response.status_code != 200:
        print(f"Failed to fetch data: {response.status_code}")
        print(response.text)  # Print the response content for debugging
        return
    
    try:
        stats = response.json()['data']
    except ValueError:
        print("Response content is not valid JSON")
        print(response.text)  # Print the raw response text
        return

    # Filter and sort teams by points per game (ppg)
    teams = {}
    for stat in stats:
        team_id = stat['team']['id']
        team_name = stat['team']['full_name']
        ppg = stat['pts']

        if team_name not in teams:
            teams[team_name] = {'team_id': team_id, 'ppg': ppg, 'games': 1}
        else:
            teams[team_name]['ppg'] += ppg
            teams[team_name]['games'] += 1

    # Calculate average points per game
    for team_name, data in teams.items():
        teams[team_name]['ppg'] /= data['games']

    # Sort teams by their ppg
    sorted_teams = sorted(teams.items(), key=lambda x: x[1]['ppg'], reverse=True)

    for i, (team_name, data) in enumerate(sorted_teams):
        print(f"{i + 1}. {team_name} - {data['ppg']:.2f} PPG")

# Example Usage
get_games()       # To get the games for the current date
get_team_stats()  # To get the team stats sorted by PPG