from bokeh.io import output_file, show
from bokeh.models import NumeralTickFormatter
from bokeh.plotting import figure

import pandas as pd

cases_df = pd.read_csv("../data/cases.csv", parse_dates=['date'])

cases_today = cases_df.loc[cases_df['date'] == '2020-4-5'].sort_values("active", ascending=False)
names = cases_today['region'].to_list()
cases = cases_today['active'].to_list()

output_file("../output/new-cases-today.html")

colour_list = ['red', 'blue', 'blue', 'blue', 'blue', 'blue', 'blue', 'blue']

p = figure(x_range=names, plot_height=250, title="New Cases Today",
           toolbar_location=None, tools="")
p.vbar(x=names, top=cases, width=0.9, color=colour_list)
p.xgrid.grid_line_color = None
p.y_range.start = 0
p.yaxis.formatter = NumeralTickFormatter(format="0,0")

show(p)
