# trying to define a normal outcome distribution curve for each player based on that players modeled numbers

# plan is to model a players performance in real time, compare that with the pitcher
# then based on that output, create a distribution of probabilities based on the final number
# randomly select from said poisson distribution
import sqlite3
from modeling import rf_model
# from sim import league
import pandas as pd
import math
import requests
from bs4 import BeautifulSoup
from tqdm import tqdm
import sqlite3

''' Data '''

class league():                                                   # the unclean one is all_smr
    def __init__(self, sqlite = True, dbase = "SMR.db", table = "all_smr_clean1", nwds_filter = True, game_log_csv = '', lg_name = ''):

        self.lg_name = lg_name

        conn = sqlite3.connect(dbase)
        df = pd.read_sql_query(f"SELECT * FROM {table}", conn)

        if sqlite == False:
            df = pd.read_csv("/home/jensen/Documents/Projects/kzoo/" + table)
        elif sqlite != False and sqlite != True:
            print("Error: sqlite must equal true or false in data function.")
        self.data = df
        
        if nwds_filter == True:
            self.data = df[df["Lg_y"] == "NWDS"]

# """ Modeling """
# # import the data (no arguments means it will only be northwoods league data)
# df1 = league(nwds_filter = False, lg_name = "Summer Ball").data
# df1['RC_x'] = ((df1['H_x'] + df1['BB_x']) * df1['TB_x']) / df1['AB_x'] + df1['BB_x']
# df1['RC_y'] = ((df1['H_y'] + df1['BB_y']) * df1['TB_y']) / df1['AB_y'] + df1['BB_y']

# # filtering data
# df1 = df1[df1['RC_x'] >= 1]
# df1 = df1[df1["RC_y"] >= 1]
# df1 = df1[df1["TB_y"] >= 30]

# # build tensorflow model based on said data (going with random forest tho)
# explanatory1 = df1[["TB_x", "OPS_x", "AB_x", "SO_x", "RC_x"]]
# response1 = df1['RC_y']

# df2 = league(nwds_filter = False, lg_name = 'summer ball').data
# df2 = df2[df2['PA_x'] >= 50]
# df2 = df2[df2['PA_y'] >= 50]
# explanatory2 = df2[['TB_x', 'OPS_x', 'PA_x', 'AB_x', 'HR_x']]
# response2 = df2['PA_y']

# """ modeling both total bases and plate appearances """
# #def __init__(self, explanatory, response, dummies = False, test_size = .3, n_estimators = 100):
# _269rc = rf_model(explanatory1, response1, n_estimators = 150)
# _269pa = rf_model(explanatory2, response2, n_estimators = 150)

# # mean and std of predicted values
# murc = _269rc.mean
# stdrc = _269rc.std

# mupa = _269pa.mean
# stdpa = _269pa.std

# """ Project rosters """
# # utilize the uniformity of baseball reference
# # maybe we can project the entore league in one function. (once bbref rosters update)

# class prob_team():

# 	def __init__(self, team_bbref_url, tm_name = ''):
# 		self.team = tm_name
# 		self.hitter_tbl, self.pitcher_tbl = self.plyr_data(team_bbref_url)
# 		self.hitters = ''
# 		self.pitchers= ''
# 		self.hit_projections = [self.pred_hit(player) for player in self.players]
# 		self.pit_projectiosn = []

# 	def pred_hit(self, player_url):
# 		hit_tbl = pd.read_html(player_url)[0]
# 		player = hit_tbl[hit_tbl['#'] == self.player_number]
# 		player['RC'] = (((player["H"] + player['BB']) * player['TB']) / player["AB"] + player['BB'])
# 		player['PA'] = player['AB'] + player['BB'] + player['HBP'] + player['SF']
# 		rc_prediction = _269rc.model.predict(player[['TB', 'OPS', 'AB', 'SO', 'RC']])
# 		pa_prediction = _269pa.model.predict(player[['TB', 'OPS', 'PA', 'AB', 'HR']])

# 		rc_range = [math.floor(rc_prediction - 2*stdrc), math.ceil(rc_prediction + 2*stdrc)]
# 		pa_range = [math.floor(pa_prediction) - 2*stdpa, math.ceil(pa_prediction + 2*stdpa)]
# 		r = [rc_range[0] / pa_prediction, rc_range[1] / pa_prediction]
# 		return r, pa_range

# 	''' pitching model is pretty rough rn, might simulate against the pitchers real time numbers during the season '''
# 	def pred_pit(self, player_url):

# 		return 

# 	def plyr_data(self, url, year):
# 		prefix = 'https://baseball-reference.com'
# 		html = BeautifulSoup(requests.get(url).text, features= 'lxml')
# 		tags = html.find_all('a', href = True)
# 		plyrs = [(prefix + tag['href']) for tag in tags if '/player.fcgi?id=' in tag['href']]
# 		print('Parsing Player Tables...')
# 		tbl = pd.concat([pd.read_html(player)[0] for player in tqdm(plyrs)])
# 		yr = tbl[tbl['Year']== year]
# 		pitchers = yr[yr['IP'] >= 0]
# 		hitters = yr[yr['PA'] >= 0]
# 		return hitters, pitchers

# """ test to see if actual vlaue is in predicted rnage and tune the number of standard deviations for range """

# def pred_range(model):
# 	the_model = ''
# 	if model == 'rc':
# 		the_model = _269rc.model
# 	elif model == 'pa':
# 		the_model = _269pa.model

# 	the_model.fit(the_model.x_train, the_model.y_train)
	
# 	return 

# range_preds = zip(pred_range(_269rc.model.predict(_269rc.x_test)), _269rc.y_test)
# yes = 0 
# no = 0
# print(range_preds)

# generate predicted range on test, then see if y test is in the range
			


# print(f'{yes / no:.3f}%')