from bokeh.io import output_file, show
from bokeh.models import NumeralTickFormatter
from bokeh.plotting import figure


import pandas as pd

islands_df = pd.read_csv("../data/islands.csv")
islands = islands_df.sort_values("population", ascending=False)
names = islands["name"].to_list()
populations = islands["population"].to_list()

output_file("../output/island-populations.html")

colour_list = ['red', 'blue', 'blue', 'blue', 'blue', 'blue', 'blue', 'blue']

p = figure(x_range=names, plot_height=250, title="Island Populations",
           toolbar_location=None, tools="")
p.vbar(x=names, top=populations, width=0.9, color=colour_list)
p.xgrid.grid_line_color = None
p.y_range.start = 0
p.yaxis.formatter = NumeralTickFormatter(format="0,0")

show(p)
