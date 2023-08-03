import streamlit as st
import pandas as pd
st.set_option('deprecation.showPyplotGlobalUse', False)

st.header('Public Company Dash')
st.subheader('Overall Series Breakdown')
df = pd.read_csv('data/stock.csv')
df['date'] = pd.to_datetime(df['date'])
cols = ['Net Tangible Assets','Invested Capital','Total Assets','Total Liabilities Net Minority Interest']

all_stocks = list(set(df['Security Name']))
all_years = list(set(df['date']))
all_cats = list(set(df['Market Category']))
all_stats = list(set(df['Financial Status']))

all_years.sort()

metrics = st.multiselect('select vals', cols,[cols[0]])
df.groupby('date').mean(numeric_only=True)[metrics].plot(kind = 'line')
st.pyplot()


dates = st.select_slider("Schedule your time range:", all_years ,value=(min(all_years),max(all_years)))
filtered_totals = df[(df['date']>=dates[0]) & (df['date']<=dates[1])]

st.subheader('Breakdown by Category')
col1,col2 = st.columns(2)
with col1:
    filtered_totals.groupby('Market Category').count()['ticker'].plot(kind='bar')
    st.pyplot()

with col2:
    filtered_totals.groupby('Financial Status').count()['ticker'].plot(kind = 'bar')
    st.pyplot()

st.subheader('Breakdown by Company')
selected = st.multiselect('select companies', all_stocks,[all_stocks[0]])
filtered_name_df = df[df['Security Name'].isin(selected)]
names = ', '.join(selected)
st.write(f' Companies selected are {names}')

col1,col2 = st.columns(2)
with col1:
    filtered_name_df.groupby(['date','ticker']).mean(numeric_only = True).unstack()['Total Assets'].plot(kind='bar')
    st.pyplot()
    metric1 = st.selectbox('select first metric',cols)
    filtered_name_df.groupby('Security Name').mean(numeric_only = True)[metric1].plot(kind='bar')
    st.pyplot()

with col2:
    filtered_name_df.groupby(['date','ticker']).mean(numeric_only = True).unstack()['Total Liabilities Net Minority Interest'].plot(kind='bar')
    st.pyplot()
    metric2 = st.selectbox('select second metric',cols)
    filtered_name_df.groupby('Security Name').mean(numeric_only = True)[metric2].plot(kind = 'bar')
    st.pyplot()
