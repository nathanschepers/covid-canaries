import time
from datetime import datetime as dt

import pandas as pd
from bokeh.io import output_file, show
from bokeh.models import DatetimeTickFormatter, HoverTool, Span, Label, Band, ColumnDataSource
from bokeh.palettes import Colorblind8
from bokeh.plotting import figure

# TODO: fix NaN hover issue

output_file("../output/deaths-over-time.html", title='COVID Canarias')

# read the canarias COVID summary data
covid_df = pd.read_csv("../data/canarias_arcgis.csv", parse_dates=['date'])
covid_df = covid_df[covid_df['region'] == 'Canaries']

# set time bounds
covid_df = covid_df[(covid_df['date'] >= '2020-02-01')]

# get deltas in number of deaths
covid_df = covid_df.merge(
    covid_df['deaths'].diff(),
    left_index=True, right_index=True, suffixes=['', '_covid']
).fillna(0)

# here we could resample the data if we want to see it by week or month
covid_deaths = covid_df.resample('D', on='date').sum()

all_deaths = pd.read_csv("https://momo.isciii.es/public/momo/data", parse_dates=['fecha_defuncion'])

all_deaths = all_deaths[(all_deaths['cod_sexo'] == 'all') &
                        (all_deaths['cod_gedad'] == 'all') &
                        (all_deaths['cod_ambito'] == 'CN') &
                        (all_deaths['fecha_defuncion'] > '2019-12-01')]

all_deaths = all_deaths.resample('D', on='fecha_defuncion').sum()
all_deaths["datestring"] = all_deaths.index.strftime("%b %d")

# merge the data sets
merged_all = pd.merge(covid_deaths, all_deaths, left_index=True, right_index=True, how='outer')
merged_all['expected_plus_covid'] = merged_all['defunciones_esperadas'] + merged_all['deaths_covid']

# set up the figure
all_figure = figure(plot_width=1000, plot_height=400, tools='hover,pan,wheel_zoom,box_zoom,reset',
                    x_axis_type="datetime", toolbar_location="below", name='COVID - Canary Islands',
                    y_range=(0,
                             (max(merged_all['defunciones_esperadas_q99']) + 25)))

# set the palette
palette = Colorblind8

# set up hover tooltips
hover = all_figure.select(dict(type=HoverTool))
hover.tooltips = [
    ("Date", '@datestring'),
    ("Expected Deaths", "@defunciones_esperadas"),
    ("Observed Deaths", "@defunciones_observadas"),
    ("COVID Deaths", "@deaths_covid")
]
all_figure.xaxis.formatter = DatetimeTickFormatter(
    hours=["%B %d"],
    days=["%B %d"],
    months=["%B %d"],
    years=["%B %d"],
)

# add lines
all_figure.line(x='index', y='defunciones_observadas', source=merged_all,
                legend_label='Observed Deaths', name='Observed Deaths', color=palette[0], line_width=2)

all_figure.line(x='index', y='defunciones_esperadas', source=merged_all,
                legend_label='Expected Deaths', name='Expected Deaths', color=palette[1], line_width=2)

all_figure.line(x='index', y='expected_plus_covid', source=merged_all,
                legend_label='Covid Deaths', name='Covid Deaths', color='red', line_width=2)

# create lockdown span
lockdown_date = time.mktime(dt(2020, 3, 14, 0, 0, 0).timetuple()) * 1000
lockdown_start = Span(location=lockdown_date,
                      dimension='height', line_color=palette[3],
                      line_dash='dashed', line_width=3)
lockdown_label = Label(x=lockdown_date, y=10, y_units='screen', text=' Lockdown', text_font='helvetica',
                       text_font_size='9pt', text_color='#444444')

# create china span
china_date = time.mktime(dt(2020, 1, 11, 0, 0, 0).timetuple()) * 1000
china_start = Span(location=china_date,
                   dimension='height', line_color=palette[4],
                   line_dash='dashed', line_width=3)
china_label = Label(x=china_date, y=10, y_units='screen', text=' China', text_font='helvetica',
                    text_font_size='9pt', text_color='#444444')

# create canaries span
canaries_date = time.mktime(dt(2020, 2, 1, 0, 0, 0).timetuple()) * 1000
canaries_start = Span(location=canaries_date,
                      dimension='height', line_color=palette[5],
                      line_dash='dashed', line_width=3)
canaries_label = Label(x=canaries_date, y=10, y_units='screen', text=' Spain', text_font='helvetica',
                       text_font_size='9pt', text_color='#444444')

# create and add bands
band_all = Band(base='index', lower='defunciones_esperadas_q99', upper='defunciones_esperadas_q01',
                source=ColumnDataSource(merged_all), level='underlay', fill_alpha=1.0, line_width=1, line_color='black')
all_figure.add_layout(band_all)

# add spans and legend
all_figure.add_layout(lockdown_start)
all_figure.add_layout(lockdown_label)
all_figure.add_layout(china_start)
all_figure.add_layout(china_label)
all_figure.add_layout(canaries_start)
all_figure.add_layout(canaries_label)
all_figure.legend.location = 'top_left'
all_figure.legend.click_policy = "hide"

# create the plot
show(all_figure)
