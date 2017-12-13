# -*- coding: utf-8 -*-

import pandas as pd
from bokeh.plotting import figure, show
from math import pi
import seaborn as sns
import matplotlib.pyplot as plt
from eda.plots import colors

def df_freq(series, freq = 'year'):
    """
    
    series: a pandas series (time series)
    freq: the frquency the data is broken into
    
    a function that takes in a pandas (time) series and returns a dataframe 
    with columns for the specified frequency.  It is intended to be used
    for plotting functions such as the below boxplot
    """
    freq_dict = {
                'year':'A',
                'month': 'M',
                'week': 'W'
                 }
    
    series = series[~((series-series.mean()).abs()>3.5*series.std())]
    groups = series.groupby(pd.Grouper(freq = freq_dict[freq]))
    df = pd.DataFrame()
    names = []
    
    for name, group in groups:
        name_dict = {
                    'year':name.year,
                    'month': name.month,
                    'week': name.week
                     }
        try:
            n = pd.DataFrame(group.values)
            df = pd.concat([df, n], axis = 1)
            names.append(str(name_dict[freq]))
        except:
            print(name)
            continue
    df.columns = names
    return df



def boxplot(series, freq='year', figsize = (15,8), grid = False):
    """
    series: a pandas series (time series)
    freq: the frquency the data is broken into
    figsize: Size of the matplotlib plt
    grid: boolean 
    """
    df = df_freq(series, freq = freq)
    df.boxplot(figsize= figsize, grid = grid)

def boxplot_data(series):
    """
    http://www.itl.nist.gov/div898/handbook/prc/section1/prc16.htm
    """
    d = pd.Series()
    s = series.dropna()
    #s = s[~((s-s.mean()).abs()>5*s.std())]
    d['q1'] = s.quantile(.25)
    d['q2'] = s.quantile(.5)
    d['q3'] = s.quantile(.75)
    d['iq'] = d['q3']-d['q1']
    d['lower_inner_fence'] = d['q1'] - 1.5 * d['iq']
    d['upper_inner_fence'] = d['q3'] + 1.5 * d['iq']
    d['lower_outer_fence'] = d['q1'] - 3 * d['iq']
    d['upper_outer_fence'] = d['q3'] + 3 * d['iq']
    d['upper_whisker'] = series.mean()+3*series.std()
    d['lower_whisker'] = series.mean()-3*series.std()
    outliers= pd.s[(s>d['upper_outer_fence']) | (s<d['lower_outer_fence'])]
    return (d, outliers)
    
    
def ts_box_data(series, freq = 'year'):
    
    freq_dict = {
                'year':'A',
                'month': 'M',
                'week': 'W'
                 }
    
    
    groups = series.groupby(pd.Grouper(freq = freq_dict[freq]))
    df = pd.DataFrame()
    names = []
    ol = []
    for name, group in groups:
        name_dict = {
                    'year':name.year,
                    'month': name.month,
                    'week': name.week
                     }
        try:
            s = pd.Series(group.values)
            s = s[~((s-s.mean()).abs()>4*s.std())]
            d,outliers = boxplot_data(s)
            ol_df = pd.DataFrame({'outliers':outliers})
            ol_df['date'] = str(name_dict[freq])
            ol.append(ol_df)
            df = df.append(d, ignore_index = True)
            names.append(str(name_dict[freq]))
        except:
            print(name)
            continue
    df['date'] = names
    df.set_index('date', inplace = True)
    #df['date'] = pd.to_datetime(df['date'])
    ol = pd.concat(ol)
    #ol['date'] = pd.to_datetime(ol['date'])
    return (df, ol)


def bk_bx_plt(data, title='', freq = '', w = 1000, h = 400):
    TOOLS = "pan,wheel_zoom,box_zoom,reset,save"
    if freq:
        df, outliers = data.pipe(ts_box_data, freq = freq) 
        p = figure(x_range=[str(x) for x in list(df.index)], tools=TOOLS, plot_width=w, plot_height=h, title = title)
    else:
        df, outliers = data.pipe(box_data)
        p = figure(x_range=list(df.index), tools=TOOLS, plot_width=w, plot_height=h, title = title)
        
    p.xaxis.major_label_orientation = pi/4
    #whiskers
    p.segment(df.index, df['upper_whisker'], df.index,df['lower_whisker'], color="black")
    #box
    p.vbar(x = df.index, width = .5, bottom = df['q1'], top = df['q3'], fill_color=colors[0], line_color="black")
    #median
    p.vbar(x = df.index, width = .5, bottom = df['q2']-.01, top = df['q2']+.01, fill_color="black", line_color="black")
    #outliers
    if outliers.values:
        
        p.circle(x = [str(x) for x in outliers.index], y = list(outliers.values), size=10, color=colors[1])
    
    p.xgrid.visible = False
    p.ygrid.visible = False
    #p.xaxis.visible = False
    p.outline_line_width  = 0
    p.outline_line_alpha = 0.0
    return p


def box_data(df):
    melted = df.melt()
    groups = melted.groupby(by = 'variable')
    
    df = pd.DataFrame()
    names = []
    ol = []
    for name, group in groups:
        
        s = pd.Series(pd.DataFrame(group.values).iloc[:,1])
        
        s = s[~((s-s.mean()).abs()>5*s.std())]
        try:
            
            d,outliers = boxplot_data(s)
            ol_df = pd.DataFrame({'outliers':outliers})
            ol_df['variable'] = name
            ol.append(ol_df)
            df = df.append(d, ignore_index = True)
            names.append(name)
        except:
            print(name)
            continue
    df['variable'] = names
    df.set_index('variable', inplace = True)
    #df['date'] = pd.to_datetime(df['date'])
    ol = pd.concat(ol)
    #ol['date'] = pd.to_datetime(ol['date'])
    return (df, ol)