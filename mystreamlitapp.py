import streamlit as st
import pandas as pd
import numpy as np
import geopandas as gpd
import altair as alt
import plotly.express as px
import plotly.graph_objects as go

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
def plot_radial(df):
    r_values = df['value'].tolist()
    r_values.append(r_values[0])  # Append the first value to the end of the list

    theta_values = theta.copy()
    theta_values.append(theta_values[0])  # Append the first value to the end of the list

    fig = go.Scatterpolar(
        r=r_values,
        theta=theta_values,
        mode='lines',
        line_color='gray',
        line_shape='spline',  # Make line into a spline
        opacity=0.3,  # Adjust line opacity
        name = df['year'].iloc[0],
        hoverinfo = 'name+r',
    )   
    return fig

# https://ipyvizzu.vizzuhq.com/latest/examples/presets/53_P_C_polar_scatter/


fig2 = go.Figure()
for year in state_filtered['year'].unique():
    year_data = state_filtered[state_filtered['year'] == year]
    if len(year_data) == 12:
        fig2.add_trace(plot_radial(year_data)) # Change from state_filtered[state_filtered['year'] == year] to year_data
fig2.update_layout(
    # paper_bgcolor='#0e1117',
    # plot_bgcolor='#0e1117',
    plot_bgcolor='rgba(0,0,0,0)',
    showlegend = False,
)
st.plotly_chart(fig2, use_container_width=True, theme = None)