import time
from datetime import datetime as dt

from bokeh.io import output_file, show
from bokeh.models import DatetimeTickFormatter, HoverTool, ColumnDataSource, Panel, Tabs, Span, Label
from bokeh.plotting import figure
from bokeh.palettes import Colorblind8

import pandas as pd

cases_df = pd.read_csv("../data/cases_canarias.csv", parse_dates=['date'])
cases_df["datestring"] = cases_df["date"].dt.strftime("%b %d")

output_file("../output/cases-over-time.html")

island_data = [{'name': 'All Islands',
                'data': ColumnDataSource(cases_df.loc[cases_df['region'] == 'Canaries']),
                'colour': 7},
               {'name': 'Tenerife',
                'data': ColumnDataSource(cases_df.loc[cases_df['region'] == 'Tenerife']),
                'colour': 6},
               {'name': 'Gran Canaria',
                'data': ColumnDataSource(cases_df.loc[cases_df['region'] == 'Gran Canaria']),
                'colour': 5},
               {'name': 'Lanzarote',
                'data': ColumnDataSource(cases_df.loc[cases_df['region'] == 'Lanzarote']),
                'colour': 4},
               {'name': 'Fuerteventura',
                'data': ColumnDataSource(cases_df.loc[cases_df['region'] == 'Fuerteventura']),
                'colour': 3},
               {'name': 'La Palma',
                'data': ColumnDataSource(cases_df.loc[cases_df['region'] == 'La Palma']),
                'colour': 2},
               {'name': 'La Gomera',
                'data': ColumnDataSource(cases_df.loc[cases_df['region'] == 'La Gomera']),
                'colour': 1},
               {'name': 'El Hierro',
                'data': ColumnDataSource(cases_df.loc[cases_df['region'] == 'El Hierro']),
                'colour': 0}]

# create and configure all of the figures
figures = []
for island in island_data:
    figures.append(figure(plot_width=1000, plot_height=400, tools='hover,pan,wheel_zoom,box_zoom,reset',
                          x_axis_type="datetime", toolbar_location="below", name=island['name']))

    hover = figures[-1].select(dict(type=HoverTool))
    hover.tooltips = [
        ("Island", "$name"),
        ("Date", '@datestring'),
        ("Active Cases", "@active"),
    ]

    figures[-1].xaxis.formatter = DatetimeTickFormatter(
        hours=["%d %B %Y"],
        days=["%d %B %Y"],
        months=["%d %B %Y"],
        years=["%d %B %Y"],
    )

# set the palette
palette = Colorblind8

# add all island data to first figure
for island in island_data:
    figures[0].line(x='date', y='active', source=island['data'], legend_label=island['name'], name=island['name'],
                    color=palette[island['colour']], line_width=2)

# add lockdown span to first figure
lockdown_date = time.mktime(dt(2020, 3, 14, 0, 0, 0).timetuple())*1000
lockdown_start = Span(location=lockdown_date,
                      dimension='height', line_color='red',
                      line_dash='dashed', line_width=3)
lockdown_label = Label(x=lockdown_date, y=300, y_units='screen', text='  Lockdown', text_font='helvetica',
                       text_font_size='9pt', text_color='#444444')
figures[0].add_layout(lockdown_start)
figures[0].add_layout(lockdown_label)
figures[0].legend.location = 'top_left'
figures[0].legend.click_policy = "hide"

# add data to remaining figures
for x in range(1, 8):
    island = island_data[x]
    figures[x].line(x='date', y='active', source=island['data'], legend_label=island['name'], name=island['name'],
                    color=palette[island['colour']], line_width=2)
    figures[x].legend.location = 'top_left'
    figures[x].legend.click_policy = "hide"

# create tabs
panels = []
for figure in figures:

    panels.append(Panel(child=figure, title=figure.name))

tabbed_plot = Tabs(tabs=panels)

# create the plot
show(tabbed_plot)
