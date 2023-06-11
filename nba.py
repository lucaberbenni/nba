import pandas as pd
import numpy as np
import requests
import time

from nba_api.stats.static import players, teams
from nba_api.stats.endpoints import playergamelog, leaguegamefinder, playercareerstats, boxscoreadvancedv2
from nba_api.stats.library.parameters import SeasonAll


def games_df():
    '''
    Fetch NBA league game data using the LeagueGameFinder class.
    Save the fetched game data as a CSV file named 'league_games.csv'.
    '''
    league_games = leaguegamefinder.LeagueGameFinder().get_data_frames()[0]
    league_games.to_csv('df/league_games.csv')

def active_player_stats():
    ''' 
    This function retrieves and combines the career statistics of active NBA players. 
    It iterates through each player, checks their active status, fetches their career stats,
    and concatenates them into a single DataFrame. The combined player statistics are then 
    saved as a CSV file named 'player_stats.csv' for further analysis.
    '''
    conc_df = pd.DataFrame()
    player_dict = players.get_players()
    for player in player_dict:
        if player['is_active'] == True:
            time.sleep(1)
            player_stats = playercareerstats.PlayerCareerStats(player_id= player['id'], timeout= 120).get_data_frames()[0]
            conc_df = pd.concat([conc_df, player_stats], axis=0, ignore_index=True)
            print(conc_df)

    conc_df.to_csv('df/player_stats.csv')

def box_df():
    '''
    This function creates a DataFrame of NBA box scores for games involving all teams in the league.
    It retrieves a dictionary of team information, extracts the team abbreviations, and fetches the
    league game data using the LeagueGameFinder class. Finally, it filters the game data to include
    only games involving the teams in the league, resulting in a DataFrame of box scores for analysis.
    '''
    team_dict = teams.get_teams()
    teams = []
    for team in team_dict:
        teams.append(team['abbreviation'])

    box_score_df =pd.DataFrame()
    league_games = leaguegamefinder.LeagueGameFinder().get_data_frames()[0]
    nba_games = league_games[league_games['TEAM_ABBREVIATION'].isin(teams)]

    for game in nba_games['GAME_ID']:
        time.sleep(0.5)
        
        box_score = boxscoreadvancedv2.BoxScoreAdvancedV2(game_id=game, timeout=120).get_data_frames()[0]
        box_score_df = pd.concat([box_score_df, box_score], ignore_index= True, axis=0)
        
        print(f"{box_score_df['GAME_ID'].nunique()}/{nba_games['GAME_ID'].nunique()}")
    box_score_df.to_csv('df/box_score.csv')

df = pd.read_csv('df/box_score.csv')
print(df)