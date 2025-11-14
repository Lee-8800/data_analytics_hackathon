import streamlit as st
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt

# Load data
df = pd.read_csv('data/titan_tests.csv')

st.set_page_config(layout="wide")

st.title("Titan Engineering Emissions Dashboard")

# Create categories
df['water_depth_cat'] = df['Water depth'].apply(lambda x: "more than 50m" if x > 50 else "50m or less")
df['air_condition'] = df['Air temperature'].apply(lambda x: "warm condition" if x > 14 else ("average condition" if x >= 4 and x <= 14 else "cold condition"))
df['water_condition'] = df['Water temperature'].apply(lambda x: "warm condition" if x > 14 else ("average condition" if x >= 4 and x <= 14 else "cold condition"))

# Create aggregated data
air_data = df.groupby(['air_condition', 'water_depth_cat'])['Emissions'].mean().reset_index()
water_data = df.groupby(['water_condition', 'water_depth_cat'])['Emissions'].mean().reset_index()

# Charts
col1, col2 = st.columns(2)

with col1:
    st.subheader("Air Condition vs Water Depth")
    fig1 = px.bar(air_data, x='air_condition', y='Emissions', color='water_depth_cat',
                  title='Average Emissions by Air Condition and Water Depth',
                  color_discrete_sequence=['#1f77b4', '#ff7f0e'], barmode='group')
    st.plotly_chart(fig1)

with col2:
    st.subheader("Water Condition vs Water Depth")
    fig2 = px.bar(water_data, x='water_condition', y='Emissions', color='water_depth_cat',
                  title='Average Emissions by Water Condition and Water Depth',
                  color_discrete_sequence=['#1f77b4', '#ff7f0e'], barmode='group')
    st.plotly_chart(fig2)

# Interactive section
st.header("Interactive Analysis")

# Sidebar filters
st.sidebar.header("Filters")
wind_directions = st.sidebar.multiselect("Wind Direction", df['Wind direction'].unique(), default=df['Wind direction'].unique())
if not wind_directions:
    wind_directions = df['Wind direction'].unique()

use_wind_filter = st.sidebar.checkbox("Filter by Wind Speed")
if use_wind_filter:
    wind_range = st.sidebar.slider("Wind Speed", float(df['Wind speed'].min()), float(df['Wind speed'].max()), 
                                   (float(df['Wind speed'].min()), float(df['Wind speed'].max())))

use_humidity_filter = st.sidebar.checkbox("Filter by Humidity", key="humidity_filter")
if use_humidity_filter:
    humidity_range = st.sidebar.slider("Humidity", float(df['Humidity'].min()), float(df['Humidity'].max()), 
                                       (float(df['Humidity'].min()), float(df['Humidity'].max())))

use_speed_filter = st.sidebar.checkbox("Filter by Average Speed", key="speed_filter")
if use_speed_filter:
    speed_range = st.sidebar.slider("Average Speed", float(df['Average speed'].min()), float(df['Average speed'].max()), 
                                    (float(df['Average speed'].min()), float(df['Average speed'].max())))


# Apply filters
filtered_df = df[df['Wind direction'].isin(wind_directions)]
if use_wind_filter:
    filtered_df = filtered_df[(filtered_df['Wind speed'] >= wind_range[0]) & (filtered_df['Wind speed'] <= wind_range[1])]
if use_humidity_filter:
    filtered_df = filtered_df[(filtered_df['Humidity'] >= humidity_range[0]) & (filtered_df['Humidity'] <= humidity_range[1])]
if use_speed_filter:
    filtered_df = filtered_df[(filtered_df['Average speed'] >= speed_range[0]) & (filtered_df['Average speed'] <= speed_range[1])]

# Interactive scatter plot
fig3 = px.scatter(filtered_df, x='Air temperature', y='Water temperature', 
                  color='Wind direction', size='Emissions',
                  hover_data=['Test ID', 'Humidity', 'Average speed', 'Emissions'],
                  title='Interactive Emissions Analysis')
fig3.update_traces(marker=dict(size=5))
fig3.update_layout(showlegend=False)
st.plotly_chart(fig3, use_container_width=True)
