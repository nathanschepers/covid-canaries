import time
from datetime import datetime as dt

import pandas as pd
from bokeh.io import output_file, show
from bokeh.models import DatetimeTickFormatter, HoverTool, Span, Label, Panel, Tabs
from bokeh.palettes import Colorblind8
from bokeh.plotting import figure

#TODO: general cleanup
#TODO: fix NaN hover issue
#TODO: demographic data
#TODO: publish?
#TODO: put all these stupid dates somewhere in one place

output_file("../output/deaths-over-time.html", title='COVID Canarias')

# read the canarias COVID summary data
covid_df = pd.read_csv("../data/cases.csv", parse_dates=['date'])
covid_df = covid_df[covid_df['region'] == 'Canaries']

# set time bounds
covid_df = covid_df[(covid_df['date'] >= '2020-02-01') &
                    (covid_df['date'] <= '2020-04-19')]

# get deltas in number of deaths
covid_df = covid_df.merge(
    covid_df['deaths'].diff(),
    left_index=True, right_index=True, suffixes=['', '_covid']
).fillna(0)

# resample by week
covid_deaths = covid_df.resample('W', on='date').sum()

# read the canarias all-deaths data
all_deaths = pd.read_csv("../data/canarias_deaths.csv", parse_dates=['fecha_defuncion'])
young_deaths = pd.read_csv("../data/canarias_deaths.csv", parse_dates=['fecha_defuncion'])
old_deaths = pd.read_csv("../data/canarias_deaths.csv", parse_dates=['fecha_defuncion'])

all_deaths = all_deaths[(all_deaths['cod_sexo'] == 'all') &
                        (all_deaths['cod_gedad'] == 'all') &
                        (all_deaths['fecha_defuncion'] > '2019-8-11') &
                        (all_deaths['fecha_defuncion'] <= '2020-04-19')]

# resample by week
all_deaths = all_deaths.resample('W', on='fecha_defuncion').sum()
all_deaths["datestring"] = all_deaths.index.strftime("%b %d")
all_deaths["expected_delta"] = all_deaths['defunciones_observadas'] - all_deaths[
    'defunciones_esperadas']

young_deaths = young_deaths[(young_deaths['cod_sexo'] == 'all') &
                            (young_deaths['cod_gedad'] == 'menos_65') &
                            (young_deaths['fecha_defuncion'] > '2019-8-11') &
                            (young_deaths['fecha_defuncion'] <= '2020-04-19')]

# resample by week
young_deaths = young_deaths.resample('W', on='fecha_defuncion').sum()
young_deaths["datestring"] = young_deaths.index.strftime("%b %d")
young_deaths["expected_delta"] = young_deaths['defunciones_observadas'] - young_deaths[
    'defunciones_esperadas']

old_deaths = old_deaths[(old_deaths['cod_sexo'] == 'all') &
                        ((old_deaths['cod_gedad'] == '65_74') | (old_deaths['cod_gedad'] == 'mas_74')) &
                        (old_deaths['fecha_defuncion'] > '2019-8-11') &
                        (old_deaths['fecha_defuncion'] <= '2020-04-19')]

# resample by week
old_deaths = old_deaths.resample('W', on='fecha_defuncion').sum()
old_deaths["datestring"] = old_deaths.index.strftime("%b %d")
old_deaths["expected_delta"] = old_deaths['defunciones_observadas'] - old_deaths[
    'defunciones_esperadas']

# merge the data sets
merged_all = pd.merge(covid_deaths, all_deaths, left_index=True, right_index=True, how='outer')
merged_all['expected_plus_covid'] = merged_all['defunciones_esperadas'] + merged_all['deaths_covid']

merged_young = pd.merge(covid_deaths, young_deaths, left_index=True, right_index=True, how='outer')
merged_young['expected_plus_covid'] = merged_young['defunciones_esperadas'] + merged_young['deaths_covid']

merged_old = pd.merge(covid_deaths, old_deaths, left_index=True, right_index=True, how='outer')
merged_old['expected_plus_covid'] = merged_old['defunciones_esperadas'] + merged_old['deaths_covid']

# set up the figure
all_figure = figure(plot_width=1000, plot_height=400, tools='hover,pan,wheel_zoom,box_zoom,reset',
                    x_axis_type="datetime", toolbar_location="below", name='COVID - Canary Islands')

old_figure = figure(plot_width=1000, plot_height=400, tools='hover,pan,wheel_zoom,box_zoom,reset',
                    x_axis_type="datetime", toolbar_location="below", name='COVID - >65 Canary Islands')

young_figure = figure(plot_width=1000, plot_height=400, tools='hover,pan,wheel_zoom,box_zoom,reset',
                      x_axis_type="datetime", toolbar_location="below", name='COVID - <65 Canary Islands')

# set the palette
palette = Colorblind8

for figure in [all_figure, old_figure, young_figure]:
    hover = figure.select(dict(type=HoverTool))
    hover.tooltips = [
        ("Week ending", '@datestring'),
        ("Expected Deaths", "@defunciones_esperadas"),
        ("Observed Deaths", "@defunciones_observadas"),
        ("COVID Deaths", "@deaths_covid")
    ]
    all_figure.xaxis.formatter = DatetimeTickFormatter(
        hours=["%B"],
        days=["%B"],
        months=["%B"],
        years=["%B"],
    )

foo = [(all_figure, merged_all),
       (young_figure, merged_young),
       (old_figure, merged_old)]

for (figure, data) in foo:
    figure.line(x='index', y='defunciones_observadas', source=data,
                legend_label='Observed Deaths', name='Observed Deaths', color=palette[0], line_width=2)

    figure.line(x='index', y='defunciones_esperadas', source=data,
                legend_label='Expected Deaths', name='Expected Deaths', color=palette[1], line_width=2)

    # since the covid deaths isn't broken down by demographic, we will only display it where it is correct
    if (figure == all_figure):
        figure.line(x='index', y='expected_plus_covid', source=data,
                    legend_label='Covid Deaths', name='Covid Deaths', color='red', line_width=2)

# add lockdown span
lockdown_date = time.mktime(dt(2020, 3, 14, 0, 0, 0).timetuple()) * 1000
lockdown_start = Span(location=lockdown_date,
                      dimension='height', line_color=palette[3],
                      line_dash='dashed', line_width=3)
lockdown_label = Label(x=lockdown_date, y=10, y_units='screen', text='  Lockdown', text_font='helvetica',
                       text_font_size='9pt', text_color='#444444')

# add china span
china_date = time.mktime(dt(2020, 1, 11, 0, 0, 0).timetuple()) * 1000
china_start = Span(location=china_date,
                   dimension='height', line_color=palette[4],
                   line_dash='dashed', line_width=3)
china_label = Label(x=china_date, y=10, y_units='screen', text='  China', text_font='helvetica',
                    text_font_size='9pt', text_color='#444444')

# add canaries span
canaries_date = time.mktime(dt(2020, 2, 1, 0, 0, 0).timetuple()) * 1000
canaries_start = Span(location=canaries_date,
                      dimension='height', line_color=palette[5],
                      line_dash='dashed', line_width=3)
canaries_label = Label(x=canaries_date, y=10, y_units='screen', text='  Canaries', text_font='helvetica',
                       text_font_size='9pt', text_color='#444444')

for figure in [all_figure, young_figure, old_figure]:
    figure.add_layout(lockdown_start)
    figure.add_layout(lockdown_label)
    figure.add_layout(china_start)
    figure.add_layout(china_label)
    figure.add_layout(canaries_start)
    figure.add_layout(canaries_label)
    figure.legend.location = 'top_left'
    figure.legend.click_policy = "hide"


# create tabs
panels = []
for figure in [all_figure, old_figure, young_figure]:

    panels.append(Panel(child=figure, title=figure.name))

tabbed_plot = Tabs(tabs=panels)

# create the plot
show(tabbed_plot)

