"""
Code to read in csv datasets for HW1.
Authors: Caroline Sigl and Lindy Bustabad
"""

import pandas
from pandas import read_csv

def dataset1():
    #Importing Dataset #1
    dataset1_df = pandas.read_csv("./dataset1.csv", sep=',', delimiter=None, header='infer')
    return dataset1_df

def dataset2():
    # #Importing Dataset #2
    dataset2_df = pandas.read_csv("./dataset2.csv", sep=',', delimiter=None, header='infer')
    return dataset2_df

