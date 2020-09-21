"""
Code to read in csv datasets for HW1.
Authors: Caroline Sigl and Lindy Bustabad
"""

import pandas
from pandas import read_csv

#Importing Dataset #1
url = "https://raw.githubusercontent.com/casigl/Datasets/master/dataset1.csv"
dataset1_df = read_csv(url)
dataset1_df.columns = ['x', 'f(x)']

print(dataset1_df)

#Importing Dataset #2
url = "https://raw.githubusercontent.com/casigl/Datasets/master/dataset2.csv"
dataset2_df = read_csv(url)
dataset2_df.columns = ['x1', 'x2', 'x3', 'f(x1,x2,x3)']

print(dataset2_df)

#Importing Dataset #3
url = "https://raw.githubusercontent.com/casigl/Datasets/master/dataset3.csv"
dataset3_df = read_csv(url)
dataset3_df.columns = ['x', 'f(x)']

print(dataset3_df)
