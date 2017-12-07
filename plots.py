# -*- coding: utf-8 -*-
from bokeh.io import reset_output
from bokeh.models import Legend, DatetimeTickFormatter
from bokeh.plotting import figure
import matplotlib.pyplot as plt
from bokeh.layouts import gridplot
from bokeh.palettes import all_palettes
import numpy as np
import pandas as pd
from boxplot import boxplot_data
from bokeh.io import show

colors = all_palettes['Colorblind'][8]


def bok_sp(plot_dict, **kwargs):
    if kwargs: figsize = kwargs['figsize']
    else: figsize = (800,400)
    plot_list = []
    plot_width, plot_height = figsize
    i = 0
    for unit,values in plot_dict.items():
        p = figure(plot_width=plot_width, plot_height=plot_height)
        p.xaxis.formatter = DatetimeTickFormatter()
        glyph_list = []
        column_list = []
        for data in values:
            column_name,x,y = data 
            g = p.line(x = x, y = y, line_width = 2, color = colors[i])
            i += 1
            column_list.append(column_name)
            glyph_list.append(g)
        items = [(column, [glyph]) for column,glyph in zip(column_list, glyph_list)]
        legend = Legend(items = items, location = (40,0))
        p.add_layout(legend, 'below')
        plot_list.append(p)
    grid = [[p] for p in plot_list]
    p = gridplot(grid)
    reset_output()  
    return p

def mlib_sp(plot_dict, **kwargs):
    if kwargs: figsize = kwargs['figsize']
    else: figsize = (15,10)
    plt.figure(figsize=figsize )
    p = 211
    for unit,values in plot_dict.items():
        plt.subplot(p)
        for data in values:
           
            column_name,x,y = data 
            plt.plot(x,y, label = column_name)
            plt.legend(bbox_to_anchor=(1.04,0), loc=3, borderaxespad=0)

        p += 1

def create_plot_dict(df):
    plot_dict = {}
    for column,value in df.__dict__['metadata'].items():
        
        column_name = value['path']
        units = value['units']
        
        x = df[column].index
        y = df[column].values
        try: 
            plot_dict[units].append((column_name,x,y))
        except:
            plot_dict.update({units:[(column_name,x,y)]})
    return plot_dict

def simple_plot(df, bok = False, **kwargs):
    plot_dict = create_plot_dict(df)
    if bok:
       return bok_sp(plot_dict, **kwargs) 
    else:
       mlib_sp(plot_dict, **kwargs)

def bok_circle(x,y):
    p = figure(plot_width=200, plot_height=200)
    p.circle(x, y, size=5, color="navy", alpha=0.2)
    return p
    
def bok_lag(series, lags):
    plot_list = []
    x = series
    for lag in range(1, lags+1):
        y = x.shift(lag)
        p = bok_circle(x,y)
        p.xaxis.axis_label = 't+1'
        p.yaxis.axis_label = 't-'+str(lag)
        plot_list.append(p)
    p = gridplot(plot_list, ncols=4, plot_width=200, plot_height=200)
    return p

def acf(series):
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
    
def bok_autocor(series):
    x = pd.Series(range(1, len(series)+1), dtype = float)
    z95, z99 = significance(series)
    y = acf(series)
    p = figure(title='Time Series Auto-Correlation', plot_width=1000,
               plot_height=500, x_axis_label="Lag", y_axis_label="Autocorrelation")
    p.line(x, z99, line_dash='dashed', line_color='grey')
    p.line(x, z95, line_color = 'grey')
    p.line(x, y=0.0, line_color='black')
    p.line(x, z99*-1, line_dash='dashed', line_color='grey')
    p.line(x, z95*-1, line_color = 'grey')
    p.line(x, y, line_width=2)
    p.xgrid.visible = False
    p.ygrid.visible = False
    p.outline_line_width  = 0
    p.outline_line_alpha = 0.0
    return p

def bok_line(x,y):
    p = figure(plot_width=1000, plot_height=300, x_axis_type = 'datetime')
    p.line(x, y, color=colors[0])
    p.xgrid.visible = False
    p.ygrid.visible = False
    p.outline_line_width  = 0
    p.outline_line_alpha = 0.0
    return p
    
def bok_decompose(df):
    plot_list = []
    x = df['date']
    columns = ['observed', 'trend', 'seasonal', 'residuals']
    for column in columns:
        y = df[column]
        p = bok_line(x,y)
        p.xaxis.axis_label = 'date'
        p.yaxis.axis_label = column
        plot_list.append(p)
    p = df['residuals'].pipe(bok_autocor)
    p.title.visible = False
    p.yaxis.axis_label = 'residual autocorrelation'
    plot_list.append(p)
    p = gridplot(plot_list, ncols=1, plot_height = 225, plot_width = 800)
    return p

def new_plot(series):
    x = series.index
    y = series.values
    quantiles,outliers = boxplot_data(series)
    p = bok_line(x,y)
    p.line(x, quantiles['lower_outer_fence'], line_dash='dashed', line_color='grey')
    p.line(x, quantiles['q1'], line_color = 'grey')
    p.line(x, quantiles['q2'], line_color='black')
    p.line(x, quantiles['upper_outer_fence'], line_dash='dashed', line_color='grey')
    p.line(x, quantiles['q3'], line_color = 'grey')
    return p 
   
    
    
    
    