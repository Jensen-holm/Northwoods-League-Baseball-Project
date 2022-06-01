from bs4 import BeautifulSoup
from model import my_model
from model import explanatory_cols
from model import response_cols
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
        self.pred_range = self.projections()

        ''' add predicted ranges to each player dataframe '''
        for col in explanatory_cols:
            self.tbl[col + ' min'] = self.pred_range[0]
            self.tbl[col + ' max'] = self.pred_range[1]

        '''
        once each player has a range of predicted values, we will need to 
        randomly generate probabilities for each event over and over since we have
        a range of probabilities instead of a set probability for each event because of the 
        way that the model works. So, we will turn the projected numbers into probabilities that
        add up to 1, then randomly assign those probabilities based on the models predicted range.
        '''

    def sewp_stats(self):
        html = BeautifulSoup(requests.get(self.link).text, features = 'lxml')
        spans = html.find_all('span')
        p_tags = html.find_all('p')
        df = pd.read_html(self.link)[0]
        df['name'] = spans[8].text
        df['pos'] = p_tags[0].text[13:].replace('  ', '').replace('\n', '').strip()
        df['height'] = spans[9].text
        df['weight'] = spans[10].text
        df['b-day'] = spans[11].text
        return df

    def projections(self, num_deviations = 1):
        # filter the df so we project based on college numbers
        # clean it (not sure if this works rn)

        ''' need to make this condusive to naia? '''
        df = self.tbl
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
            self.tbl = df

            pred_ranges = []
            for stat in pred:
                min_ = stat - (my_model.std * num_deviations)
                max_ = stat + (my_model.std * num_deviations)
                pred_ranges.append([min_, max_])
            pred_ranges = zip(pred_ranges, response_cols)


            return pred_ranges
            # ''' export a csv containing predicted values before we turn the minto probabilities, if it already exists it will update '''

        elif len(df) < 1:
            return "No available Colligate Stats to Model off of."
        
class Team():

    def __init__(self, team_link):
        self.team_link = team_link
        self.player_links = self.get_plyr_links()
        spans = BeautifulSoup(requests.get(self.team_link).text, features = 'lxml').find_all('span')
        self.year = spans[8].text
        self.team_name = spans[9].text
        self.player_list = self.scrape_player_nums()

        # now that we have this csv of predicted values, lets predict probabilities per PA
        # somehow get it to add up to one
        self.team_df = pd.concat([plyr.tbl for plyr in self.player_list])

    def get_plyr_links(self):
        html = BeautifulSoup(requests.get(self.team_link).text, features = 'lxml')
        a_tags = html.find_all('a', href = True)
        return [('https://baseball-reference.com' + tag['href']) for tag in a_tags if '/player.fcgi?id=' in tag['href']]

    def scrape_player_nums(self):
        print(f'\n                  Projecting players on the {self.year} {self.team_name}\n')
        return [Player(guy) for guy in tqdm(self.player_links)]

class ProjectNewLeague():

    def __init__(self, lg_url = input('\nEnter League / Year URL (ignore for now): ')):

        spans = BeautifulSoup(requests.get(lg_url).text, features = 'lxml').find_all('span')
        self.lg_year = spans[8].text
        self.lg_name = spans[9].text
        print(f'\n                                   {self.lg_name}  {self.lg_year}\n')
        
        self.links = self.team_links(lg_url)
        self.teams = self.generate_teams()
        self.team_names = [team.team_name for team in self.teams]
        self.save_league()

    def team_links(self, lg_url):
        html = BeautifulSoup(requests.get(lg_url).text, features = 'lxml')
        a_tags = html.find_all('a', href = True)
        all_tm_links = [tag['href'] for tag in a_tags if '/team.cgi?id=' in tag['href']]
        return all_tm_links

    def generate_teams(self):
        return [Team('https://baseball-reference.com' + link) for link in self.links]

    def save_league(self):
        print(f'\n  Saved to csv file path: /Users/user/Documents/python-projects/kzoo/projected_leagues{self.lg_name + "_" + self.lg_year}\n')
        league_df = pd.concat([team.team_df for team in self.teams])
        league_df.to_csv(f'/Users/user/Documents/python-projects/kzoo/projected_leagues/{self.lg_name + "_" + self.lg_year}')
        
class PlayBall():

    def __init__(self, new = True):
        print("\n                       - - - - JENSEN'S SUMMER BASEBALL SIMULATOR - - - -\n")

        if new == True:
            print(f'\n                                          New League\n')
            self.teams = ProjectNewLeague(lg_url = 'https://www.baseball-reference.com/register/league.cgi?id=f5c87b08').teams
        
        if new == False:
            ''' read a csv from an old projected league '''
            print('\n       Getting old league\n')


        # print a list of options for teams to chose from 
        for i in range(len(self.teams)):
            print(f'                                    {self.teams[i].team_name}')
        
        # prompt user to choose teams
        home = input('\n                                Enter Home team: ')
        away = input('                                  Enter Away team: ')
        self.num_games = int(input('                                    Enter Number of simulated games: '))
        # iterate through list of team objects to find the teams
        # that have the matching team names to the ones the user chose
        self.Home = [team for team in self.teams if home == team.team_name][0]
        self.Away = [team for team in self.teams if away == team.team_name][0]

        self.games = [self.game for i in range(self.num_games)]
        
        self.results()

    def game(self):
        return 'game'

    def results(self):
        print(f'            ---- Results for {self.num_games} simulated games between the {self.Home.team_name} and the {self.Away.team_name} ----')
        print('                                                     simulator not finished yet.')

simulation = PlayBall(new = True)
