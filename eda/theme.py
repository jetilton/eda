# -*- coding: utf-8 -*-
from bokeh.themes import Theme
theme = Theme(json={
    'attrs': {
        'Figure': {
            'background_fill_color': '#f0f0f0',
            'border_fill_color': 'white',
            'outline_line_color': 'white',
            'outline_line_width' : 0,
            'outline_line_alpha' : 0.0,
            'width':1800
            },
        'Axis': {
            'axis_line_color': "white",
            'axis_label_text_color': "black",
            'axis_label_standoff':30,
            'axis_label_text_font_size': '15pt',
            'axis_label_text_font_style': 'bold',
            'major_label_text_color': "black",
            'major_label_text_font_size': '10pt',
            'major_label_text_font_style' : 'bold',
            'major_tick_line_color': "white",
            'minor_tick_line_color': "white",
            'minor_tick_line_color': "white",
            },
        'Grid': {
            'grid_line_width': 2,
            'grid_line_dash': 'solid',
            'grid_line_alpha': 1,
            'grid_line_color': 'white'
            },
        'Circle': {
            
            'size': 10,
            },
        'Line':{
            #'line_width': 5,
            'line_join' : 'miter',
            'line_cap':'round'
        },
        'Segment':{
            'line_width': 3
            
        },
        'Vbar':{
            'line_width':10
        },
            
        'Title': {
            'text_color': "black",
            'text_font_size' : '25pt'
            },
        'Fill':{
            'fill_color': 'orange'
            
        }
        }
    })