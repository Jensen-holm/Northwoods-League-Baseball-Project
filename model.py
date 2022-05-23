#%%
"""
What: tensorflow Sequential model
Why: predict summer league bsbl performance
specs: tensorflow keras sequential regression model
"""

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import StandardScaler
# from sklearn.preprocessing import Normalizer
from tensorflow.keras.models import Sequential
from tensorflow.keras import layers
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.callbacks import EarlyStopping
from sklearn.metrics import r2_score
import seaborn as sns  
from sklearn.ensemble import RandomForestRegressor
import matplotlib.pyplot as plt 
import numpy as np 
sns.set()

"""

in the process of training and testing these settings 

"""

class tf_model():

    def __init__(self, name, dataset, explanatory, response, split = .3, standardize = True):
        self.name = name
        self.split = split # 70-30 train_test_split
        self.standardize = standardize
        self.model = self.build(dataset, explanatory, response)

        # standardize fit branch
        if self.standardize == True:
            self.Fit(self.features_train_scaled, self.labels_train_scaled)
            self.Eval(self.model, self.features_test_scaled, self.labels_test_scaled)
        elif self.standardize == False:
            self.Fit(self.features_train, self.labels_train)
            self.Eval(self.model, self.features_test, self.labels_test)

    def build(self, dataset, explanatory, response, dummies = True, dropout_ = .3):

        # create instance of sequential model
        my_model = Sequential(name = self.name)
        df = dataset
        # to dummy or not to dummy
        if dummies == True:
            df = pd.get_dummies(pd.DataFrame(dataset))
        elif dummies == False:
            df = pd.DataFrame(dataset)

        # train_test_split
        # can only be one response in sequential models
        self.features_train, self.features_test, self.labels_train, self.labels_test = train_test_split(explanatory, response, test_size = self.split, random_state = 42)

        # to standardize or not to standardize
        if self.standardize == True:

            # standardization and the column transformer
            numeric_features = explanatory.select_dtypes(include = ['float64','int64'])
            numeric_columns = numeric_features.columns

            ct = ColumnTransformer([('only numeric',StandardScaler(), numeric_columns)], remainder = 'passthrough')

            # ct for the lables
            # since there is only one column
            self.labels_train_scaled = (self.labels_train - self.labels_train.mean())/self.labels_train.std() 
            self.labels_test_scaled = (self.labels_test - self.labels_train.mean()) / self.labels_train.std()

            self.features_train_scaled = ct.fit_transform(self.features_train)
            self.features_test_scaled = ct.fit_transform(self.features_test)

            # # I do not know if we will even need this block
            # self.labels_train_scaled = ctlabels.fit_transform(self.labels_train)
            # self.labels_test_scaled = ctlabels.fit_transform(self.labels_test)

            my_model.add(layers.InputLayer(input_shape = (self.features_train_scaled.shape[1])))
            # adding hidden layers
            my_model.add(layers.Dense(32, activation = 'relu'))
            #my_model.add(layers.Dropout(dropout_))
            # output layer
            my_model.add(layers.Dense(1))
            # optimiser
            opt = Adam(learning_rate = 0.01)
            my_model.compile(loss = 'mse', metrics = ['mae'], optimizer = opt)
            self.es = EarlyStopping(monitor='val_loss', mode='min', verbose=0, patience = 20)
            print(my_model.summary())
            return my_model

        elif self.standardize == False:

            # same thing but without standardization and the column transformer
            my_model.add(layers.InputLayer(input_shape = (self.features_train.shape[1])))
            # adding hidden layers
            my_model.add(layers.Dense(32, activation = 'relu'))
            #my_model.add(layers.Dropout(dropout_))
            # output layer
            my_model.add(layers.Dense(1))
            # optimiser
            opt = Adam(learning_rate = 0.01)
            my_model.compile(loss = 'mse', metrics = ['mae'], optimizer = opt)
            self.es = EarlyStopping(monitor = 'val_loss', mode = 'min', verbose = 0, patience = 20)
            print(my_model.summary())
            return my_model

        elif self.standardize != False:
            return f"standardize should be a Boolean Value, not {self.standardize}."

    # fit to training data
    def Fit(self, features_train, labels_train, num_epochs = 5, batch_size = 1):
        return self.model.fit(features_train, labels_train, epochs=num_epochs, batch_size= batch_size, verbose=1, validation_split = 0.2) #callbacks = [self.es])

    # evaluate on the test data
    def Eval(self, model, features_test, labels_test):
        val_mse, val_mae = self.model.evaluate(features_test, labels_test, verbose = 0)
        y_true = labels_test
        pred = model.predict(features_test)
        r2 = r2_score(labels_test, pred)
        plt.scatter(pred, labels_test, marker = '^', alpha = .2)
        plt.xlabel('Predicted Value')
        plt.ylabel('Actual Value')
        x = np.arange(max(pred))
        plt.plot(x,x, color = 'red')
        plt.show()

        # distribution of predicted values
        plt.hist(pred, bins = 50)

        print(f"\n --- RESULTS ---\nR Squared: {r2}\nMAE: {val_mae}\nMSE: {val_mse}")







""" Random forest seems to get me better  results with nwds data """

class rf_model():

    def __init__(self, explanatory, response, dummies = False, test_size = .3, n_estimators = 100):

        self.explanatory = explanatory
        self.response = response
        self.model = RandomForestRegressor(n_estimators = n_estimators, random_state = 42)

        self.x_train, self.x_test, self.y_train, self.y_test = train_test_split(explanatory, response, test_size = .3, random_state = 42)

        if dummies == True:
            self.x_train, self.x_test, self.y_train, self.y_test = self.dumb_split(explanatory, response)

        self.fit(self.x_train, self.y_train)
        self.mean, self.std, self.pred = self.evaluate(self.x_test, self.y_test)

        #select feature importances to model off of 
        importances = list(self.model.feature_importances_)
        print(importances)

    def dumb_split(self, explanatory, response):
        explanatory = pd.get_dummies(explanatory)
        response = pd.get_dummies(response)
        x_train, x_test, y_train, y_test = train_test_split(explanatory, response, test_size = .3, random_state = 42)
        return x_train, x_test, y_train, y_test

    def fit(self,x_train, y_train):
        return  self.model.fit(x_train, y_train)

    def evaluate(self, x_test, y_test):
        # stats
        pred = self.model.predict(x_test)
        print(f'R Squared: {r2_score(y_test, pred)}\n')
        # print(f'Mean Absolute Error: \n')
        # print(f'Mean Squared Error \n')

        #plot
        x = np.arange(min(pred), max(pred))

        plt.plot(x,x, color = 'red')
        plt.scatter(y_test, pred, marker = '^', alpha = .3)
        plt.xlabel('Actual')
        plt.ylabel('Predicted')
        plt.show()

        # dist of pred values 
        plt.hist(pred, bins = 50)
        plt.title("Distribution of Predicted values on test data")
        plt.show()

        # get mean and std from predicted val distribution
        std = np.std(pred)
        mean = np.mean(pred)

        return mean, std, pred

    def projection(self, metrics = []):
        # use this to predict future performances if evaluate numbers are good enough
        return self.model.predict(metrics) # add std twice so we can get 95% confidence interval and pull randomly from that
