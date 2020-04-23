# Scripts

## `update-canarias-cases.py`

This adds a new row to `../data/canarias_arcgis.csv` with case (and death) data from the day
that it is run.

Data is scraped from 
[here](https://grafcan1.maps.arcgis.com/apps/opsdashboard/index.html#/156eddd4d6fa4ff1987468d1fd70efb6).

## `canaries-deaths-over-time.py`

This creates an html file (`../output/canaries-deaths-over-time.html) which is an interactive graph
of expected and confirmed *deaths* on the canary islands for some months.

It highlights the following:
 - The first reported death in China
 - The first reported death in the Canary Islands (first in Spain)
 - The date of the full lockdown in spain
 
Note the spike in deaths of the elderly immediately following the first chinese death, but
before any testing had been done here. Also note the sharp decline in deaths as the island
population begins to self-impose social distancing as the news of local infections breaks.

## `canaries-infections-over-time.py`

This creates an html file (`../output/cases-over-time.html`) which is an interactive graph of the confirmed covid 
cases on the island since the first identified case. It uses the data from `../data`.

## `island-populations.py`

This is a simple bar chart of the populations of the canary islands. Initially created as a test. It could be
improved: for example, it could use the same colour palette as `canaries-infections-over-time.py`

## `new-cases-today.py`

This is a simple bar chart of the new cases on the canary islands. The date is hardcoded in the script. It could be
improved: for example, it could use the same colour palette as `canaries-infections-over-time.py`