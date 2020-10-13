"""
Code to read in csv datasets for HW1.
Authors: Caroline Sigl and Lindy Bustabad
"""

import pandas
from pandas import read_csv

def dataset1():
    #Importing Dataset #1
    dataset1_df = pandas.read_csv("./csv/dataset1.csv", sep=',', delimiter=None, header='infer')
    return dataset1_df

def dataset2():
    # #Importing Dataset #2
    dataset2_df = pandas.read_csv("./csv/dataset2.csv", sep=',', delimiter=None, header='infer')
    return dataset2_df

def d1fitness():
    d1fitness_df = pandas.read_csv("./csv/d1fitness.csv", sep=',', delimiter=None, header='infer')
    return d1fitness_df

def d1mse():
    d1mse_df = pandas.read_csv("./csv/d1mse.csv", sep=',', delimiter=None, header='infer')
    return d1mse_df

def d2fitness1():
    d2fitness1_df = pandas.read_csv("./csv/d2fitness1.csv", sep=',', delimiter=None, header='infer')
    return d2fitness1_df

def d2mse1():
    d2mse1_df = pandas.read_csv("./csv/d2mse1.csv", sep=',', delimiter=None, header='infer')
    return d2mse1_df

def d2fitness2():
    d2fitness2_df = pandas.read_csv("./csv/d2fitness2.csv", sep=',', delimiter=None, header='infer')
    return d2fitness2_df

def d2mse2():
    d2mse2_df = pandas.read_csv("./csv/d2mse2.csv", sep=',', delimiter=None, header='infer')
    return d2mse2_df

def d2fitness3():
    d2fitness3_df = pandas.read_csv("./csv/d2fitness3.csv", sep=',', delimiter=None, header='infer')
    return d2fitness3_df

def d2mse3():
    d2mse3_df = pandas.read_csv("./csv/d2mse3.csv", sep=',', delimiter=None, header='infer')
    return d2mse3_df

def d2fitness4():
    d2fitness4_df = pandas.read_csv("./csv/d2fitness4.csv", sep=',', delimiter=None, header='infer')
    return d2fitness4_df

def d2mse4():
    d2mse4_df = pandas.read_csv("./csv/d2mse4.csv", sep=',', delimiter=None, header='infer')
    return d2mse4_df

def d2fitness5():
    d2fitness5_df = pandas.read_csv("./csv/d2fitness5.csv", sep=',', delimiter=None, header='infer')
    return d2fitness5_df

def d2mse5():
    d2mse5_df = pandas.read_csv("./csv/d2mse5.csv", sep=',', delimiter=None, header='infer')
    return d2mse5_df