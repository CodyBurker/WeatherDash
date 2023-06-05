import streamlit as st
import pandas as pd
import numpy as np
import geopandas as gpd
import altair as alt
import plotly.express as px

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
    return all_data


def filter_state(input_data, state):
    filtered = input_data.\
        query(f'STATE == "{state}" and value > -50').\
        sort_values('date').\
        groupby(['year', 'month']).\
        agg({'value':'mean'}).\
        reset_index()
    return(filtered)


def filter_year(input_data, beg_year, end_year):
    filtered = input_data[input_data['year'].astype(int) >= beg_year]
    filtered = filtered[filtered['year'].astype(int) <= end_year]
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
state_filtered = filter_year(state_filtered, date_range[0], date_range[1])
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

# Create a base chart object
base = alt.Chart(state_filtered).mark_line(opacity=0.3).encode(
    x='month:O',
    y=alt.Y('value:Q', title='Temperature (F)'),
    tooltip=['month:O', alt.Tooltip('value:Q', title='Avg Temp', format='.2f'), 'year:O'],
    # color = 'value:Q'
).properties(
    title=f'{selected_state} Temperature by Year'
)

# Loop over years and create a plot for each year
chart = alt.layer(
    *[base.transform_filter(alt.datum.year == year).mark_line(color='gray', opacity=0.2, interpolate='basis') for year in state_filtered['year'].unique()],
    data=state_filtered
).properties(width=600, height=400).encode(
).interactive()

st.altair_chart(chart,use_container_width=True)

# Create radar chart
theta = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
fig = px.line_polar(
    state_filtered.groupby('month').agg({'value':'mean'}).reset_index(),
    r='value',
    theta=theta,
)
st.plotly_chart(fig, use_container_width=True)
# Dict to turn numbers into month names
# month_map={'1':'Jan','2':'Feb','3':'Mar'}

# state_filtered_radial = state_filtered
# state_filtered_radial['month'] = state_filtered_radial['month'] * 30

# # Try scatter polar plot
# fig = px.scatter_polar(
#     state_filtered_radial,
#     r='value',
#     theta='month')
# st.plotly_chart(fig, use_container_width=True)