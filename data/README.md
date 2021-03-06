# Data Sourices

## `canarias_arcgis.csv`

Canary islands cases information (including deaths from COVID-19). Scraped from 
[here](https://grafcan1.maps.arcgis.com/apps/opsdashboard/index.html#/156eddd4d6fa4ff1987468d1fd70efb6)
by `../scripts/update-canarias-cases.py`

## `cases_canarias.csv`

Note: this is old data, and `canarias_arcgis.csv` should be used instead.

Number of cases, fatalities, recoveries per island. taken from daily briefings from Canarian health
authority, found [here](https://www3.gobiernodecanarias.org/noticias/) until (at least) April 7.

Note that after April 7 the government released a comprehensive ArcGIS application for visualizing the epidemic.
This application can be found [here](https://grafcan1.maps.arcgis.com/apps/opsdashboard/index.html#/156eddd4d6fa4ff1987468d1fd70efb6).

## On Data Cleanliness

After a review, the public health department discovered that they had misplaced
some cases. That's why there seem to be spikes/dips on various islands
on that day.

April 6:

See [here](https://www3.gobiernodecanarias.org/noticias/la-consejeria-de-sanidad-constata-1649-casos-acumulados-de-coronavirus-covid-19-2/).

"La Dirección General de Salud Pública del SCS ha modificado y mejorado, 
en cuanto a la profusión de datos, el informe epidemiológico diario de Covid-19,
de modo que la información que se ofrecerá desde hoy es la que atiende a los
casos registrados en función del lugar de declaración y no al de residencia. 
Esto obedece a que hay personas que residen en una isla pero su tarjeta 
sanitaria está registrada en otra, lo que dificulta el procesamiento de los 
datos."
