# -*- coding: utf-8 -*-

import pandas as pd
from eda.line import bk_line
from rpy2.robjects import r, pandas2ri
import numpy as np
from rpy2.robjects.packages import importr
from eda.autocorrelation import autocor
from bokeh.io import curdoc
from bokeh.layouts import gridplot


def decompose(series, frequency, s_window = 'periodic', log = False, theme = False, **kwargs):
    '''
    Decompose a time series into seasonal, trend and irregular components using loess, 
    acronym STL.
    https://www.rdocumentation.org/packages/stats/versions/3.4.3/topics/stl
    
    params:
        series: a time series
        
        frequency: the number of observations per “cycle” 
                   (normally a year, but sometimes a week, a day or an hour)
                   https://robjhyndman.com/hyndsight/seasonal-periods/
        
        s_window: either the character string "periodic" or the span 
                 (in lags) of the loess window for seasonal extraction, 
                 which should be odd and at least 7, according to Cleveland 
                 et al.
        
        log:    boolean.  take log of series
        
        theme:  a bokeh theme
        
        **kwargs:  See other params for stl at 
           https://www.rdocumentation.org/packages/stats/versions/3.4.3/topics/stl
    '''
        
    df = pd.DataFrame()
    df['date'] = series.index
    if log: series = series.pipe(np.log)
    s = [x for x in series.values]
    length = len(series)
    s = r.ts(s, frequency=frequency)
    decomposed = [x for x in r.stl(s, s_window).rx2('time.series')]
    df['observed'] = series.values
    df['trend'] = decomposed[length:2*length]
    df['seasonal'] = decomposed[0:length]
    df['residuals'] = decomposed[2*length:3*length]
    return df
        

def stl_plot(series, frequency, title = '', theme = False, **kwargs):
    df = decompose(series, frequency = frequency)
    plot_list = []
    x = df['date']
    columns = ['observed', 'trend', 'seasonal', 'residuals']
    for column in columns:
        y = df[column]
        p = bk_line(x,y, title = title, x_axis_type = 'datetime', **kwargs)
        p.yaxis.axis_label = column
        plot_list.append(p)
    p = df['residuals'].pipe(autocor)
    p.title.visible = False
    p.yaxis.axis_label = 'residual autocorrelation'
    plot_list.append(p)
    p = gridplot(plot_list, ncols=1, plot_height = 225, plot_width = 800)
    if theme:
        doc = curdoc()
        doc.theme = theme
        doc.add_root(p)
    return p