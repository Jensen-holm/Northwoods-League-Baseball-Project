from modeling import rf_model
from prob import league

# import data
df =  league(nwds_filter = False).data

df['RC_x'] = ((df['H_x'] + df['BB_x']) * df['TB_x']) / df['AB_x'] + df['BB_x']
df['RC_y'] = ((df['H_y'] + df['BB_y']) * df['TB_y']) / df['AB_y'] + df['BB_y']

df = df[df['RC_x'] >= 1]
df = df[df["RC_y"] >= 1]
df = df[df["TB_y"] >= 30]
df = df.dropna(how = 'all')

# colligate numbers to predict range of possible nwds numbers
explanatory = df[['TB_x', 'OPS_x', 'PA_x','AB_x', 'SO_x', 'BB_x', 'HR_x']]
response = df[['RC_y', 'TB_y', 'PA_y', 'SO_y', 'BB_y']]

my_model = rf_model(explanatory, response, n_estimators = 150)

''' work on eval range function in modeling '''
