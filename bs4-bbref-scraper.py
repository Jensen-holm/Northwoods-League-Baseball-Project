#%% """ Beautiful Soup BBREF Crawler """
''' Libraries '''
from bs4 import BeautifulSoup
import pandas as pd
import requests
from tqdm import tqdm
#%% """ General Functions """

class scrape_baseball_reference():

  def __init__(self):
    print("SCRAPING OPTIONS:")
    print("Pass a dictionary of League year id's to get_league_player_background_history(dictoinary_of_league_year_ids = ___ )")
    print("")
    print("Pass a URL to find_data(url) to get any specific players baseline statistics")
    print("")
    print("Pass your list of parsed data to check() the total number of years and players you scraped")

  # General scraping functions
  def find_data(self, url):
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
      player_data.append(self.find_data('https://www.baseball-reference.com' + link))

    # add unique id numbers for each player since we didnt scrape names
    id_num = 0
    for player in player_data:
        player["ID"] = id_num 
        id_num += 1
    return player_data

  def get_league_player_background_history(self, dictionary_of_year_ids):
    print("Parsing League History from Baseball Reference...")
    self.lg_background_plyrs = [self.league_year_player_data(year) for year in dictionary_of_year_ids.values()]
    return self.lg_background_pyrs
  # Use this function to make sure we crawled all the right data
  def check(self, list_of_league_data):
    players = 0
    for year in list_of_league_data:
      players += len(year)
    print(f'Number of years scraped: {len(list_of_league_data)}')
    print(f'Total number of scraped players: {players}')

  # Cleaning
  def concat(self, list_of_parsed_league_data):
    self.mooshed_data = [pd.concat(year) for year in list_of_parsed_league_data[1:]]
    return self.mooshed_data



#%% """ EXAMPLE """
# dict of team id's for desired league by year
nwl_yearid_dict = {2021:'f5c87b08',2020:'78f2935d',
                   2019:'817f5f93',2018:'6a2b88b5',
                   2017:'c290e2ac',2016:'b33681e2',2015:'1671dc07'}

Northwoods_league = scrape_baseball_reference()
Northwoods_league_Data = Northwoods_league.get_league_player_background_history(nwl_yearid_dict)

#%% Cleaning 
Northwoods_league.check(Northwoods_league_Data)
Northwoods_league.concat()