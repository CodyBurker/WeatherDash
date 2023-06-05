import streamlit as st
import pandas as pd
import numpy as np
import geopandas as gpd
import pandas as pd
import altair as alt

# @st.cache_data
def load_data():
    # Read in the shapefile of climate divisions
    gdf = gpd.read_file('CONUS_CLIMATE_DIVISIONS.shp/GIS.OFFICIAL_CLIM_DIVISIONS.shp')
    gdf_converted = gdf
    gdf_converted['division_number'] = gdf_converted['CD_NEW'].apply(lambda x: f'{int(x):02d}0')
    gdf_converted['state_code'] = gdf_converted['STATE_FIPS']
    gdf_converted['state_div'] = gdf_converted['state_code'] + gdf_converted['division_number']
    gdf_converted.set_index('state_div', inplace=True)
    print(len(gdf_converted))
    div_weather = pd.read_parquet('climdiv-tmpcdv-v1.0.0-20230504.parquet')
    div_weather['state_div'] = div_weather['state_code'] + div_weather['division_number']
    div_weather.set_index('state_div', inplace=True)
    # Join the weather data to the shapefile
    # gdf_weather = gdf_converted.merge(div_weather, on = 'state_div', how='outer')
    all_data = gdf_converted.merge(div_weather, on = 'state_div', how='outer')
    gdf_weather_23 = gdf_converted.merge(div_weather.query('year == "2023" and month == "01"'), on = 'state_div', how='outer')
    print(f'gdf_weather_23: {len(gdf_weather_23)}')
    return gdf_weather_23, all_data



year, total = load_data()



date_range = st.slider('Years', 
          min_value= min(indiana['year'].astype(int)), 
          max_value = max(indiana['year'].astype(int)), 
          value=[1950,2023])

indiana = total.query('STATE == "Indiana" and value > -50').sort_values('date').groupby(['year', 'month']).agg({'value':'mean'}).reset_index()

print(date_range)

indiana_filtered = indiana[(indiana['year'].astype(int) >= date_range[0]) & (indiana['year'].astype(int) <= date_range[1])]
# Color is month
chart = alt.Chart(
    indiana_filtered
    ).mark_line(
        interpolate='basis'
    ).encode(
    x='year',
    y='value',
    color='month'
)
st.altair_chart(chart,use_container_width=True)