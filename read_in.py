"""
Code to read in csv datasets for HW1.
Authors: Caroline Sigl and Lindy Bustabad
"""

import pandas
from pandas import read_csv

def dataset1():
    #Importing Dataset #1
    dataset1_df = pandas.read_csv("./dataset1.csv", sep=',', delimiter=None, header='infer')
    # url = "https://raw.githubusercontent.com/lkbbad/CSC370-HW2/master/dataset1.csv"
    # dataset1_df = read_csv(url)
    # dataset1_df.columns = ['x', 'f(x)']
    return dataset1_df

# def dataset2():
    # #Importing Dataset #2
    # dataset2_df = pandas.read_csv("./dataset2.csv", sep=',', delimiter=None, header='infer')
    # url = "https://raw.githubusercontent.com/lkbbad/CSC370-HW2/master/dataset2.csv"
    # dataset2_df = read_csv(url)
    # dataset2_df.columns = ['x1', 'x2', 'x3', 'f(x1,x2,x3)']

    # print(dataset2_df)

# def dataset3():
    # #Importing Dataset #3
    # dataset3_df = pandas.read_csv("./dataset3.csv", sep=',', delimiter=None, header='infer')
    # url = "https://raw.githubusercontent.com/lkbbad/CSC370-HW2/master/dataset3.csv"
    # dataset3_df = read_csv(url)
    # dataset3_df.columns = ['x', 'f(x)']

    # print(dataset3_df)
