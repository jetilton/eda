# -*- coding: utf-8 -*-


from bokeh.plotting import figure
from bokeh.io import curdoc
from bokeh.models import Legend
from eda.boxplot import boxplot_data


def control_plot(series, theme = False, title = '', x_axis_type = 'datetime', **kwargs):
    """
    The control chart is a graph used to study how a process changes over time. 
    Data are plotted in time order. A control chart always has a central line for 
    the average, an upper line for the upper control limit and a lower line for  
    the lower control limit. These lines are determined from historical data. 
    By comparing current data to these lines, you can draw conclusions about 
    whether the process variation is consistent (in control) or is unpredictable 
    (out of control, affected by special causes of variation).
    
    When to Use a Control Chart
    
     - When controlling ongoing processes by finding and correcting problems as they occur.
     - When predicting the expected range of outcomes from a process.
     - When determining whether a process is stable (in statistical control).
     - When analyzing patterns of process variation from special causes (non-routine events) or common causes (built into the process).
     - When determining whether your quality improvement project should aim to prevent specific problems or to make fundamental changes to the process.
    
    
    source: http://asq.org/learn-about-quality/data-collection-analysis-tools/overview/control-chart.html
    """
    
    
    
    p = figure(title = title, x_axis_type=x_axis_type, **kwargs)
    x = series.index
    y = series.values
    quantiles,outliers = boxplot_data(series)
    s3 = p.line(x, series.mean()+3*series.std(), line_color = 'red', line_width = 2)
    s2 = p.line(x, series.mean()+2*series.std(), line_color = 'grey', line_width = 2)
    s1 = p.line(x, series.mean()+series.std(), line_dash='dashed', line_color='grey', line_width = 2)
    m = p.line(x, series.mean(), line_color='black', line_width = 2)
    p.line(x, series.mean()-series.std(), line_dash='dashed', line_color='grey', line_width = 2)
    p.line(x, series.mean()-2*series.std(), line_color = 'grey', line_width = 2)
    p.line(x, series.mean()-3*series.std(), line_color = 'red', line_width = 2)
    p.line(x, y)
    legend = Legend(items=[
    ('3 standard deviations' , [s3]),
    ('2 standard deviations' , [s2]),
    ('1 standard deviations' , [s1]),
    ("Mean" , [m])], location=(0, 0))
    
    p.add_layout(legend, 'below')
    p.legend.orientation = "horizontal"
    if theme:
        doc = curdoc()
        doc.theme = theme
        doc.add_root(p)
    
    return p 


