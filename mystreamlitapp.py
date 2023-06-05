import streamlit as st
import pandas as pd
import numpy as np
import geopandas as gpd
import altair as alt

SHAPE_FILEPATH = 'CONUS_CLIMATE_DIVISIONS.shp/GIS.OFFICIAL_CLIM_DIVISIONS.shp'
PAR_FILEPATH = 'climdiv-tmpcdv-v1.0.0-20230504.parquet'

@st.cache_data
def read_shp_file(filepath = SHAPE_FILEPATH):
    gdf = gpd.read_file(filepath)
    gdf_converted = gdf
    gdf_converted['division_number'] = gdf_converted['CD_NEW'].apply(lambda x: f'{int(x):02d}0')
    gdf_converted['state_code'] = gdf_converted['STATE_FIPS']
    gdf_converted['state_div'] = gdf_converted['state_code'] + gdf_converted['division_number']
    gdf_converted.set_index('state_div', inplace=True)
    return(gdf_converted)

@st.cache_data
def read_parquet_file(filepath = PAR_FILEPATH):
    div_weather = pd.read_parquet(filepath)
    div_weather['state_div'] = div_weather['state_code'] + div_weather['division_number']
    div_weather.set_index('state_div', inplace=True)
    return(div_weather)

def load_data():
    # Read in the shapefile of climate divisions
    gdf_converted = read_shp_file(SHAPE_FILEPATH)
    div_weather = read_parquet_file(PAR_FILEPATH)

    all_data = gdf_converted.merge(div_weather, on = 'state_div', how='outer')
    return pd.DataFrame(all_data)


def filter_state(input_data, state):
    filtered = input_data.\
        query(f'STATE == "{state}" and value > -50').\
        sort_values('date').\
        groupby(['year', 'month']).\
        agg({'value':'mean'}).\
        reset_index()
    return(filtered)


# indiana = total.query('STATE == "Indiana" and value > -50').sort_values('date').groupby(['year', 'month']).agg({'value':'mean'}).reset_index()

total = load_data()
date_range = st.slider('Years', 
          min_value= min(total['year'].dropna().astype(int)), 
          max_value = max(total['year'].dropna().astype(int)), 
          value=[1950,2023])

all_states = total[['STATE']].drop_duplicates().sort_values('STATE')
selected_state = st.selectbox(
    'Select State',
    all_states,)

state_filtered = filter_state(total, selected_state)
# state_filtered = state_filtered[(state_filtered['year'].astype(int) >= date_range[0]) & (state_filtered['year'].astype(int) <= date_range[1])]
# Color is month
chart = alt.Chart(
    state_filtered
    ).mark_line(
        interpolate='basis'
    ).encode(
    x='year',
    y='value',
    color='month'
)
st.altair_chart(chart,use_container_width=True)