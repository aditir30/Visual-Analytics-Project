#Visual Analytics
#Project By: Nidhi Srinath, Aditi Raghuwanshi, Sharat Sindoor, Pranusha Apuri

#Importing Libraries
import pandas as pd
import streamlit as st
import altair as alt
from vega_datasets import data
from altair.expr import datum

st.title("Minimum Wages Through Ages")
st.markdown('The aim of this project is to visualize the state, federal, and effective minimum wages in the United States from the year 1968 to 2020. For a brief understanding, we use a bar chart and a scatter plot to analyze the change in the wages across the years, a choropleth map showing the average state minimum wages across the United States since the past 5 decades, and a heatmap visualizing the data and its distributions.')


#Importing Datasets
df = pd.read_csv('min_wage_data.csv',usecols=['year','state_id','state_min_wage','fed_min_wage','effective_min_wage','state_min_wage_2020','fed_min_wage_2020','effective_min_wage_2020'],encoding='cp1252')
df = df.rename(columns={'fed_min_wage':'Federal Minimum Wage','effective_min_wage':'Effective Minimum Wage','state_min_wage':'State Minimum Wage','state_min_wage_2020':'State Minimum Wage in 2020','fed_min_wage_2020':'Federal Minimum Wage in 2020','effective_min_wage_2020':'Effective Minimum Wage in 2020'})
wages=['State Minimum Wage','Federal Minimum Wage','Effective Minimum Wage','State Minimum Wage 2020 Estimate','Federal Minimum Wage 2020 Estimate','Effective Minimum Wage 2020 Estimate']

#Selection box for visualizations
sel = st.selectbox('Choose a visualization',('--','Wage Statistics of the United States','Average State Minimum Wages','Wage Data Exploration'))

#1. Wage Data Statistic using bar chart and scatter plot
if sel=='Wage Statistics of the United States':
    year_select=st.sidebar.slider('Select Year',1968,2020,2000)
    wage_select=st.sidebar.selectbox("Select the type of wage",wages)
    title= "Wage Statistics of USA in "+ str(year_select)

    bar = alt.Chart(df).mark_bar().encode(
        x=alt.X('state_id',title='States',sort= '-y',type='ordinal'),
        y=alt.Y(wage_select,type='quantitative', scale=alt.Scale(domain=(0, 18),clamp=True)),
        tooltip=[alt.Tooltip('state_id', title = 'State'),alt.Tooltip(wage_select, title = str(wage_select)+'($/hr)'),alt.Tooltip('year', title = 'Year')]
    ).transform_filter(
        alt.FieldEqualPredicate(field='year', equal=year_select)
    ).properties(
        projection={'type': 'albersUsa'},
        width=800,
        height=500,
        title=title
    )
    st.altair_chart(bar)
    
    scatterplot = alt.Chart(df).mark_circle(size=70,opacity=1).encode(
        x=alt.X('state_id',title='States',type='ordinal'),
        y=alt.Y(wage_select,type='quantitative'),
         tooltip=[alt.Tooltip('state_id', title = 'State'),alt.Tooltip(wage_select,title = str(wage_select)+'($/hr)'),alt.Tooltip('year', title = 'Year')]
    ).transform_filter(
        alt.FieldEqualPredicate(field='year', equal=year_select)
    ).properties(projection={'type': 'albersUsa'},
                 width=800,
                 height=500)

    
    st.altair_chart(scatterplot)
    

#2. Average State Wage Choropleth Representation
if sel == 'Average State Minimum Wages':
    title = 'Average State Minimum Wages for the past 5 decades'
    df_map = pd.read_csv('name_code_mapping_US.csv')
    df_join = pd.merge(df, df_map, left_on='state_id', right_on='Full_Name')
    df_choro = df_join.groupby(['State_Code','State_Abv','state_id'])['State Minimum Wage'].mean().reset_index()


    states = alt.topo_feature(data.us_10m.url, 'states')
    # Creating configs for color,selection,hovering
    multi = alt.selection_multi(empty='all',fields=['state_id'])

    color = alt.condition(multi,
                      alt.Color('State Minimum Wage:Q',
                      scale=alt.Scale(scheme='blues')),
                      alt.value('lightgray'))
    hover = alt.selection(type='single', on='mouseover', nearest=True,
                          fields=['state_id'])

    #Creating an altair map layer
    choro = alt.Chart(states).mark_geoshape(
        stroke='white'
    ).encode( 
        color=color, 
        tooltip=[alt.Tooltip('state_id:O', title='State'),alt.Tooltip('State Minimum Wage:Q', title='Avg. Minimum Wage ($/hr)')]
    ).add_selection(
        multi
    ).transform_lookup(
        lookup='id',
        from_=alt.LookupData(df_choro, 'State_Code', ['State Minimum Wage','state_id'])
    ).properties(
        projection={'type': 'albersUsa'},
        width=800,
        height=500,
        title = title
    )

    c1 = alt.layer(choro)
    st.altair_chart(c1)


#3. Wage Data Exploration with Heat Map
if sel=='Wage Data Exploration':
    title = "Trend in Wages Increment"
    df_map = pd.read_csv('name_code_mapping_US.csv')
    df_join = pd.merge(df, df_map, left_on='state_id', right_on='Full_Name')

    wage_select=st.selectbox("Select the type of wage",list(wages),index=0)

    heatmap = alt.Chart(df_join).mark_rect().encode(
    x = alt.X('year:O', title ='Year'),
    y = alt.Y('state_id:O', title = 'States'),
    color = alt.Color(wage_select+':Q')
    ).properties(
    width=1000,
    height=800,
    title = "Trend in Wage Increment"
    ).interactive()
    
    st.altair_chart(heatmap)


