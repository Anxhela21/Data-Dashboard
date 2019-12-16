import pandas as pd
import numpy as np
import plotly.graph_objs as go
import plotly.colors
from collections import OrderedDict
import requests


# default list of all countries of interest
# default list of all countries of interest
country_default = OrderedDict([("Yemen", "YE"), ("Malawi", "MW"), ("Niger", "NE"),("Mozambique", "MZ"),("Central African Republic", "CF")])

def return_figures(countries=country_default):
    
  """Creates four plotly visualizations using the World Bank API

  # Example of the World Bank API endpoint:
  # arable land for the United States and Brazil from 1990 to 2015
  # http://api.worldbank.org/v2/countries/usa;bra/indicators/AG.LND.ARBL.HA?date=1990:2015&per_page=1000&format=json

    Args:
        country_default (dict): list of countries for filtering the data

    Returns:
        list (dict): list containing the four plotly visualizations

  """

  # when the countries variable is empty, use the country_default dictionary
  if not bool(countries):
    countries = country_default

  # prepare filter data for World Bank API
  # the API uses ISO-3 country codes separated by ;
  country_filter = list(countries.values())
  country_filter = [x.lower() for x in country_filter]
  country_filter = ';'.join(country_filter)

  # World Bank indicators of interest for pulling data
  indicators= [ "TM.VAL.AGRI.ZS.UN", "TX.VAL.AGRI.ZS.UN", "TX.VAL.MRCH.XD.WD", "TM.VAL.MRCH.XD.WD", "SN.ITK.DEFC.ZS"]

    # Agricultural Raw Materials Imports = TM.VAL.AGRI.ZS.UN
    # Agricultural Raw Materials Exports = TX.VAL.AGRI.ZS.UN
    # Export Value Index (2000 =100) = TX.VAL.MRCH.XD.WD 
    # Import Value Index (2000 =100) = TM.VAL.MRCH.XD.WD
    # Malnourished = SN.ITK.DEFC.ZS
                                        

  data_frames = [] # stores the data frames with the indicator data of interest
  urls = [] # url endpoints for the World Bank API

  # pull data from World Bank API and clean the resulting json
  # results stored in data_frames variable
  for indicator in indicators:
    url = 'http://api.worldbank.org/v2/countries/' + country_filter +\
    '/indicators/' + indicator + '?date=1990:2015&per_page=1000&format=json'
    urls.append(url)

    try:
      r = requests.get(url)
      data = r.json()[1]
    except:
      print('could not load data ', indicator)

    for i, value in enumerate(data):
      value['indicator'] = value['indicator']['value']
      value['country'] = value['country']['value']

    data_frames.append(data)
  
  # first chart plots arable land from 1990 to 2015 in top 10 economies 
  # as a line chart
  graph_one = []
  df_one = pd.DataFrame(data_frames[0])

  # filter and sort values for the visualization
  # filtering plots the countries in decreasing order by their values
  #df_one = df_one[(df_one['date'] == '2017') | (df_one['date'] == '1990')]
  #df_one.sort_values('value', ascending=False, inplace=True)

  # this  country list is re-used by all the charts to ensure legends have the same
  # order and color
  countrylist = df_one.country.unique().tolist()
  
  for country in countrylist:
      x_val = df_one[df_one['country'] == country].date.tolist()
      y_val =  df_one[df_one['country'] == country].value.tolist()
      graph_one.append(
          go.Scatter(
          x = x_val,
          y = y_val,
          mode = 'lines',
          name = country
          )
      )

  layout_one = dict(title = 'Agricultural Raw Materials Imports',
                xaxis = dict(title = 'Year',
                  autotick=False, tick0=2000, dtick=1),
                yaxis = dict(title = '% of merchandise imports', autotick=False, tick0=0, dtick=5),    autosize=False,
    width=600,
    height=500,)




# New Graph Two:
  graph_two = []
  df_two = pd.DataFrame(data_frames[3])
  #df_three = df_three[(df_three['date'] == '2015') | (df_three['date'] == '1990')]

  #df_three.sort_values('value', ascending=False, inplace=True)
  for country in countrylist:
      x_val = df_two[df_two['country'] == country].date.tolist()
      y_val =  df_two[df_two['country'] == country].value.tolist()
      graph_two.append(
          go.Bar(
          x = x_val,
          y = y_val,
          name = country
          )
      )

  layout_two = dict(title = 'Import Value Index (2000 = 100)',
               xaxis = dict(title = 'Year',
                  autotick=False, tick0=2000, dtick=1),
                yaxis = dict(title = 'value (thousand)'),    autosize=False,
    width=600,
    height=500,)



  # third chart plots percent of population that is rural from 1990 to 2015
  graph_three = []
  df_three = pd.DataFrame(data_frames[1])
  #df_three = df_three[(df_three['date'] == '2015') | (df_three['date'] == '1990')]

  #df_three.sort_values('value', ascending=False, inplace=True)
  for country in countrylist:
      x_val = df_three[df_three['country'] == country].date.tolist()
      y_val =  df_three[df_three['country'] == country].value.tolist()
      graph_three.append(
          go.Scatter(
          x = x_val,
          y = y_val,
          mode = 'lines',
          name = country
          )
      )

  layout_three = dict(title = 'Agricultural Raw Materials Exports',
               xaxis = dict(title = 'Year',
                  autotick=False, tick0=2000, dtick=1),
                yaxis = dict(title = '& of merchandise exports'),    autosize=False,
    width=600,
    height=500,)



  graph_four = []
  df_four= pd.DataFrame(data_frames[2])

  for country in countrylist:
      x_val = df_four[df_four['country'] == country].date.tolist()
      y_val =  df_four[df_four['country'] == country].value.tolist()
      graph_four.append(
          go.Bar(
          x = x_val,
          y = y_val,
          name = country
          )
      )

  layout_four = dict(title = 'Export Value Index (2000 = 100)',
               xaxis = dict(title = 'Year',
                  autotick=False, tick0=2000, dtick=1),
                yaxis = dict(title = 'value (thousand)'),    autosize=False,
    width=600,
    height=500,)


  graph_five= []
  df_five = pd.DataFrame(data_frames[4])

  for country in countrylist:
      x_val = df_five[df_five['country'] == country].date.tolist()
      y_val =  df_five[df_five['country'] == country].value.tolist()
      graph_five.append(
          go.Bar(
          x = x_val,
          y = y_val,
          name = country
          )
      )

  layout_five = dict(title = 'Prevalence of Undernourishment',
               xaxis = dict(title = 'Year',
                  autotick=False, tick0=2000, dtick=1),
                yaxis = dict(title = '% of population'),    autosize=False,
    width=600,
    height=500,)



  # second chart plots ararble land for 2015 as a bar chart
  graph_six = []
  df_five.sort_values('value', ascending=False, inplace=True)
  df_five= df_five[df_five['date'] == '2015'] 

  graph_six.append(
      go.Bar(
      x = df_five.country.tolist(),
      y = df_five.value.tolist(),
      )
  )

  layout_six = dict(title = 'Prevalence of Malnutrition in 2015',
                xaxis = dict(title = 'Country',),
                yaxis = dict(title = 'Year'),    autosize=False,
    width=600,
    height=500,)
                    
  # append all charts
  figures = []
  figures.append(dict(data=graph_one, layout=layout_one))
  figures.append(dict(data=graph_two, layout=layout_two))
  figures.append(dict(data=graph_three, layout=layout_three))
  figures.append(dict(data=graph_four, layout=layout_four))
  figures.append(dict(data=graph_five, layout=layout_five))
  figures.append(dict(data=graph_six, layout=layout_six))

  return figures
