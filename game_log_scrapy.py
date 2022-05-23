from bs4 import BeautifulSoup
import pandas as pd
import requests 
from tqdm import tqdm

def sewp(url):
  html = requests.get(url)
  return BeautifulSoup(html.text, features = 'lxml')

def links(url):
  html = sewp(url)
  hrefs = [a['href'] for a in html.find_all('a', href = True)]
  return hrefs

def get_player_links(url):
  alphabet = [link for link in links(url) if 'menu_players_alphabetically' in link]
  link = ['http://northwoods.bbstats.pointstreak.com/textstats/' + letter for letter in alphabet]
  
  players = []
  for i in link:
    players.append(links(i))
  
  plyrs = []
  for letter in players:
    for href in letter:
      if 'player_game_log' in href:
        plyrs.append(href)
  
  return plyrs

def get_player_data(year_url):
  prefix = 'http://northwoods.bbstats.pointstreak.com/textstats/'
  player_links = get_player_links(year_url)
  print('\nrequesting html data from each player site... ')
  soup = [sewp(prefix + player) for player in player_links]
  player_stats_strings = [player.find_all('p') for player in tqdm(soup)]
  return player_stats_strings

# manually find all the years we want to get data from 
year_url_list = [
                 'http://northwoods.bbstats.pointstreak.com/textstats/menu_players_alphabetically.html?seasonid=31974',
                 'http://northwoods.bbstats.pointstreak.com/textstats/menu_players_alphabetically.html?seasonid=31293',
                 'http://northwoods.bbstats.pointstreak.com/textstats/menu_players_alphabetically.html?seasonid=30702',
                 'http://northwoods.bbstats.pointstreak.com/textstats/menu_players_alphabetically.html?seasonid=29992',
                 'http://northwoods.bbstats.pointstreak.com/textstats/menu_players_alphabetically.html?seasonid=29211',
                 'http://northwoods.bbstats.pointstreak.com/textstats/menu_players_alphabetically.html?seasonid=28661',
                 'http://northwoods.bbstats.pointstreak.com/textstats/menu_players_alphabetically.html?seasonid=23677',
                 'http://northwoods.bbstats.pointstreak.com/textstats/menu_players_alphabetically.html?seasonid=12218',
                 'http://northwoods.bbstats.pointstreak.com/textstats/menu_players_alphabetically.html?seasonid=504',
                 'http://northwoods.bbstats.pointstreak.com/textstats/menu_players_alphabetically.html?seasonid=155',
                 'http://northwoods.bbstats.pointstreak.com/textstats/menu_players_alphabetically.html?seasonid=120'
]

def get_all_player_data():
  return [get_player_data(year) for year in tqdm(year_url_list)]

uncleaned_txt = get_all_player_data()

txt = []
for letter in uncleaned_txt:
  for player in letter:
    txt.append(player[0].text)

def clean_all(dirty_list):
  strings = [player.split('\n') for player in dirty_list]

  batting_dataframes = []
  pitching_dataframes = []
  for player in strings:
    name = player[1].replace(' ', '').replace('\r', '')
    batting_gl = player[player.index('BATTING GAME LOG                                                                       \r') + 2:player.index('BATTING TOTALS                                                                         \r') - 2]
    pitching_gl = player[player.index('PITCHING GAME LOG                                                                      \r') + 2:player.index('PITCHING TOTALS                                                                        \r') - 2]
    split_rows_bat = [row.split() for row in batting_gl]
    split_rows_pit = [row.split() for row in pitching_gl]

    bat_df = pd.DataFrame(split_rows_bat)
    pit_df = pd.DataFrame(split_rows_pit)

    pit_df['Name'] = name
    bat_df['Name'] = name

    if len(split_rows_bat) > 0 and len(split_rows_pit) > 0:
      batting_dataframes.append(bat_df)
      pitching_dataframes.append(pit_df)
    elif len(split_rows_bat) > 0 and len(split_rows_pit) == 0:
      batting_dataframes.append(bat_df)
    elif len(split_rows_bat) == 0 and len(split_rows_pit) > 0:
      pitching_dataframes.append(pit_df)

  return pd.concat(batting_dataframes), pd.concat(pitching_dataframes)

bat, pit = clean_all(txt)

bat.to_csv('/home/jensen/Documents/Projects/kzoo/bat_game_logs.csv')
pit.to_csv('/home/jensen/Documents/Projects/kzoo/pit_game_logs.csv')
