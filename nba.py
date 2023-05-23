import pandas as pd
import numpy as np
import requests
import time

from nba_api.stats.static import players, teams
from nba_api.stats.endpoints import playergamelog, leaguegamefinder, playercareerstats, boxscoreadvancedv2
from nba_api.stats.library.parameters import SeasonAll



# gamelog_bron = playergamelog.PlayerGameLog(player_id='2544', season='2017')
# gamelog_bron_df = gamelog_bron.get_data_frames()[0]
# print(gamelog_bron_df)

# gamelog_bron_all = playergamelog.PlayerGameLog(player_id='2544', season= SeasonAll.all)
# gamelog_bron_df_all = gamelog_bron_all.get_data_frames()[0]
# print(gamelog_bron_df_all)

def games_df():
    '''
    scrape, append to a df and save it all leage games
    '''
    league_games = leaguegamefinder.LeagueGameFinder().get_data_frames()[0]
    league_games.to_csv('df/league_games.csv')

def active_player_stats():
    '''
    scrape, append to a df carrer stats of every single active player and save it as csv
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
    scrape, append to a df and save through stats of every nba games of every nba team
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