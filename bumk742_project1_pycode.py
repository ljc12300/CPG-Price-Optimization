# -*- coding: utf-8 -*-
"""BUMK742_Project1_PYcode

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1BbPp4MbZuxwgQcz9TkiAdVMr7uJcCbyY
"""

import numpy as np
import pandas as pd
from sklearn import datasets

# The GDRIVE_PATH variable tells Google Colab "how to connect"
GDRIVE_PATH = '/content/gdrive' # do not change this GDRIVE_PATH variable!

from google.colab import drive
drive.mount(GDRIVE_PATH)

# Make sure that MY_COLAB_FOLDER points to the folder with the tropic.csv file
MY_COLAB_FOLDER = 'My Drive/Past_Project_Codes_PY/Dataset/'
DATA_FOLDER = GDRIVE_PATH + '/' + MY_COLAB_FOLDER # this line creates the path
print(DATA_FOLDER)

X = pd.read_csv(
    DATA_FOLDER + 'tropic.csv',
)

X.head()

X.describe()

# Pre-steps of fitting models

X['Store'] = X.Store.astype('category')

X.dtypes

X = pd.get_dummies(X)
X

# Rename Store_XX into sequence numbers (1....15)
  # create a dictionary
dict = {'Store_2':'Store1','Store_14':'Store2','Store_32':'Store3','Store_52':'Store4','Store_62':'Store5','Store_68':'Store6','Store_71':'Store7','Store_72':'Store8','Store_93':'Store9','Store_95':'Store10','Store_111':'Store11','Store_123':'Store12','Store_124':'Store13','Store_130':'Store14','Store_137':'Store15'}

  # call rename () method
X.rename(columns=dict,
          inplace=True)

display(X)

# Convert Weeks into Quarters
qrt1_week = list(range(1,14)) + list(range(53,66))
qrt1_week

qrt2_week = list(range(14,27)) + list(range(66,79))
qrt2_week

qrt3_week = list(range(27,40)) + list(range(79,92))
qrt3_week

qrt4_week = list(range(40,53)) + list(range(92,105))
qrt4_week

# create a list of our conditions
conditions = [
    (X['Week'].isin(qrt1_week)),
    (X['Week'].isin(qrt2_week)),
    (X['Week'].isin(qrt3_week)),
    (X['Week'].isin(qrt4_week)),
    ]

# create a list of the values we want to assign for each condition
values = ['qrt1', 'qrt2', 'qrt3','qrt4']

# create a new column and use np.select to assign values to it using our lists as arguments
X['qrt_1234'] = np.select(conditions, values)

# display updated DataFrame
X.head()

X['qrt_1234'] = X.qrt_1234.astype('category')
X.dtypes

X1 = pd.get_dummies(X.qrt_1234)
X1

X = X.join(X1)

X.head()

# Add dummy Variable "end_9_9" if the last digit of Price is 9 
  # Need to convert Price from float to String
X['Price'] = X.Price.astype('string')

Price_not_end9 = list(range(0,9)) 
Price_not_end9

X['end_9'] = X['Price'].str[-1:]

X['end_9'] = X.end_9.astype('int')

X.dtypes

X.loc[X['end_9'] == 9, 'end_9_9'] = 1 
X.loc[X['end_9'].isin(Price_not_end9), 'end_9_9'] = 0

X['end_9_9'] = X.end_9_9.astype('category')

# Add interaction variable (price* deal)
X['Price'] = X.Price.astype('float')
X["interaction_1"] = X["Price"] * X["Deal"]

import numpy as np
from sklearn.linear_model import LinearRegression
import statsmodels.api as sm

# 1. Linear Regression Model
x = pd.DataFrame(np.c_[X["end_9_9"], X["interaction_1"], X["qrt1"], X["qrt2"], X["qrt3"], X["Price"], X["Deal"], X["Store1"], X["Store2"],X["Store3"],X["Store4"],X["Store5"],X["Store6"],X["Store7"],X["Store8"],X["Store9"],X["Store10"],X["Store11"],X["Store12"],X["Store13"],X["Store14"]],
                 columns = ["end_9_9", "interaction_1","qrt1","qrt2","qrt3","Price","Deal","Store1","Store2","Store3","Store4","Store5","Store6","Store7","Store8","Store9","Store10","Store11","Store12","Store13","Store14"])
y = X["Quant"]

# Note the difference in argument order
Linear_Regression_Model = sm.OLS(y, x).fit()
predictions = Linear_Regression_Model.predict(x) # make the predictions by the model

# Print out the statistics
Linear_Regression_Model.summary()

# 2. semi-log model
X["log_Quant"] = np.log(X["Quant"])

x = pd.DataFrame(np.c_[X["end_9_9"], X["interaction_1"], X["qrt1"], X["qrt2"], X["qrt3"], X["Price"], X["Deal"], X["Store1"], X["Store2"],X["Store3"],X["Store4"],X["Store5"],X["Store6"],X["Store7"],X["Store8"],X["Store9"],X["Store10"],X["Store11"],X["Store12"],X["Store13"],X["Store14"]],
                 columns = ["end_9_9", "interaction_1","qrt1","qrt2","qrt3","Price","Deal","Store1","Store2","Store3","Store4","Store5","Store6","Store7","Store8","Store9","Store10","Store11","Store12","Store13","Store14"])
y = X["log_Quant"] 

# Note the difference in argument order
Semi_log_Linear_Regression_Model = sm.OLS(y, x).fit()
predictions = Semi_log_Linear_Regression_Model.predict(x) # make the predictions by the model

# Print out the statistics
Semi_log_Linear_Regression_Model.summary()

# 3. Log-log model (log the price)
x = pd.DataFrame(np.c_[X["end_9_9"], X["interaction_1"], X["qrt1"], X["qrt2"], X["qrt3"], np.log(X["Price"]), X["Deal"], X["Store1"], X["Store2"],X["Store3"],X["Store4"],X["Store5"],X["Store6"],X["Store7"],X["Store8"],X["Store9"],X["Store10"],X["Store11"],X["Store12"],X["Store13"],X["Store14"]],
                 columns = ["end_9_9", "interaction_1","qrt1","qrt2","qrt3","log_Price","Deal","Store1","Store2","Store3","Store4","Store5","Store6","Store7","Store8","Store9","Store10","Store11","Store12","Store13","Store14"])
y = X["log_Quant"] 

# Note the difference in argument order
Log_log_Linear_Regression_Model = sm.OLS(y, x).fit()
predictions = Log_log_Linear_Regression_Model.predict(x) # make the predictions by the model

# Print out the statistics
Log_log_Linear_Regression_Model.summary()