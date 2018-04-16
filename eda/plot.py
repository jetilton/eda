# -*- coding: utf-8 -*-

from eda.line import bk_line
from eda.control import control_plot
from eda.matrix import bk_circle, bk_hist, bk_matrix
from eda.autocorrelation import autocor
from eda.stl import stl_plot
from bokeh.palettes import all_palettes
from eda.theme import theme
colors = all_palettes['Colorblind'][8]

#theme = Theme(json = yaml.safe_load(open('eda/theme.yml')))
