# -*- coding: utf-8 -*-
import numpy as np
import pandas as pd
from collections import OrderedDict
from sklearn.model_selection import train_test_split




def chunks(l, n):
    """Yield successive n-sized chunks from l."""
    for i in range(0, len(l), n):
        yield l[i:i + n]
        
def rmse(y, y_hat):
    return ((np.sum((y_hat-y)**2)/ len (y)) **0.5) 

def mae(y, y_hat):
    return np.sum(abs(y - y_hat)) / len(y)

def fit(x,y,deg): 
    df = pd.DataFrame(data = {'x':x,'y':y})
    train, test = train_test_split(df, test_size=0.2)
    x = train['x']
    y = train['y']
    z = np.polyfit(x, y, deg = deg, full = False)
    p = np.poly1d(z)
    x = test['x']
    y = test['y']
    y_hat = p(x)
    MAE = mae(y, y_hat)
    RMSE = rmse(y, y_hat)
    return (MAE, RMSE)


def bagged_fit(x,y,deg, bags = 5, frac = .75):
    df = pd.DataFrame(data = {'x':x,'y':y})
    train, test = train_test_split(df, test_size=0.2)
    coef = []
    for i in range(bags):
        sample = train.sample(frac = frac)
        x = sample['x']
        y = sample['y']
        z = np.polyfit(x, y, deg = deg, full = False)
        coef.append(z)
    p = np.poly1d(pd.DataFrame(coef).mean())
    y = test['y']
    x = test['x']
    y_hat = p(x)
    MAE = mae(y, y_hat)
    RMSE = rmse(y, y_hat)
    return (MAE, RMSE)
    


def linear_validate(x, y, degrees = 3, bagged = True, **kwargs):
    error_dict = OrderedDict([('degree',[]), ('MAE',[]), ('RMSE',[])])
    for d in range(degrees):
        deg = d + 1
        if bagged:MAE, RMSE = bagged_fit(x,y,deg, **kwargs)
        else: MAE, RMSE = fit(x,y,deg)
        error_dict['degree'].append(deg)
        error_dict['MAE'].append(MAE)
        error_dict['RMSE'].append(RMSE)
    return pd.DataFrame(error_dict)