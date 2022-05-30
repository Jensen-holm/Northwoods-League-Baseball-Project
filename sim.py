from bs4 import BeautifulSoup
from model import my_model
from model import explanatory_cols
from tqdm import tqdm 
import pandas as pd 
import numpy as np
import requests

'''
only need to project stats one time for each league
'''

class Player():

    def __init__(self, bbref_link):
        self.link = bbref_link
        self.tbl = self.sewp_stats()
        ''' move projection function to the league object '''

    ''' 
    once each player has a range of predicted values, we will need to 
    randomly generate probabilities for each event over and over since we have
    a range of probabilities instead of a set probability for each event because of the 
    way that the model works. So, we will turn the projected numbers into probabilities that
    add up to 1, then randomly assign those probabilities based on the models predicted range.
    '''

    def sewp_stats(self):
        return pd.read_html(self.link)[0]
        
        
class Team():

    def __init__(self, team_link):
        self.team_link = team_link
        self.player_links = self.get_plyr_links()
        self.player_stats_list = self.scrape_player_nums()
        spans = BeautifulSoup(requests.get(self.team_link).text, features = 'lxml').find_all('span')
        self.year = spans[8].text
        self.team_name = spans[9].text
        
        print(f'\n   Projecting Ranges for players on the {self.year} {self.team_name}\n')
        self.pred_ranges = [self.projections(player.tbl) for player in tqdm(self.player_stats_list)]
        

    def get_plyr_links(self):
        html = BeautifulSoup(requests.get(self.team_link).text, features = 'lxml')
        a_tags = html.find_all('a', href = True)
        return [('https://baseball-reference.com' + tag['href']) for tag in a_tags if '/player.fcgi?id=' in tag['href']]

    def scrape_player_nums(self):
        return [Player(guy) for guy in self.player_links]

    def projections(self, df, num_deviations = 1):
        # filter the df so we project based on college numbers
        ''' may need to change these filters later '''
        # clean it (not sure if this works rn)
        df = df[df['Lev'] != 'Other']
        df = df[df['Lev'] == 'NCAA']
        df = df[df['Year'] == 2022]
        df = df.apply(pd.to_numeric, errors = 'coerce').combine_first(df)

        # if they have college numbers, project them!
        if len(df) > 0:
            df['RC'] = ((df['H'] + df['BB']) * df['TB']) / df['AB'] + df['BB']

            ''' create single columns '''
            df['1b'] = df['H'] - (df['2B'] + df['3B'] + df['HR'])

            '''create in play outs columns '''
            df['inpO'] = df['PA'] - (df['H'] - df['SO'] - df['HBP'] - df['SO'] - df['BB'])
            print(df)
            pred = my_model.model.predict(df[[explanatory_cols]])
            return [[(stat - (my_model.std * num_deviations)), stat + (my_model.std * num_deviations)]for stat in pred]
            # ''' export a csv containing predicted values before we turn the minto probabilities, if it already exists it will update '''

        elif len(df) < 1:
            return None

class League():

    def __init__(self, lg_url = input('\nEnter League / Year URL (ignore for now): ')):

        spans = BeautifulSoup(requests.get(lg_url).text, features = 'lxml').find_all('span')
        self.lg_year = spans[8].text
        self.lg_name = spans[9].text
        print(f'\n  {self.lg_name}  {self.lg_year}\n')
        
        self.links = self.team_links(lg_url)
        self.teams = self.generate_teams()
        self.team_names = [team.team_name for team in self.teams]

    def team_links(self, lg_url):
        html = BeautifulSoup(requests.get(lg_url).text, features = 'lxml')
        a_tags = html.find_all('a', href = True)
        all_tm_links = [tag['href'] for tag in a_tags if '/team.cgi?id=' in tag['href']]
        return all_tm_links

    def generate_teams(self):
        return [Team('https://baseball-reference.com' + link) for link in self.links]
        
class PlayBall():

    def __init__(self):
        print("\n   - - - - JENSEN'S SUMMER BASEBALL SIMULATOR - - - -\n")
        self.teams = League(lg_url = 'https://www.baseball-reference.com/register/league.cgi?id=f5c87b08').teams

        # print a list of options for teams to chose from 
        for i in range(len(self.teams)):
            print(self.teams[i].team_name)
        
        # prompt user to choose teams
        home = input('\nEnter Home team: ')
        away = input('\nEnter Away team: ')
        self.num_games = int(input('\nEnter Number of simulated games: '))
        # iterate through list of team objects to find the teams
        # that have the matching team names to the ones the user chose
        self.Home = [team for team in self.teams if home == team.team_name][0]
        self.Away = [team for team in self.teams if away == team.team_name][0]

        self.games = [self.game for i in range(self.num_games)]
        
        self.results()

    def game(self):
        return 'game'

    def results(self):
        print(f'\---- Results for {self.num_games} simulated games between the {self.Home.team_name} and the {self.Away.team_name} ----')
        print('simulator not finished yet.')

simulation = PlayBall()
