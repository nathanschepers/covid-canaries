import time
from datetime import datetime as dt, datetime
import json

import pandas as pd
from bokeh.embed import json_item
from bokeh.io import output_file
from bokeh.models import DatetimeTickFormatter, HoverTool, Span, Label, Band, ColumnDataSource, Range1d, DataRange1d, \
    CustomJSHover, Legend
from bokeh.palettes import Colorblind8
from bokeh.plotting import figure, show

output_file("../output/covid-canarias.html", title='COVID Canarias')

# read the canarias COVID summary data
arcgis_df = pd.read_csv("../data/canarias_arcgis.csv", parse_dates=['date'])
arcgis_df = arcgis_df[arcgis_df['region'] == 'Canaries']
arcgis_df = arcgis_df[(arcgis_df['date'] >= '2020-02-01')]

# get deltas in number of deaths
arcgis_df = arcgis_df.merge(
    arcgis_df['deaths'].diff(),
    left_index=True, right_index=True, suffixes=['', '_covid']
).fillna(0)

# resample and set index
arcgis_df = arcgis_df.resample('D', on='date').sum()

# read the MoMo deaths data
momo_df = pd.read_csv("https://momo.isciii.es/public/momo/data", parse_dates=['fecha_defuncion'])
momo_df = momo_df[(momo_df['cod_sexo'] == 'all') &
                  (momo_df['cod_gedad'] == 'all') &
                  (momo_df['cod_ambito'] == 'CN') &
                  (momo_df['fecha_defuncion'] > '2019-12-01')]

# resample and set index
momo_df = momo_df.resample('D', on='fecha_defuncion').sum()

# merge the data sets
merged_df = pd.merge(arcgis_df, momo_df, left_index=True, right_index=True, how='outer')
merged_df['expected_plus_covid'] = merged_df['defunciones_esperadas'] + merged_df['deaths_covid']
merged_df["datestring"] = merged_df.index.strftime("%b %d")

# set up the figure
p = figure(plot_width=1000, plot_height=400, tools='pan,wheel_zoom,reset',
           x_axis_type="datetime", toolbar_location=None, name='COVID - Canary Islands',
           x_range=DataRange1d(bounds="auto"),
           y_range=Range1d(0, (max(merged_df['defunciones_esperadas_q99']) + 25), bounds="auto"))
p.sizing_mode = 'scale_width'

# Set up hover tooltips
covid_hover_formatter = CustomJSHover(code="""
    if (isNaN(value)) {
        return "-"
    }
    return value.toString();
""")

p.add_tools(HoverTool(
    tooltips=[("Date", '@datestring'),
              ("Expected Deaths", "@defunciones_esperadas"),
              ("Observed Deaths", "@defunciones_observadas"),
              ('COVID-19 Deaths', '@deaths_covid{custom}')],
    formatters={'@deaths_covid': covid_hover_formatter}
))

# format x axis
p.xaxis.formatter = DatetimeTickFormatter(
    hours=["%B %-d"],
    days=["%B %-d"],
    months=["%B %-d"],
    years=["%B %-d"],
)

palette = Colorblind8

# add lines
observed_line = p.line(x='index', y='defunciones_observadas', source=merged_df, name='Observed Deaths',
                       legend_label='Observed', color=palette[0], line_width=1)

expected_line = p.line(x='index', y='defunciones_esperadas', source=merged_df, name='Expected Deaths', color=palette[1],
                       legend_label='Expected', line_width=1)

covid_line = p.line(x='index', y='expected_plus_covid', source=merged_df, name='COVID-19 Deaths', color='red',
                    legend_label='COVID-19', line_width=1)

# create and add bands
confidence_interval = Band(base='index', lower='defunciones_esperadas_q99', upper='defunciones_esperadas_q01',
                           source=ColumnDataSource(merged_df), level='underlay', fill_alpha=1.0, line_width=1,
                           line_color='black')
p.add_layout(confidence_interval)

# create lockdown span
lockdown_date = time.mktime(dt(2020, 3, 14, 0, 0, 0).timetuple()) * 1000
lockdown_start = Span(location=lockdown_date, dimension='height', line_color=palette[3], line_dash='dashed',
                      line_width=2)
lockdown_label = Label(x=lockdown_date, y=10, y_units='screen', text=' Lockdown', text_font='helvetica',
                       text_font_size='9pt')

# create lockdown span
phase0_date = time.mktime(dt(2020, 5, 2, 0, 0, 0).timetuple()) * 1000
phase0_start = Span(location=lockdown_date, dimension='height', line_color=palette[6], line_dash='dashed',
                      line_width=2)
phase0_label = Label(x=lockdown_date, y=10, y_units='screen', text=' Phase 0', text_font='helvetica',
                       text_font_size='9pt')


# create china span
china_date = time.mktime(dt(2020, 1, 11, 0, 0, 0).timetuple()) * 1000
china_start = Span(location=china_date, dimension='height', line_color=palette[4], line_dash='dashed', line_width=2)
china_label = Label(x=china_date, y=10, y_units='screen', text=' China', text_font='helvetica', text_font_size='9pt')

# create canaries span
spain_date = time.mktime(dt(2020, 2, 1, 0, 0, 0).timetuple()) * 1000
spain_start = Span(location=spain_date, dimension='height', line_color=palette[5], line_dash='dashed', line_width=2)
spain_label = Label(x=spain_date, y=10, y_units='screen', text=' Spain', text_font='helvetica', text_font_size='9pt')

# add spans and legend
p.add_layout(phase0_start)
p.add_layout(phase0_label)
p.add_layout(lockdown_start)
p.add_layout(lockdown_label)
p.add_layout(china_start)
p.add_layout(china_label)
p.add_layout(spain_start)
p.add_layout(spain_label)

p.legend.location = "top_left"
p.legend.click_policy = "hide"
p.legend.label_text_font_size = "8pt"
p.legend.spacing = 0
p.legend.border_line_color = None

p.border_fill_color = "whitesmoke"
p.min_border_top = 15

# create the json data for the plot
item_text = json.dumps(json_item(p, "COVID Canarias"))

with open('../docs/page.template', 'r') as file:
    filedata = file.read()

# Replace the target string
filedata = filedata.replace('{PLACEHOLDER}', item_text)

now = datetime.now()
filedata = filedata.replace('{DATE}', now.strftime("%d/%m/%Y %H:%M:%S"))

# Write the file out again
with open('../docs/README.md', 'w') as file:
    print("canaries_deaths_over_time.py: Writing new README.md.")
    file.write(filedata)
