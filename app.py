import streamlit as st
import pandas as pd
import plotly.express as px

# Load your CSV
df = pd.read_csv('merged_data.csv')

st.title('Fe Biofortification Dashboard')
st.markdown("""
This dashboard visualizes the potential 2030 impact of Fe biofortification interventions across regions, scenarios, and countries. 
Use the dropdowns and selectors to explore how different assumptions affect projected **relative iron deficiency reduction** and **DALYs saved**.
""")

# -------------------------------
# Metric and region selection
# -------------------------------
metric_option = st.selectbox('Select metric to display:', ['Relative reduction (%)', 'DALYs saved'])

selected_regions = st.multiselect(
    'Select one or more regions to compare:',
    sorted(df['region'].dropna().unique()),
    default=['South Asia', 'LAC']
)

compare_df = df[df['region'].isin(selected_regions)]
y_col = 'r_iron_r_2030' if metric_option == 'Relative reduction (%)' else 'd_iron_r_2030'
y_label = metric_option

# -------------------------------
# Across region view for selected metric
# -------------------------------
st.markdown("###")
st.subheader(f'{metric_option} per country and scenario')
fig_grouped = px.bar(
    compare_df,
    x='Country',
    y=y_col,
    color='assumptions',
    facet_col='region',
    facet_col_wrap=2,
    title=f'{metric_option} per country and scenario',
    labels={y_col: y_label},
    height=600
)
fig_grouped.update_layout(barmode='group', xaxis_tickangle=-45)
fig_grouped.update_layout(yaxis_tickformat=',')
st.plotly_chart(fig_grouped)

# -------------------------------
# Size-proportional view of the selected metric per country under a single scenario
# -------------------------------
scenario_dot = st.selectbox('Select a scenario for dot plot comparison:', df['assumptions'].unique())

dot_df = df[(df['region'].isin(selected_regions)) & (df['assumptions'] == scenario_dot)]
st.markdown("###")
st.subheader(f'{metric_option} by country under selected scenario')
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
fig_dot.update_layout(yaxis_tickformat=',')
st.plotly_chart(fig_dot)

# -------------------------------
# Impact in each country across all scenarios, for the selected metric
# -------------------------------
st.markdown("###")
st.subheader(f'{metric_option} heatmap per country and scenario')
st.markdown("""
Darker colors indicate stronger impact.
""")
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
fig_heat.update_layout(coloraxis_colorbar_tickformat=',')
st.plotly_chart(fig_heat)

# Fe deficiency reduction and DALYs, limited to selected regions only
st.markdown("###")
st.subheader('Correlation: DALYs saved vs Relative reduction')

scatter_df = df[(df['assumptions'] == scenario_dot) & (df['region'].isin(selected_regions))]
fig1 = px.scatter(
    scatter_df,
    x='r_iron_r_2030',
    y='d_iron_r_2030',
    color='region',
    hover_name='Country'
)
fig1.update_layout(
    xaxis_title='Relative reduction (%)',
    yaxis_title='DALYs saved',
    title=f'{scenario_dot}: DALYs vs Relative Reduction in selected regions'
)
fig1.update_layout(yaxis_tickformat=',')
st.plotly_chart(fig1)

# -------------------------------
# Sidebar filters for individual country plots
# -------------------------------
st.markdown("###")
st.subheader('Country-level comparison (select below)')
col1, col2 = st.columns(2)
with col1:
    region = st.selectbox('Select region', sorted(df['region'].dropna().unique()), key='region_select')
with col2:
    scenario = st.selectbox('Select scenario', sorted(df['assumptions'].unique()), key='scenario_select')
filtered = df[(df['region'] == region) & (df['assumptions'] == scenario)]

# Individual bar plots
st.markdown("###")
st.subheader(f'Relative reduction (%) in {region} under {scenario}')
fig2 = px.bar(filtered, x='Country', y='r_iron_r_2030', color='Country')
fig2.update_layout(yaxis_tickformat=',')
st.plotly_chart(fig2)
st.markdown("###")
st.subheader(f'DALYs saved in {region} under {scenario}')
fig3 = px.bar(filtered, x='Country', y='d_iron_r_2030', color='Country')
fig3.update_layout(yaxis_tickformat=',')
st.plotly_chart(fig3)

# -------------------------------
# Additional plots: boxplots and correlation
# -------------------------------
st.markdown("---")
st.header('Boxplots')

# Distribution of relative reduction in Fe deficiency across all modeled scenarios for selected countries
box_region = st.selectbox('Boxplot: Choose region', sorted(df['region'].dropna().unique()), key='box_region')
box_df = df[df['region'] == box_region]

box_countries = st.multiselect('Choose countries for boxplot', sorted(box_df['Country'].unique()), default=sorted(box_df['Country'].unique()))
box_filtered = box_df[box_df['Country'].isin(box_countries)]
st.markdown("###")
st.subheader('Boxplot: Relative reduction across scenarios')

fig4 = px.box(box_filtered, x='assumptions', y='r_iron_r_2030', color='Country')
fig4.update_layout(xaxis_title='Scenario', yaxis_title='Relative reduction (%)')
fig4.update_layout(yaxis_tickformat=',')
st.plotly_chart(fig4)

st.markdown("---")
st.caption("Note: Scenarios represent combinations of adoption rate, yield, and biofortification level assumptions. All figures are projections for the year 2030.")
