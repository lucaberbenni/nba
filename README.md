# nba
web scraping with nba_api to make prediction of future games.

1. **games_df():**
   This function scrapes NBA league games data and appends it to a DataFrame. The data is then saved as a CSV file named "league_games.csv". It can be useful for analyzing and exploring NBA game statistics.

2. **active_player_stats():**
   This function scrapes career statistics for every active NBA player and saves the data as a CSV file named "player_stats.csv". By iterating through each active player, it retrieves their career stats using the NBA API. This data can be used to analyze player performance, compare players, or generate insights.

3. **box_df():**
   This function scrapes advanced statistics for every NBA game of every NBA team. It creates a DataFrame containing the box scores and saves it as a CSV file named "box_score.csv". By iterating through each game, it retrieves advanced box score data using the NBA API. These advanced statistics provide deeper insights into game performance.
