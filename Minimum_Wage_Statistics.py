import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st
import altair as alt
from vega_datasets import data
from altair.expr import datum

st.title("Minimum Wages Through Ages")
st.markdown('The aim of this project is to visualise the state, federal, and effective minimum wages in the United states from the year 1968 to 2020. For a brief understanding, we use a visualisation of a choropleth map showing the average state minimum wages across the United States since the past 5 decades. We can understand the change in the wages across the years using a bar chart or a scatter plot.')


#Common data
df = pd.read_csv('min_wage_data.csv',usecols=['year','state_id','state_min_wage','fed_min_wage','effective_min_wage','state_min_wage_2020','fed_min_wage_2020','effective_min_wage_2020'],encoding='cp1252')
wages=['state_min_wage','fed_min_wage','effective_min_wage','state_min_wage_2020','fed_min_wage_2020','effective_min_wage_2020']



sel = st.selectbox('Choose a visualization',('--','Bar Chart' ,'Scatter Plot','Choropleth'))

#BAR CHART
if sel=='Bar Chart':
    year_select=st.sidebar.slider('Select Year',1968,2020)
    wage_select=st.sidebar.selectbox("Select the type of wage",wages)
    title= "Wage Statistics of USA in "+ str(year_select)
# bar chart , good so far
    bar = alt.Chart(df).mark_bar().encode(
        x=alt.X('state_id',title='States',type='ordinal'),
        y=alt.Y(wage_select,type='quantitative',scale=alt.Scale(domain=(0, 18),clamp=True)),
        tooltip=['state_id',wage_select,'year']
    ).transform_filter(
        alt.FieldEqualPredicate(field='year', equal=year_select)
    ).properties(
        projection={'type': 'albersUsa'},
        width=800,
        height=500,
        title=title
    )
    st.altair_chart(bar)
  
#SCATTER PLOT
if sel=='Scatter Plot':
    year_select=st.sidebar.slider('Select Year',1968,2020)
    wage_select=st.sidebar.selectbox("Select the type of wage",wages)
    title= "Wage Statistics of USA in "+ str(year_select)
    scatterplot = alt.Chart(df).mark_circle(size=70,opacity=1).encode(
        x=alt.X('state_id',title='States',type='ordinal'),
        y=alt.Y(wage_select,type='quantitative'),
         tooltip=['state_id',wage_select,'year']).transform_filter(
        alt.FieldEqualPredicate(field='year', equal=year_select)
    ).properties(projection={'type': 'albersUsa'},width=800,height=500,title=title)

    st.altair_chart(scatterplot)

#CHOROPLETH
if sel == 'Choropleth':
    title = 'Average State Minimum Wages for the past 5 decades'
    df_map = pd.read_csv('name_code_mapping_US.csv')
    df_join = pd.merge(df, df_map, left_on='state_id', right_on='Full_Name')
    df_choro = df_join.groupby(['State_Code','State_Abv','state_id'])['state_min_wage'].mean().reset_index()


    states = alt.topo_feature(data.us_10m.url, 'states')
    # Creating configs for color,selection,hovering
    multi = alt.selection_multi(empty='all',fields=['state_id'])

    color = alt.condition(multi,
                      alt.Color('state_min_wage:Q',
                      scale=alt.Scale(scheme='blues')),
                      alt.value('lightgray'))
    hover = alt.selection(type='single', on='mouseover', nearest=True,
                          fields=['state_id'])

    #Creating an altair map layer
    choro = alt.Chart(states).mark_geoshape(
        stroke='white'
    ).encode( 
        color=color, 
        tooltip=['state_id:O', 'state_min_wage:Q']
    ).add_selection(
        multi
    ).transform_lookup(
        lookup='id',
        from_=alt.LookupData(df_choro, 'State_Code', ['state_min_wage','state_id'])
    ).properties(
        projection={'type': 'albersUsa'},
        width=800,
        height=500,
        title = title
    )

    c1 = alt.layer(choro)
    st.altair_chart(c1)



