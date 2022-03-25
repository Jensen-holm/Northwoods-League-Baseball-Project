#%% """ BS4 Baseball Reference Crawler py """
""" Libraries """
from bs4 import BeautifulSoup
from tqdm import tqdm
import pandas as pd
import requests
import sqlite3

#%% """ Class """

""" Baseball Reference Crawler Class Object """

class scrape_baseball_reference():

    def __init__(self):
        print(" --- Scrape the Baseball Reference Register ---")

    # General scraping functions
    def find_first_table_data(self, url):
        return pd.read_html(url)[0]

    def sewp(self, url):
        webpage = requests.get(url)
        return BeautifulSoup(webpage.text, features = 'lxml')

    def find_links(self, url):
        html = self.sewp(url)
        href_tags = html.find_all(href = True)
        return [tag.get('href') for tag in href_tags]

    # Baseball reference specific functions
    def get_player_background_data(self, league_year_id):
        league_links = self.find_links('https://www.baseball-reference.com/register/league.cgi?id=' + league_year_id)
        # Find team links
        team_links = []
        for href in league_links:
            if '/register/team.cgi?' in href:
                team_links.append(href)
        # scrape the team links for the player links
        links_from_team = []
        for href in team_links:
            links_from_team.append(self.find_links('https://www.baseball-reference.com' + href))
        # Append relevant links to list
        player_links = []
        for href in links_from_team:
            for link in href:
                if '/register/player.fcgi?id=' in link:
                    player_links.append(link)
        # Get rid of duplicates
        player_links = list(set(player_links))
        # finish by Returning the player data to a list
        player_data = []
        for link in tqdm(player_links):
            player_data.append(self.find_first_table_data('https://www.baseball-reference.com' + link))
        # add unique id numbers for each player since we didnt scrape names
        id_num = 0
        for player in player_data:
            player["ID"] = id_num 
            id_num += 1
        return player_data

    def get_league_player_background_history(self, dictionary_of_year_ids):
        print("\n --- Parsing Player Background Data by Year ---")
        self.lg_background_players = [self.get_player_background_data(year) for year in dictionary_of_year_ids.values()]
        return self.lg_background_players
        
    # Use this function to make sure we crawled all the right data
    def check(self, list_of_league_data):
        players = 0
        for year in list_of_league_data:
            players += len(year)
            print(f'Number of years scraped: {len(list_of_league_data)}')
            print(f'Total number of scraped players: {players}')

  # Cleaning (had to index the list to concat b/c first parsed year is empty for some reason)
  # All of these cleaning functions are currently specific to the Northwoods League Data.
    def flip_my_data(self, list_of_parsed_league_data):
        mooshed_data_by_year = [pd.concat(year) for year in list_of_parsed_league_data[1:]]
        flat_list = []
        for year in mooshed_data_by_year:
            flat_list.append(year)
        self.all_data = pd.concat(flat_list)
        return self.flip(self.all_data)
    
    def flip(self, df):
        ncaa = df[df["Lev"] == "NCAA"]
        naia = df[df["Lev"] == "NAIA"]
        nwds = df[df["Lg"] == "NWDS"]
        college = pd.concat([ncaa, naia], ignore_index = True)
        flipped = pd.merge(left = college, right = nwds, on = ["Year", "ID"])
        return flipped

    # sqlite function(s)
    def move_to_sql(self, df, data_base_name, table_name):
        print(f" --- Moved Data To Local sqlite3 Database ({data_base_name}, {table_name}) ---")
        self.conn = sqlite3.connect(data_base_name + ".db")
        self.cur = self.conn.cursor()
        return df.to_sql(name = table_name, con = self.conn, if_exists = "replace")
    
    def end_sql(self):
        return self.conn.close()
