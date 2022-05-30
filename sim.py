from bs4 import BeautifulSoup
from model import my_model
from tqdm import tqdm 
import pandas as pd 
import numpy as np
import requests

''' player object '''
class Player():

    def __init__(self):
        self.name = ''
        self.projection = self.rc_projection()

    ''' need to generate predictions here in a function or something '''

    def rc_projection(self):
        return prob_bat()

''' team object '''
class Team():

    def __init__(self, team_link):
        self.team_link = team_link
        self.player_links = self.get_plyr_links(self.team_link)

        spans = BeautifulSoup(requests.get(self.team_link).text, features = 'lxml').find_all('span')
        self.year = spans[8].text
        self.team_name = spans[9].text

    def get_plyr_links(self):
        html = BeautifulSoup(requests.get(self.team_link).text, features = 'lxml')
        a_tags = html.find_all('a', href = True)
        return [tag['href'] for tag in a_tags if '/player.fcgi?id=' in tag['href']]

    def scrape_player_nums(self, tm_link):
        return [Player(guy) for guy in self.player_links]


''' league object '''
class League():

    def __init__(self, lg_url = input('Enter League URL: '), year = 'recent'):
        self.lg_name = ''
        self.links = self.tm_links(lg_url)
        self.teams = [Team(link) for link in self.links]

    def team_links(self, lg_url):
        html = BeautifulSoup(requests.get(lg_url).text, features = 'lxml')
        a_tags = html.find_all('a', href = True)
        all_tm_links = [tag['href'] for tag in a_tags if '/team.cgi?id=' in tag['href']]
        return all_tm_links

    def generate_teams(self):
        return [Team('https://baseball-reference.com' + link) for link in self.links]
        


''' game object '''
class PlayBall():

    def __init__(self, league_url):
        self.teams = League(league_url).teams

        # print a list of options for teams to chose from 
        for i in range(len(self.teams)):
            print(self.teams[i].team_name)
        
        # prompt user to choose teams
        home = input('Enter Home team: ')
        away = input('Enter Away team: ')
        self.num_games = int(input('Enter Number of games: '))
        # iterate through list of team objects to find the teams
        # that have the matching team names to the ones the user chose
        self.Home = [team for team in self.teams if home == team.team_name][0]
        self.Away = [team for team in self.teams if away == team.team_name][0]

        self.games = [self.game for i in range(self.num_games)]
        
        self.results()

    def game(self):
        
        
        return 

    def results(self):
        print(f'\---- Results for {self.num_games} simulated games between the {self.Home.team_name} and the {self.Away.team_name} ----')
        print('')
