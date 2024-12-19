import requests
import csv
from datetime import datetime, timedelta
from get_seasons import get_seasons
from get_competitions_by_season import get_competitions_by_season
from get_match_labels import get_match_labels
from get_player_statistics import get_player_statistics

base_url = 'https://wabi-north-europe-k-primary-api.analysis.windows.net/public/reports/querydata'
headers = {
    'Accept': 'application/json, text/plain, */*',
    'Accept-Language': 'en-US,en;q=0.9',
    'Content-Type': 'application/json;charset=UTF-8',
    'Origin': 'https://app.powerbi.com',
    'Referer': 'https://app.powerbi.com/',
    'X-PowerBI-ResourceKey': '47b91a6a-ce28-4401-b2fb-484df6a15a2f',
    'RequestId': '86bd878e-bb5c-66fd-0569-5f3aa4f91389',
    'ActivityId': '7534df4e-7d32-47eb-be49-05677cd597b1'
}
params = {
    'synchronous': 'true'
}

def main():
    # 1. Get all seasons
    seasons_response = get_seasons(base_url, headers)

    # Extract seasons from the response
    seasons = []
    try:
        dsr = seasons_response['results'][0]['result']['data']['dsr']
        for item in dsr['DS'][0]['PH'][0]['DM0']:
            seasons.append(item['G0'])
        print(f"Available seasons: {seasons}")
    except Exception as e:
        print(f"Error extracting seasons: {e}")
    print("\nAvailable seasons:")
    for i, season in enumerate(seasons, 1):
        print(f"{i}. {season}") 
    
    # Select a season
    season_idx = int(input("\nSelect season (enter number): ")) - 1
    selected_season = seasons[season_idx]
    
    # 2. Get competitions for selected season with date filter
    competitions = get_competitions_by_season(base_url, headers, selected_season)
    print("\nAvailable competitions:")
    for i, comp in enumerate(competitions, 1):
        print(f"{i}. {comp}")
        
    # Select a competition
    comp_idx = int(input("\nSelect competition (enter number): ")) - 1
    selected_competition = competitions[comp_idx]
    
    # Get date range from user
    print("\nEnter date range (YYYY-MM-DD format):")
    start_date = input("Start date: ")
    end_date = input("End date: ")
    
    # Get match labels for the date range
    matches = get_match_labels(base_url, headers, selected_season, selected_competition, start_date, end_date)
    
    print(f"\nMatches between {start_date} and {end_date}:")
    for i, match in enumerate(matches, 1):
        home_team, away_team = match['teams']
        print(f"{i}. {home_team} vs {away_team}")
    
    # Let user select a specific match
    if matches:
        match_idx = int(input("\nSelect match (enter number): ")) - 1
        selected_match = matches[match_idx]
        print(f"\nSelected match: {selected_match['label']}")
        print(f"Home team: {selected_match['teams'][0]}")
        print(f"Away team: {selected_match['teams'][1]}")
        
        # Get player statistics for the selected match
        players = get_player_statistics(base_url, headers, selected_season, selected_competition, start_date, end_date, selected_match['label'])
        
        with open('player_stats.csv', 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=[
                'Player Name', 'Team', 'Playing Time', 'Distance', 'HS Distance', 'HS Runs',
                'Sprint Distance', 'Sprints', 'Max Speed', 'Timestamp', 'Period', 'HI Distance'
            ])
            writer.writeheader()
            writer.writerows(players)

main()
