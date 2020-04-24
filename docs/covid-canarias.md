<script src="https://cdn.bokeh.org/bokeh/release/bokeh-2.0.1.min.js"></script>
# COVID-19 Deaths in the Canary Islands

<div id="COVID Canarias"></div>

## The Plot

This plots deaths (all causes) for the Canary Islands over time, with expected deaths for that same time period. The 
data is from the [MoMo](https://momo.isciii.es/public/momo/dashboard/momo_dashboard.html#datos) project, which started 
from a study of the yearly flu in 2012. MoMo computes the expected deaths for a given date based on a long running 
rolling average.

It adds a line to show the novel coronavirus as unexpected deaths^[1]^. This data is from the 
[government of the Canary Islands](https://www3.gobiernodecanarias.org/noticias/).

Three vertical bars have been added to show:

1. The first reported death in China
2. The first reported case in Spain, which occurred here on La Gomera
3. The date that strict lockdown^[2]^ measures were imposed

Data is gathered daily from MoMo and from the Government of the Canary Islands ArcGIS dashboard. The graph is generated 
using Python with Pandas and Bokeh.

The code for generating this graph can be found [here](https://github.com/nathanschepers/covid-canaries). For details 
of how it is put together, please consult the `README.md` files there.

## Footnotes

^[1]^ : 

This is calculated by summing the number of confirmed Covid-19 deaths with the number of expected deaths for each 
day.

^[2]^ : 

Lockdown in the Canary islands consisted of a number of measures, including:
	
- school closures
- closures of all public parks, beaches, or other gathering places
- closure of all common spaces in apartment buildings (rooftops, courtyards)
- cancelling of all public gatherings (concerts, &c.)
- closure of all businesses other than supermarket/pharmacy and supporting business
- closure of all hotels (all tourists were required to leave the islands)
- severe movement restrictions (unable to leave the house without documentation)
- a new street-cleaning initiative, with a focus on the spaces around essential businesses

This lockdown has been enforced by police, who were given powers to operate from Madrid. In addition, the Spanish 
military has been present in a supporting role.

Lockdown measures began to ease on April 13, with some additional businesses (ie. home delivery companies) operating.

As of April 24, no retail establishments are open, and people are only allowed to leave their homes for essential 
purposes. Essential purposes are defined as:

- travel to/from a supermarket or pharmacy
- travel to the doctor or bank
- dog walking, within a limited radius of home

<script>
    item_text = {PLACEHOLDER};
    Bokeh.embed.embed_item(item_text);
</script>