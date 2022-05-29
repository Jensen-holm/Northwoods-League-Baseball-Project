# """
# Why: predict summer league bsbl performance
# specs: sklearn random forest regressor (originally tried tensorflow)
# """

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score
import seaborn as sns
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error
import matplotlib.pyplot as plt
import numpy as np
sns.set()

""" Random forest seems to get me better  results with nwds data """

class rf_model():

    def __init__(self, explanatory, response, dummies = False, test_size = .3, n_estimators = 100, pred_range = True, num_deviations = 2):
        self.num_deviations = num_deviations
        self.explanatory = explanatory
        self.response = response
        self.model = RandomForestRegressor(n_estimators = n_estimators, random_state = 42)

        self.x_train, self.x_test, self.y_train, self.y_test = train_test_split(explanatory, response, test_size = test_size, random_state = 42)

        if dummies == True:
            self.x_train, self.x_test, self.y_train, self.y_test = self.dumb_split(explanatory, response)

        self.fit()

        self.importances()

        self.evaluate()

        if pred_range == True:
            self.eval_range()

    def dumb_split(self, explanatory, response):
        explanatory = pd.get_dummies(explanatory)
        response = pd.get_dummies(response)
        x_train, x_test, y_train, y_test = train_test_split(explanatory, response, test_size = .3, random_state = 42)
        return x_train, x_test, y_train, y_test

    def fit(self):
        return  self.model.fit(self.x_train, self.y_train)

    def importances(self):
        #select feature importances to model off of
        importances = list(zip(list(self.model.feature_importances_), self.response.columns))
        print('\n---- Importance of selected features ----\n')
        for i in range(len(importances)):
            print(f'{importances[i][1]} : {importances[i][0]:.3f}\n')

    def evaluate(self, plot = False):
        # stats
        pred = self.model.predict(self.x_test)
        print(f'\n--- Eval without range ---\nR Squared: {r2_score(self.y_test, pred)}\n')

        # print the mae for each of the predictions
        for col in self.response.columns:
            pred1 = pd.DataFrame(pred, columns = self.response.columns)
            print(f'Mean Absolute Error for {col}: {mean_absolute_error(self.y_test[col], pred1[col]):.3f} \n')


        if plot != False:
            # x = np.arange(min(pred[2]), max(pred[2]))

            # plt.plot(x,x, color = 'red')
            plt.scatter(self.y_test, pred, marker = '^', alpha = .3)
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

    def eval_range(self):

        pred = self.model.predict(self.x_test)
        self.pred_df = pd.DataFrame(pred, columns = self.y_test.columns)
        print('\n---- Eval with range ----\n')

        actual = self.y_test
        self.pred_df.sort_index(axis = 1, inplace= True)
        actual.sort_index(axis = 1, inplace = True)
        self.pred_df.sort_index(inplace = True)
        actual.sort_index(inplace = True)

        self.ranges = []
        # for each column of predicted vals
        for col in self.y_test.columns:
            # create a range based on mu and std
            mu = self.y_test[col].mean()
            std = self.y_test[col].std()
            self.pred_df[col + ' min'] = self.pred_df[col] - (std * self.num_deviations)
            self.pred_df[col + ' max'] = self.pred_df[col] + (std * self.num_deviations)
            self.ranges.append([mu - (std * self.num_deviations), mu + (std * self.num_deviations), col])

        # evaluate if the actual value is within each predicted range or not        
        yes = 0
        no = 0
        off = 0
        for col in self.y_test.columns:
            for i in range(len(self.pred_df)):
                if self.pred_df[col + ' min'].iloc[i] <= actual[col].iloc[i] <= self.pred_df[col + ' max'].iloc[i]:
                    yes += 1
                elif self.pred_df[col + ' min'].iloc[i] > actual[col].iloc[i]:
                    no +=1
                    off += (self.pred_df[col + ' min'].iloc[i] - actual[col].iloc[i])
                elif self.pred_df[col + ' max'].iloc[i] < actual[col].iloc[i]:
                    no += 1
                    off += (actual[col].iloc[i] - self.pred_df[col + ' max'].iloc[i])

        ''' evaluation branch '''
        if no != 0 and yes != 0:
            print(f'{(yes / (yes + no)) * 100:.3f}% of the actual values fall within the predicted range.\n')

        elif no == 0:
            print(f'100% of the actual values fall within the predicted range.\n')

        elif yes == 0:
            print(f'0% of the actual values fall within the predicted range.\n')

        if no != 0:
            print(f'Predicted values outside the range are off by an average absolute value of {off / no:.3f} units.\n')

'''
within simp.py is where we will
estimate the ranges of each
individial we want to project
'''
