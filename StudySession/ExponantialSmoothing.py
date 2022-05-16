
from decimal import ROUND_DOWN
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from pyparsing import Each
from scipy.optimize import minimize
from sklearn.metrics import mean_squared_log_error
from sklearn.model_selection import TimeSeriesSplit
from array import *

actual_sales_list = []

mad_result = 0
mse_result = 0
mape_result = 0

with open('input.txt', 'r') as data:
    for line in data:
        newline = line.strip('\n')
        actual_sales_list.append(int(newline))

def exponential_smoothing(series, alpha, beta):
    i = 0
    f = []
    t = []  
    fit = []      
    f.append(series[1])
    t.append(series[2])
    

    for i in range(0,27,1):
        f.append(alpha * series[i+3] + (1-alpha) * (f[i] + t[i]))
        t.append(beta*(f[i+1] - f[i]) + (1-beta)*t[i])
        fit.append(round(f[i] + t[i]))  

    return fit

def mad_calculation(series):
    fit = []
    sum = [0 for _ in range(361)]
    mad = [0 for _ in range(361)]

    for alpha in range(5, 100, 5):
        for beta in range(5, 100, 5): 
            fit.append(exponential_smoothing(series, float(alpha/100), float(beta/100)))

    for i in range(0,len(fit)):
        for x in range(0,27,1):
            sum[i] = abs((sum[i] + abs(round(fit[i][x])) - series[x+3]))

    for i in range(0,len(fit)):    
        mad[i] = sum[i]/27
    
    print("MAD Data")
    print(mad)
    return mad

def mse_calculation(series):
    fit = []
    mse = [0 for _ in range(361)]
    sum = [0 for _ in range(361)]
    
    for alpha in range(5, 100, 5):
        for beta in range(5, 100, 5): 
            fit.append(exponential_smoothing(series, float(alpha/100), float(beta/100)))

    for i in range(0,len(fit)):
        for x in range(0,27,1):
            sum[i] = sum[i] + ((round(fit[i][x]) - series[x+3])*(round(fit[i][x]) - series[x+3]))
    
    for i in range(0,len(fit)):
        for y in range(0,21,1):
            mse [i] = sum[i]/27
    print("MSE Data")
    print(mse)   
    return mse   

def mape_calculation(series):
    fit = []
    mape = [0 for _ in range(361)]
    sum = [0 for _ in range(361)]

    for alpha in range(5, 100, 5):
        for beta in range(5, 100, 5): 
            fit.append(exponential_smoothing(series, float(alpha/100), float(beta/100)))

    for i in range(0,len(fit)):
        for x in range(0,27,1):
            sum[i] = sum[i] + (abs(round(fit[i][x]) - series[x+3])/series[x+3])*100
    
    for i in range(0,len(fit)):
        mape [i] = sum[i]/27

    print("MAPE Data")
    print(mape)
    return mape

def find_alpha_beta_valuse(index):
    a = int(index / 21)
    b = index % 21
    
    alpha = a*5/100
    beta = b*5/100

    return [alpha, beta]

mad = mad_calculation(actual_sales_list)
mse = mse_calculation(actual_sales_list)
mape = mape_calculation(actual_sales_list)

print()
print("----ANSWERS----")
print()
print("Min MAD: ",np.min(mad))
print("Alpha-Beta")
print(find_alpha_beta_valuse(mad.index(np.min(mad))))
print("Min MSE: ",np.min(mse))
print("Alpha-Beta")
print(find_alpha_beta_valuse(mse.index(np.min(mse))))
print("Min MAPE: ",np.min(mape))
print("Alpha-Beta")
print(find_alpha_beta_valuse(mape.index(np.min(mape))))

