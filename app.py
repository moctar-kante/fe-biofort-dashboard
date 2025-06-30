import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Load your CSV
df = pd.read_csv('merged_data.csv')

st.title('Fe Biofortification Dashboard')

# 1. Select metric
metric_option = st.selectbox('Select metric', ['Relative reduction (%)', 'DALYs saved'])

# 2. Select one or more regions
selected_regions = st.multiselect(
    'Select regions to compare',
    sorted(df['region'].dropna().unique()),
    default=['South Asia', 'LAC']
)

# 3. Filter data
compare_df = df[df['region'].isin(selected_regions)]

# 4. Choose which variable to plot
y_col = 'r_iron_r_2030' if metric_option == 'Relative reduction (%)' else 'd_iron_r_2030'
y_label = metric_option

fig_grouped = px.bar(
    compare_df,
    x='Country',
    y=y_col,
    color='assumptions',
    facet_col='region',
    facet_col_wrap=2,
    title=f'{metric_option} per country and scenario (grouped)',
    labels={y_col: y_label},
    height=600
)
fig_grouped.update_layout(
    barmode='group',
    xaxis_tickangle=-45
)
st.plotly_chart(fig_grouped)

scenario_dot = st.selectbox('Select scenario for comparison', df['assumptions'].unique())

dot_df = df[(df['region'].isin(selected_regions)) & (df['assumptions'] == scenario_dot)]

fig_dot = px.scatter(
    dot_df,
    x='Country',
    y=y_col,
    color='region',
    size=y_col,
    hover_name='Country',
    title=f'{y_label} by country under: {scenario_dot}'
)
fig_dot.update_layout(xaxis_tickangle=-45)
st.plotly_chart(fig_dot)

heat_df = df[df['region'].isin(selected_regions)]

fig_heat = px.density_heatmap(
    heat_df,
    x='assumptions',
    y='Country',
    z=y_col,
    color_continuous_scale='YlOrRd',
    facet_col='region',
    facet_col_wrap=2,
    title=f'{y_label} heatmap per country and scenario',
    height=700
)
st.plotly_chart(fig_heat)


# Sidebar filters
region = st.selectbox('Select region', sorted(df['region'].dropna().unique()))
scenario = st.selectbox('Select scenario', sorted(df['assumptions'].unique()))

# Filter by region and scenario
filtered = df[(df['region'] == region) & (df['assumptions'] == scenario)]

# Plot 1: Relative reduction
st.subheader('Relative reduction (%)')
fig1 = px.bar(filtered, x='Country', y='r_iron_r_2030', color='Country')
st.plotly_chart(fig1)

# Plot 2: DALYs saved
st.subheader('DALYs saved')
fig2 = px.bar(filtered, x='Country', y='d_iron_r_2030', color='Country')
st.plotly_chart(fig2)

# --------- ADDITIONAL PLOTS ---------

st.markdown("---")
st.header('Boxplot and correlation analysis')

# Select region and countries for boxplot
box_region = st.selectbox('Boxplot: Choose region', sorted(df['region'].dropna().unique()), key='box_region')
box_df = df[df['region'] == box_region]

box_countries = st.multiselect('Choose countries', sorted(box_df['Country'].unique()), default=sorted(box_df['Country'].unique()))
box_filtered = box_df[box_df['Country'].isin(box_countries)]

# Boxplot of relative reduction
st.subheader('Boxplot: Relative reduction per scenario')
fig3 = px.box(box_filtered, x='assumptions', y='r_iron_r_2030', color='Country')
fig3.update_layout(xaxis_title='Scenario', yaxis_title='Relative reduction (%)')
st.plotly_chart(fig3)

# Scatter plot: DALY vs relative reduction
st.subheader('Correlation: DALYs vs relative reduction')

scatter_df = df[df['assumptions'] == scenario]

fig4 = px.scatter(scatter_df, x='r_iron_r_2030', y='d_iron_r_2030', color='region', hover_name='Country')
fig4.update_layout(
    xaxis_title='Relative reduction (%)',
    yaxis_title='DALYs saved',
    title=f'{scenario}: DALYs vs Relative Reduction'
)
st.plotly_chart(fig4)
