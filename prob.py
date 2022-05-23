# trying to define a normal outcome distribution curve for each player based on that players modeled numbers

# plan is to model a players performance in real time, compare that with the pitcher
# then based on that output, create a distribution of probabilities based on the final number
# randomly select from said poisson distribution

# demonstrate modeling a player
import model
from sim import league
import numpy as np
import pandas as pd
import math

# import the data (no arguments means it will only be northwoods league data)
df1 = league(nwds_filter = False, lg_name = "Summer Ball").data
df1['RC_x'] = ((df1['H_x'] + df1['BB_x']) * df1['TB_x']) / df1['AB_x'] + df1['BB_x']
df1['RC_y'] = ((df1['H_y'] + df1['BB_y']) * df1['TB_y']) / df1['AB_y'] + df1['BB_y']

# filtering data
df1 = df1[df1['RC_x'] >= 1]
df1 = df1[df1["RC_y"] >= 1]
df1 = df1[df1["TB_y"] >= 30]

# build tensorflow model based on said data (going with random forest tho)
explanatory1 = df1[["TB_x", "OPS_x", "AB_x", "SO_x", "RC_x"]]
response1 = df1['RC_y']

df2 = league(nwds_filter = False, lg_name = 'summer ball').data
df2 = df2[df2['PA_x'] >= 50]
df2 = df2[df2['PA_y'] >= 50]
explanatory2 = df2[['TB_x', 'OPS_x', 'PA_x', 'AB_x', 'HR_x']]
response2 = df2['PA_y']

""" modeling both total bases and plate appearances """
#def __init__(self, explanatory, response, dummies = False, test_size = .3, n_estimators = 100):
_269rc = model.rf_model(explanatory1, response1, n_estimators = 150)
_269pa = model.rf_model(explanatory2, response2, n_estimators = 150)

# mean and std of predicted values
murc = _269rc.mean
stdrc = _269rc.std

mupa = _269pa.mean
stdpa = _269pa.std

""" Then make a model for pitchers """


class prob_bat():

	def __init__(self, player_number, team_url, sidearm = True, name = ''):
		self.name = name

		if sidearm == False:
			print('sidearm should be true until we work on this part.')

		elif sidearm == True:
			self.pred = _269.predict(self.pred_sidearm(team_url))
			self._range = [pred - (2*std), pred + (2*std)]

	def pred_sidearm(self, team_url, player_number):
		hit_tbl = pd.read_html(team_url)[0]
		player = hit_tbl[hit_tbl['#'] == player_number]
		player['RC'] = (((player["H"] + player['BB']) * player['TB']) / player["AB"] + player['BB'])
		player['PA'] = player['AB'] + player['BB'] + player['HBP'] + player['SF']
		rc_prediction = _269rc.model.predict(player[['TB', 'OPS', 'AB', 'SO', 'RC']])
		pa_prediction = _269pa.model.predict(player[['TB', 'OPS', 'PA', 'AB', 'HR']])

		rc_range = [math.floor(rc_prediction - 2*stdrc), math.ceil(rc_prediction + 2*stdrc)]
		pa_range = [math.floor(pa_prediction) - 2*stdpa, math.ceil(pa_prediction + 2*stdpa)]
		r = [rc_range[0] / pa_prediction, rc_range[1] / pa_prediction]
		return r

def predict_metrics_sidearm(team_url, player_number):
		hit_tbl = pd.read_html(team_url)[0]
		player = hit_tbl[hit_tbl['#'] == player_number]
		player['RC'] = (((player["H"] + player['BB']) * player['TB']) / player["AB"] + player['BB'])
		player['PA'] = player['AB'] + player['BB'] + player['HBP'] + player['SF']
		rc_prediction = _269rc.model.predict(player[['TB', 'OPS', 'AB', 'SO', 'RC']])
		pa_prediction = _269pa.model.predict(player[['TB', 'OPS', 'PA', 'AB', 'HR']])

		# this returns best and worst case scenario runs created over projected plate appearances in a list
		rc_range = [math.floor(rc_prediction - 2*stdrc), math.ceil(rc_prediction + 2*stdrc)]
		pa_range = [math.floor(pa_prediction) - 2*stdpa, math.ceil(pa_prediction + 2*stdpa)]
		r = [rc_range[0] / pa_prediction, rc_range[1] / pa_prediction]
		return r

schuman_pred = predict_metrics_sidearm('https://gvsulakers.com/sports/baseball/stats/2022', 11.0)
print(schuman_pred)

