# -*- coding: utf-8 -*-


from bokeh.plotting import figure
from bokeh.io import curdoc

def bk_line(x,y, theme = False, title = '', x_axis_type = 'datetime', **kwargs):
    """
    Simple Line plot
    """
    
    p = figure(title = title, x_axis_type=x_axis_type, **kwargs)
    p.line(x, y)
    if theme:
        doc = curdoc()
        doc.theme = theme
        doc.add_root(p)
    return p

