import requests
import datetime
import pandas as pd
import csv


request_headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:75.0) Gecko/20100101 Firefox/75.0',
    'Accept': '*/*',
    'Accept-Language': 'en-US,en;q=0.5',
    'Origin': 'https://grafcan1.maps.arcgis.com',
    'Connection': 'keep-alive',
    'Referer': 'https://grafcan1.maps.arcgis.com/apps/opsdashboard/index.html',
    'Cache-Control': 'max-age=0',
    'TE': 'Trailers',
}

deaths_params = (
    ('f', 'json'),
    ('where', '(ESTADO=\'Fallecido\') AND (TIPO_MUN=\'Residencia\')'),
    ('returnGeometry', 'false'),
    ('spatialRel', 'esriSpatialRelIntersects'),
    ('outFields', '*'),
    ('outStatistics', '[{"statisticType":"count","onStatisticField":"OID","outStatisticFieldName":"value"}]'),
    ('resultType', 'standard'),
    ('cacheHint', 'true'),
)

recovered_params = (
    ('f', 'json'),
    ('where', '(ESTADO=\'Cerrado por alta m\xE9dica\') AND (TIPO_MUN=\'Residencia\')'),
    ('returnGeometry', 'false'),
    ('spatialRel', 'esriSpatialRelIntersects'),
    ('outFields', '*'),
    ('outStatistics', '[{"statisticType":"count","onStatisticField":"OID","outStatisticFieldName":"value"}]'),
    ('resultType', 'standard'),
    ('cacheHint', 'true'),
)

total_cases_params = (
    ('f', 'json'),
    ('where', 'TIPO_MUN=\'Residencia\''),
    ('returnGeometry', 'false'),
    ('spatialRel', 'esriSpatialRelIntersects'),
    ('outFields', '*'),
    ('outStatistics', '[{"statisticType":"count","onStatisticField":"OID","outStatisticFieldName":"value"}]'),
    ('resultType', 'standard'),
    ('cacheHint', 'true'),
)

endpoint = 'https://services9.arcgis.com/CgZpnNiCwFObjaOT/arcgis/rest/services/CV19tipo/FeatureServer/4/query'

deaths_response = requests.get(endpoint, headers=request_headers, params=deaths_params)
recoveries_response = requests.get(endpoint, headers=request_headers, params=recovered_params)
total_cases_response = requests.get(endpoint, headers=request_headers, params=total_cases_params)

today = datetime.date.today().strftime('%Y/%-m/%d')

deaths = deaths_response.json()['features'][0]['attributes']['value']
recoveries = recoveries_response.json()['features'][0]['attributes']['value']
total_cases = total_cases_response.json()['features'][0]['attributes']['value']

today_row = [today, 'Canaries', total_cases, '', deaths, recoveries]

# check if we have been run already today, and if not, then add the new row
df = pd.read_csv("../data/canarias_arcgis.csv")
if df.values[-1].tolist()[0] == today_row[0]:
    print("update_canarias_cases.py: Already run today.")
else:
    print("update_canarias_cases.py: First run today.")
    with open('../data/canarias_arcgis.csv', 'a') as datafile:
        writer = csv.writer(datafile, lineterminator='\n')
        print("update_canarias_cases.py: writing row:", today_row)
        writer.writerow(today_row)
