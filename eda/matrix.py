# -*- coding: utf-8 -*-

import numpy as np
from sklearn.model_selection import train_test_split
import warnings
import numpy.polynomial.polynomial as poly
warnings.simplefilter('ignore', np.RankWarning)
import pandas as pd
from bokeh.models import Title
from bokeh.models import HoverTool
from bokeh.plotting import figure
from bokeh.io import curdoc
from bokeh.layouts import layout

#https://codefying.com/2016/08/18/two-ways-to-perform-linear-regression-in-python-with-numpy-ans-sk-learn/


def bk_circle(x,y, alpha=0.08, theme = False, regress = False, **kwargs):
    
    df = pd.DataFrame(data = {'x':x,'y':y})
    df.sort_values(by = 'x', inplace = True)
    df.reset_index(drop = True, inplace = True)
    x = df['x']
    y = df['y']
    p = figure()
    if theme:
        doc = curdoc()
        doc.theme = theme
        doc.add_root(p)  
    p.circle(x, y, size=5, alpha=alpha)
    if regress:
        try:
            if kwargs['best_poly']:
                degree,_ =  get_best_poly(x,y,3, 20)
        except KeyError:
            try:
                degree = kwargs['degree'] 
            except KeyError:
                degree = 1
        try:
            bags =  kwargs['bags'] 
        except KeyError:
            bags = 10
        coefs, error, r_squared = get_bagged_poly(x,y, degree, bags)
        ffit = poly.polyval(x, coefs)
        line = p.line(x = x, y = ffit, color = 'black', line_width = 1)
        hover = HoverTool(tooltips=[("R Squared", str(r_squared)),
                                ("MSE", str(round(error)))])
        hover.renderers.append(line)
        p.tools=[hover]
    return p

def bk_hist(series, theme = False):
    p = figure()
    hist, edges = np.histogram(series, density=True)
    p.quad(top=hist, bottom=0, left=edges[:-1], right=edges[1:]) 
    if theme:
        doc = curdoc()
        doc.theme = theme
        doc.add_root(p)  
    return p



def get_poly_fit(x,y, degree):
    """
    get_poly_fit returns the polynomial coefficients 
    to a specified degree and the cross validated error
    
    Params:
        x: independent data
        y: dependent data
        degree: degree to fit polynomial to
    
    Returns:
        result: dictionary with the polynomial coefficients and cross validated error
    
    """

    df = pd.DataFrame(data = {'x':x,'y':y})
    df.sort_values(by = 'x', inplace = True)
    df.reset_index(drop = True, inplace = True)
    x = df['x']
    y = df['y']
    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2)
    coefs = poly.polyfit(x_train,y_train, degree)
    predict=poly.polyval(x_test, coefs)
    error=np.mean((predict-y_test)**2)
    result = {'coefs':coefs, 'error':error}
    return result


def get_poly_fits(x,y, degrees):
    """
    get_poly_fits returns the polynomial 
    coefficients to a specified range of degrees
    
    Params:
        x: independent data
        y: dependent data
        degrees: highest degree to fit a polynomial
    
    Returns:
        result: dictionary with the polynomial coefficients and cross validated error of
                each polynomial
    
    """
    df = pd.DataFrame(data = {'x':x,'y':y})
    df.sort_values(by = 'x', inplace = True)
    df.reset_index(drop = True, inplace = True)
    x = df['x']
    y = df['y']
    degree_range = range(degrees)
    results = {degree+1:{} for degree in degree_range}
    for degree in degree_range:
        degree = degree + 1
        result = get_poly_fit(x,y, degree)
        results[degree].update(result)
    return results


def sample_poly_fit(x,y,degrees, samples):
    """
    sample_poly_fit returns the cross validated error 
    to a specified range of degrees, for n samples
    
    Params:
        x: independent data
        y: dependent data
        degrees: highest degree to fit a polynomial
        samples: how many samples to run
    
    Returns:
        error_df: pd.DataFrame of cross validated errors for each 
                degree
    
    """
    df = pd.DataFrame(data = {'x':x,'y':y})
    df.sort_values(by = 'x', inplace = True)
    df.reset_index(drop = True, inplace = True)
    x = df['x']
    y = df['y']
    degree_range = range(degrees)
    errors = {degree+1:[] for degree in degree_range}
    for sample in range(samples):
        results = get_poly_fits(x,y, degrees)
        for key,value in results.items():
            errors[key].append(value['error'])
    error_df = pd.DataFrame(errors)
    return error_df
    
def get_best_poly(x,y,degrees, samples):
    """
    get_best_poly returns the polynomial degree with lowest 
    average cross validated error to a  specified range of 
    degrees, for n samples
    
    Params:
        x: independent data
        y: dependent data
        degrees: highest degree to fit a polynomial
        samples: how many samples to run
    
    Returns:
        error_df: pd.DataFrame of cross validated errors for each 
                  degree
        best_poly: int, the degree with the lowest average 
                    cross validated error
    
    """
    df = pd.DataFrame(data = {'x':x,'y':y})
    df.sort_values(by = 'x', inplace = True)
    df.reset_index(drop = True, inplace = True)
    x = df['x']
    y = df['y']
    error_df = sample_poly_fit(x,y,degrees, samples)
    errors = pd.DataFrame(error_df.mean()).reset_index()
    errors.columns = ['degrees', 'values']
    errors.index =[0 for x in range(len(errors))]
    best_poly = errors.pivot(columns = 'degrees', values = 'values').idxmin(axis=1).values[0]
    return best_poly, error_df


def get_bagged_poly(x,y, degree, bags):
    """
    get_bagged_poly returns the polynomial 
    coefficients to a specified degrees and its 
    cross validated error using a bagging with
    replacement
    
    Params:
        x: independent data
        y: dependent data
        degree: degree to fit a polynomial
        bags: how many bags to run
    
    Returns:
        result: int, the degree with the lowest average 
                cross validated error
    
    """
    df = pd.DataFrame(data = {'x':x,'y':y})
    df.sort_values(by = 'x', inplace = True)
    df.reset_index(drop = True, inplace = True)
    x = df['x']
    y = df['y']
    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2)
    bag_range = range(bags)
    results = []
    for bag in bag_range:
        sample_df = pd.DataFrame({'x':x_train, 'y':y_train}).sample(frac = .8, replace = True)
        x_sample = sample_df['x']
        y_sample = sample_df['y']
        coefs = poly.polyfit(x_sample,y_sample, degree)
        results.append(coefs)
    coefs = np.mean(np.array(results), axis = 0)
    yhat = poly.polyval(x_train,coefs)        
    ybar = y_train.mean()          
    ssres = np.sum((y_train-yhat)**2)   
    sstot = np.sum((y_train - ybar)**2)    
    r_squared = 1 - ssres / sstot
    predict=poly.polyval(x_test, coefs)
    error=np.mean((predict-y_test)**2)
    return coefs, error, r_squared

def bk_matrix(df, theme = False, w_h = 400, alpha = .1, regress = False, **kwargs):
    rows = []
    for y in df.columns:
        i = 0
        r = []
        for x in df.columns:
            
            if x == y:
                p = bk_hist(df[y], theme = theme)
            else: 
                d = df[[y, x]].reset_index(drop = True)
                d.sort_values(by = y, inplace = True)
                p = bk_circle(d[x],d[y], theme = theme, alpha = alpha, regress = regress, **kwargs)
                
            p.toolbar.logo=None
            p.toolbar_location = None
            p.width = w_h
            p.height = w_h
            p.axis.visible = False
            if i ==0:
                p.add_layout(Title(text=y, align="center", text_font_size = '14px'), "left")
            r.append(p)
            i += 1
        rows.append(r)
    for p, col in zip(rows[-1], list(df.columns)):
        p.add_layout(Title(text=col, align="center", text_font_size = '14px'), "below")
    
    
    return layout(rows)