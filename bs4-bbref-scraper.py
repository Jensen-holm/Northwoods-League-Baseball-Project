#%% """ BS4 Baseball Reference Crawler py """
""" Libraries """
from bs4 import BeautifulSoup
from tqdm import tqdm
import pandas as pd
import requests
import sqlite3

#%% """ Class """

class scrape_baseball_reference():

    def __init__(self):
        print("SCRAPING OPTIONS:")
        print(" - Pass a dictionary of League year id's to get_league_player_background_history()")
        print(" - Pass a URL to find_data(url) to get any specific players baseline statistics")
        print(" - Pass your list of parsed data to check() the total number of years and players you scraped")
        print(" - Clean your data with the concat and flip functions")
        print(" - Export data to local sqlite3 database with moce_to_sql() or move_all_to_sql()")

    # General scraping functions
    def find_first_table_data(self, url):
        first_table = pd.read_html(url)
        return first_table[0]

    def sewp(self, url):
        webpage = requests.get(url)
        html = BeautifulSoup(webpage.text, features = 'lxml')
        return html

    def find_links(self, url):
        html = self.sewp(url)
        href_tags = html.find_all(href = True)
        href_tags = list(href_tags)
        hrefs = [tag.get('href') for tag in href_tags]
        return hrefs

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
        print("\n--- Parsing Player Background Data by Year ---")
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
    def concat(self, list_of_parsed_league_data):
        mooshed_data_by_year = [pd.concat(year) for year in list_of_parsed_league_data[1:]]
        self.mooshed_data = [pd.concat(year) for year in mooshed_data_by_year]
        return self.mooshed_data

    def flip_nwds(self, year):
        naia = year[year["Lev"] == "NAIA"]
        ncaa = year[year["Lev"] == "NCAA"]
        nwds = year[year["Lev"] == "Smr"]
        return naia, ncaa, nwds
    
    def flip_northwoods(self, list_of_parsed_data):
        self.flipped_data = [self.flip_nwds(year) for year in list_of_parsed_data]
        return self.flipped_data

    def move_to_sql(self, df, data_base_name, table_name):
        conn = sqlite3.connect(data_base_name + ".db")
        df.to_sql(name = table_name, con = conn)

    def move_all_to_sql(self, list_of_dfs, data_base_name, table_name):
        conn = sqlite3.connect(data_base_name + ".db")
        x = 0
        for year in list_of_dfs:
            year.to_sql(name = table_name + x, con = conn)
            x += 1
            table_name += str(x)
#%% """ EXAMPLE """
nwl_yearid_dict = {2021:'f5c87b08',2020:'78f2935d',
                   2019:'817f5f93',2018:'6a2b88b5',
                   2017:'c290e2ac',2016:'b33681e2',2015:'1671dc07'}

Northwoods_league = scrape_baseball_reference()
Northwoods_league_Data = Northwoods_league.get_league_player_background_history(nwl_yearid_dict)

#%% Cleaning 
print(Northwoods_league.check(Northwoods_league_Data))
Northwoods_league_Data = Northwoods_league.concat(Northwoods_league_Data)
