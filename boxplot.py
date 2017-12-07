# -*- coding: utf-8 -*-

import pandas as pd
from bokeh.plotting import figure, show
from math import pi
import seaborn as sns
import matplotlib.pyplot as plt

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
    s = s[~((s-s.mean()).abs()>3.5*s.std())]
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
    outliers= list(s[s>d['upper_outer_fence']]) + list(s[s<d['lower_outer_fence']])
    return(d,outliers)
    
    
def bokeh_df_box_data(series, freq = 'year'):
    
    freq_dict = {
                'year':'A',
                'month': 'M',
                'week': 'W'
                 }
    
    series = series[~((series-series.mean()).abs()>3.5*series.std())]
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
    #df['date'] = pd.to_datetime(df['date'])
    ol = pd.concat(ol)
    #ol['date'] = pd.to_datetime(ol['date'])
    return (df, ol)


def bokeh_ts_bx_plt(series, title, freq = 'year'):
    df,ol_df = series.pipe(bokeh_df_box_data, freq = freq) 
    TOOLS = "pan,wheel_zoom,box_zoom,reset,save"
    p = figure(x_range=[str(x) for x in df['date']], tools=TOOLS, plot_width=1000, plot_height=480, title = title)
    p.xaxis.major_label_orientation = pi/4
    #whiskers
    p.segment(df.date, df['upper_whisker'], df.date,df['lower_whisker'], color="black")
    #box
    p.vbar(x = df['date'], width = .5, bottom = df['q1'], top = df['q3'], fill_color="#D5E1DD", line_color="black")
    #median
    p.vbar(x = df['date'], width = .5, bottom = df['q2']-.01, top = df['q2']+.01, fill_color="black", line_color="black")
    #outliers
    p.circle(x = ol_df['date'], y = ol_df['outliers'], size=5, color="#F2583E", alpha=0.5)
    
    p.xgrid.visible = False
    p.ygrid.visible = False
    #p.xaxis.visible = False
    p.outline_line_width  = 0
    p.outline_line_alpha = 0.0
    return p


def simple_boxplot(df, title):
    meta =df.__dict__['metadata']
    plot_dict = {}
    for k,v in meta.items():
        try:
            plot_dict[v['units']].append((k, v['path']))
        except:
            plot_dict.update({v['units']:[(k, v['path'])]})
    for k,v in plot_dict.items():
        data = [df[x[0]].dropna() for x in v]
        names = [x[1] for x in v]
        names = [' '.join(x.split('.')[0:2]) for x in names]
        f, ax = plt.subplots()
        ax.set_ylabel(k)
        sns.boxplot(data = data).set(xticklabels=names, title = title)
