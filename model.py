from modeling import rf_model
from prob import league
import pandas as pd

# import data
df =  league(nwds_filter = False).data

df['RC_x'] = ((df['H_x'] + df['BB_x']) * df['TB_x']) / df['AB_x'] + df['BB_x']
df['RC_y'] = ((df['H_y'] + df['BB_y']) * df['TB_y']) / df['AB_y'] + df['BB_y']

''' create single columns '''
df['1b_x'] = df['H_x'] - (df['2B_x'] + df['3B_x'] + df['HR_x'])
df['1b_y'] = df['H_y'] - (df['2B_y'] + df['3B_y'] + df['HR_y'])

'''create in play outs columns '''
df['inpO_x'] = df['PA_x'] - (df['H_x'] - df['SO_x'] - df['HBP_x'] - df['SO_x'] - df['BB_x'])
df['inpO_y'] = df['PA_y'] - (df['H_y'] - df['SO_y'] - df['HBP_y'] - df['SO_y'] - df['BB_y'])

df = df[df['RC_x'] >= 1]
df = df[df["RC_y"] >= 1]
df = df[df["TB_y"] >= 10]
df = df[df['BB_y'] >= 1]
df = df[df['SO_y'] >= 1]
df = df[df['PA_y'] >= 50]

'''
Try modeling based on overall colligate numbers
we will have to re scrape potentially and refilter
the modeling data to do so.
'''

'''
we need to modify it so taht the 
model will predict at bat probabilities
that add up to one
instead of full season statistics.
'''


# colligate numbers to predict range of possible nwds numbers
explanatory = df[['TB_x', 'OPS_x', 'PA_x','AB_x', 'SO_x', 'BB_x', 'HR_x', 'RC_x', '2B_x']]
explanatory_cols = [col.replace('_x', '') for col in explanatory.columns]
# print(explanatory_cols)

response = df[['1b_y', '2B_y', '3B_y', 'HR_y', 'SO_y', 'BB_y', 'inpO_y', 'RC_y', 'PA_y']]
response_cols = response.columns

my_model = rf_model(explanatory, response, n_estimators = 50, num_deviations = 1.25)

'''
project useful stats for the managers to see
for the growlers whole team and put that into a
csv. will also be able to import new teams from
baseball reference for potential pick ups during the 
season
'''
