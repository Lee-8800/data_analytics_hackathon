import streamlit as st
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt

# Load data
tests = pd.read_csv('data/titan_tests.csv')
boats = pd.read_csv('data/titan_boats.csv')

joined_df = pd.merge(tests, boats, on='Serial number', how='left')

st.set_page_config(layout="wide")

st.title("⛵- Titan Engineering Emissions Dashboard - ⛵")

# Create categories
joined_df['water_depth_cat'] = joined_df['Water depth'].apply(lambda x: "more than 50m" if x > 50 else "50m or less")
joined_df['air_condition'] = joined_df['Air temperature'].apply(lambda x: "warm condition" if x > 14 else ("average condition" if x >= 4 and x <= 14 else "cold condition"))
joined_df['water_condition'] = joined_df['Water temperature'].apply(lambda x: "warm condition" if x > 14 else ("average condition" if x >= 4 and x <= 14 else "cold condition"))


# Create aggregated data

fifty_or_less_air = joined_df[joined_df['water_depth_cat'] == '50m or less'].groupby(["Model", 'air_condition', 'water_depth_cat'])['Emissions'].mean().reset_index()
fifty_or_less_water = joined_df[joined_df['water_depth_cat'] == '50m or less'].groupby(["Model", 'water_condition', 'water_depth_cat'])['Emissions'].mean().reset_index()

more_than_air = joined_df[joined_df['water_depth_cat'] == 'more than 50m'].groupby(["Model", 'air_condition', 'water_depth_cat'])['Emissions'].mean().reset_index()
more_than_water = joined_df[joined_df['water_depth_cat'] == 'more than 50m'].groupby(["Model", 'water_condition', 'water_depth_cat'])['Emissions'].mean().reset_index()

air_data = joined_df.groupby(['air_condition', 'water_depth_cat'])['Emissions'].mean().reset_index()
water_data = joined_df.groupby(['water_condition', 'water_depth_cat'])['Emissions'].mean().reset_index()

# # Create new data with model category
# st.header("Data")
# combined_data = pd.concat([fifty_or_less_air, more_than_air], ignore_index=True).sort_values('Model')
# st.write(combined_data)


# Charts

# Create color variable
model_colors = ['#00D4FF', '#FFD700', '#FF6B6B']  # Cyan, Gold, Coral

col1, col2 = st.columns(2)

# col1 is 50m or less, col2 is more than 50m
with col1:
    with st.container(border=True):
        st.subheader("Emissions at 50m or less")
        fig1 = px.bar(fifty_or_less_air, x='air_condition', y='Emissions', color='Model',
                    title='Average Emissions by Air Condition in 50m or less depth',
                    color_discrete_sequence=model_colors, barmode='group')
        st.plotly_chart(fig1)

        fig1 = px.bar(fifty_or_less_water, x='water_condition', y='Emissions', color='Model',
                    title='Average Emissions by Water Condition in 50m or less depth',
                    color_discrete_sequence=model_colors, barmode='group')
        st.plotly_chart(fig1)
with col2:
    with st.container(border=True):
        st.subheader("Emissions at more than 50m depth")
        fig1 = px.bar(more_than_air, x='air_condition', y='Emissions', color='Model',
                    title='Average Emissions by Air Condition more than 50m depth',
                    color_discrete_sequence=model_colors, barmode='group')
        st.plotly_chart(fig1)

        fig1 = px.bar(more_than_water, x='water_condition', y='Emissions', color='Model',
                    title='Average Emissions by Water Condition more than 50m depth',
                    color_discrete_sequence=model_colors, barmode='group')
        st.plotly_chart(fig1)


st.divider()

# Interactive section
st.header("Interactive Analysis")



# Sidebar filters
st.sidebar.header("Filters")
wind_directions = st.sidebar.multiselect("Wind Direction", joined_df['Wind direction'].unique())
if not wind_directions:
    wind_directions = joined_df['Wind direction'].unique()

use_wind_filter = st.sidebar.checkbox("Filter by Wind Speed")
if use_wind_filter:
    wind_range = st.sidebar.slider("Wind Speed", float(joined_df['Wind speed'].min()), float(joined_df['Wind speed'].max()), 
                                   (float(joined_df['Wind speed'].min()), float(joined_df['Wind speed'].max())))

use_humidity_filter = st.sidebar.checkbox("Filter by Humidity", key="humidity_filter")
if use_humidity_filter:
    humidity_range = st.sidebar.slider("Humidity", float(joined_df['Humidity'].min()), float(joined_df['Humidity'].max()), 
                                       (float(joined_df['Humidity'].min()), float(joined_df['Humidity'].max())))

use_speed_filter = st.sidebar.checkbox("Filter by Average Speed", key="speed_filter")
if use_speed_filter:
    speed_range = st.sidebar.slider("Average Speed", float(joined_df['Average speed'].min()), float(joined_df['Average speed'].max()), 
                                    (float(joined_df['Average speed'].min()), float(joined_df['Average speed'].max())))


# Apply filters
filtered_df = joined_df[joined_df['Wind direction'].isin(wind_directions)]
if use_wind_filter:
    filtered_df = filtered_df[(filtered_df['Wind speed'] >= wind_range[0]) & (filtered_df['Wind speed'] <= wind_range[1])]
if use_humidity_filter:
    filtered_df = filtered_df[(filtered_df['Humidity'] >= humidity_range[0]) & (filtered_df['Humidity'] <= humidity_range[1])]
if use_speed_filter:
    filtered_df = filtered_df[(filtered_df['Average speed'] >= speed_range[0]) & (filtered_df['Average speed'] <= speed_range[1])]

# # Interactive scatter plot
# fig3 = px.scatter(filtered_df, x='Air temperature', y='Water temperature', 
#                   color='Model',
#                   color_discrete_sequence=model_colors, size='Emissions',
#                   hover_data=['Test ID', 'Humidity', 'Average speed', 'Emissions'],
#                   title='Interactive Emissions Analysis')
# fig3.update_traces(marker=dict(size=5))
# fig3.update_layout(showlegend=True)
# st.plotly_chart(fig3, use_container_width=True)


# User-definable scatter plot
st.header("⚓ - Custom Scatter Plot - ⚓")

col1, col2 = st.columns(2)
with col1:
    x_axis = st.selectbox("Select X-axis", ['Air temperature', 'Water temperature', 'Water depth', 'Emissions', 'Average speed', 'Wind speed', 'Humidity', 'Air pressure', 'Distance from shore'])
with col2:
    y_axis = st.selectbox("Select Y-axis", ['Air temperature', 'Water temperature', 'Water depth', 'Emissions', 'Average speed', 'Wind speed', 'Humidity', 'Air pressure', 'Distance from shore'], index=1)

with st.container(border=True):
    # Create scatter plot
    fig_scatter = px.scatter(filtered_df, x=x_axis, y=y_axis, 
                            color='Model', size='Emissions',
                            color_discrete_sequence=model_colors,
                            hover_data=['Test ID', 'Emissions'],
                            title=f'{x_axis} vs {y_axis} by Model')
    fig_scatter.update_traces(marker=dict(size=5))
    st.plotly_chart(fig_scatter, use_container_width=True)

expander = st.expander("Data")
expander.write(filtered_df)
