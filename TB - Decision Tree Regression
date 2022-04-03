""" Libraries """
import matplotlib.pyplot as plt 
import seaborn as sns
import pandas as pd
import numpy as np
import sqlite3 
sns.set()

""" Read in the Northwoods League Data from the sqlite3 Database """
northwoods_db = sqlite3.connect("Northwoods.db")
cur = northwoods_db.cursor()

""" import data without outliers """
bat = pd.read_sql_query("SELECT * FROM ALL_NORTHWOODS_DATA WHERE PA_X >= 50 AND PA_Y >= 50 AND OPS_y >= .4", northwoods_db)

# Clean it up
bat = bat.apply(pd.to_numeric, errors='coerce').combine_first(bat)
bat = bat.dropna(how = "all", axis = "columns")
bat = bat.fillna(0)
bat = bat.drop_duplicates(subset = ["AgeDif_x", "Age_x", "TB_y", "SLG_y"], keep = "first")

# Exploratory Data Analysis 

def scatter(x, y, xlabel, ylabel):
    plt.scatter(x, y, marker= "o", alpha = .5)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.show()

def normality(x):
    plt.hist(x, bins = 50)
    plt.show()
    
normality(bat["TB_y"])
scatter(bat["TB_x"], bat["TB_y"], "Spring TB", "Summer TB")

# Bootstrapping data & creating dummy variables

def btstrap(df):
    np.random.seed(3)
    btstr_data = pd.DataFrame(columns=df.columns)
    for data in range(df.shape[0]):
        selected_num = np.random.choice(range(df.shape[0]))
        btstr_data = btstr_data.append(df[selected_num : selected_num + 1])
    return btstr_data

def draw_bs_data(dataframe, num_times_strapped):
    data = [btstrap(dataframe) for i in range(num_times_strapped)]
    return pd.concat(data)

bs_data = draw_bs_data(bat, 2)
dummies = pd.get_dummies(bs_data)

# Modeling
from sklearn.tree import DecisionTreeRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error as mse

x = dummies[[col for col in dummies.columns if "x" in col or "Tm" in col or "Lev" in col]]
y = dummies["TB_y"]
x_train, x_test, y_train, y_test = train_test_split(x, y, test_size= .2, train_size= .8, random_state= 1)
dt = DecisionTreeRegressor(max_depth= 30, random_state= 1, min_samples_split = 10)
dt.fit(x_train, y_train)
y_pred = dt.predict(x_test)

# Visualizing // Evaluating

def evaluate(model_predicted_values, y_test):
    print("predictions are based on test data\n- Minimum prediction: {min(model_predicted_values):.4f}")
    print(f"Mean prediction: {np.mean(model_predicted_values):.4f}\n- Median prediction: {np.median(model_predicted_values):.4f}")
    print(f"Max prediction: {max(model_predicted_values):.4f}")
    print(f"Mean squared error: {mse(y_test, model_predicted_values):.4f}")
    print(f"Root mean squared error: {(mse(y_test, model_predicted_values) ** (1/2)):.4f}")
    plt.scatter(x = y_pred, y = y_test, alpha = .5, marker = "^")
    x = np.arange(0,max(y_test))
    plt.plot(x, 1*x , c = "red")
    plt.title("Actual vs. predicted scatter plot")
    plt.xlabel("Predicted Value")
    plt.ylabel("Actual Value")
    plt.show()
    plt.title("Distribution of predicted values")
    sns.histplot(y_pred, bins = 50)
    plt.show()

evaluate(y_pred, y_test)
# This leaves us with the actual versus predicted plot that I posted in a seperate file
# inside this repository along with a histogram that displays the distribution of 
# predicted values.
