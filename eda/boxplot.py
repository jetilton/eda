# -*- coding: utf-8 -*-

import pandas as pd
from bokeh.plotting import figure
from math import pi
from bokeh.palettes import all_palettes
from bokeh.io import curdoc
colors = all_palettes['Colorblind'][8]



def boxplot_data(series):
    """
    params:
        series: a pandas series
    
    returns:
        d: series with values to produce boxplots
        outliers: new series contianing the outliers
    
    
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
    outliers= s[(s>d['upper_outer_fence']) | (s<d['lower_outer_fence'])]
    return (d, outliers)

def box_data(df):
    """
    box_data calculates boxplot values for each column in a pandas df
    
    params:
        df: pandas dataframe 
    returns:
        df: Dataframe of boxplot data
        ol: outliers for data
    
    """
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
    
    #df['date'] = pd.to_datetime(df['date'])
    ol = pd.concat(ol)
    #ol['date'] = pd.to_datetime(ol['date'])
    return (df, ol)




def ts_box_data(series, freq = 'A'):
    """
    ts_box_data groups data into a specified frequency and returns a
    dataframe of boxplot data for each group
    
    params:
        series: a time series
        freq: a frequency.  Available frequencies are located 
        at the website below
        http://pandas.pydata.org/pandas-docs/stable/timeseries.html#offset-aliases
        
    returns:
        df: a dataframe of grouped boxplot data
        ol: a dataframe of the outliers for each group
        
    """

    groups = series.groupby(pd.Grouper(freq = freq))
    df = pd.DataFrame()
    names = []
    ol = []
    for name, group in groups:
#        name_dict = {
#                    'year':name.year,
#                    'month': name.month,
#                    'week': name.week
#                     }
        try:
            s = pd.Series(group.values)
            s = s[~((s-s.mean()).abs()>4*s.std())]
            d,outliers = boxplot_data(s)
            ol_df = pd.DataFrame({'outliers':outliers})
            ol_df['date'] = name
            ol.append(ol_df)
            df = df.append(d, ignore_index = True)
            names.append(name)
        except:
            print(name)
            continue
    df['date'] = names
    df.set_index('date', inplace = True)
    #df['date'] = pd.to_datetime(df['date'])
    ol = pd.concat(ol)
    ol.set_index('date', inplace = True)
    #ol['date'] = pd.to_datetime(ol['date'])
    return (df, ol)




def box_plot(x_col_name, df, outliers = False, title='',theme = False):
    x = [str(x) for x in df[x_col_name]]
    TOOLS = "pan,wheel_zoom,box_zoom,reset,save"
    
    p = figure(x_range=x, tools=TOOLS, title = title)    
    p.xaxis.major_label_orientation = pi/4
    #whiskers
    p.segment(x, df['upper_whisker'], x,df['lower_whisker'], color="black")
    #box
    p.vbar(x = x, width = .5, bottom = df['q1'], top = df['q3'], fill_color=colors[:len(df)], line_color="black")
    #median
    p.vbar(x = x, width = .5, bottom = df['q2']-.01, top = df['q2']+.01, fill_color="black", line_color="black")
    #outliers
    if not outliers.empty:
        
        p.circle(x = outliers.index, y = outliers.values[0], size=5, color=colors[1])
    
    if theme:
        doc = curdoc()
        doc.theme = theme
        doc.add_root(p)   
    
    return p