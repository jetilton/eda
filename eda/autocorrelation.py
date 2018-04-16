# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np
from bokeh.plotting import figure
from bokeh.io import curdoc



def acf(series:pd.core.series.Series) -> pd.core.series.Series:
    """
    Autocorrelation, also known as serial correlation, is the correlation 
    of a signal with a delayed copy of itself as a function of delay. 
    Informally, it is the similarity between observations as a function 
    of the time lag between them. The analysis of autocorrelation is a 
    mathematical tool for finding repeating patterns, such as the presence 
    of a periodic signal obscured by noise, or identifying the missing 
    fundamental frequency in a signal implied by its harmonic frequencies. 
    It is often used in signal processing for analyzing functions or series 
    of values, such as time domain signals.
    
    
    params:
        series: a time series
    
    returns:
        acf_coeffs: the autocorrelation at lag (index)
    
    """
    n = len(series)
    data = np.asarray(series)
    mean = np.mean(data)
    c0 = np.sum((data - mean) ** 2) / float(n)
    def r(h):
        acf_lag = ((data[:n - h] - mean) * (data[h:] - mean)).sum() / float(n) / c0
        return round(acf_lag, 3)
    x = np.arange(n) # Avoiding lag 0 calculation
    acf_coeffs = pd.Series(map(r, x)).round(decimals = 3)
    acf_coeffs = acf_coeffs + 0
    return acf_coeffs


def significance(series):
    
    n = len(series)
    z95 = 1.959963984540054 / np.sqrt(n)
    z99 = 2.5758293035489004 / np.sqrt(n)
    return(z95,z99)
    
def autocor(series:pd.core.series.Series, theme = False, title = 'Time Series Auto-Correlation'):
    """
    Autocorrelation plots are often used for checking randomness in time series. 
    This is done by computing autocorrelations for data values at varying time lags. 
    If time series is random, such autocorrelations should be near zero for any and 
    all time-lag separations. If time series is non-random then one or more of the 
    autocorrelations will be significantly non-zero. The horizontal lines displayed 
    in the plot correspond to 95% and 99% confidence bands. The dashed line is 99% 
    confidence band.
    
     params:
        series: a time series
    
    returns:
        p: a bokeh plotting figure of the series' autocorrelation
    
    
    """
     
    x = pd.Series(range(1, len(series)+1), dtype = float)
    z95, z99 = significance(series)
    y = acf(series)
    p = figure(title=title, plot_width=1000,
               plot_height=500, x_axis_label="Lag", y_axis_label="Autocorrelation")
    p.line(x, z99, line_dash='dashed', line_color='grey', line_width = 2)
    p.line(x, z95, line_color = 'grey', line_width = 2)
    p.line(x, y=0.0, line_color='black', line_width = 2)
    p.line(x, z99*-1, line_dash='dashed', line_color='grey', line_width = 2)
    p.line(x, z95*-1, line_color = 'grey', line_width = 2)
    p.line(x, y)
    if theme:
        doc = curdoc()
        doc.theme = theme
        doc.add_root(p)
    return p