import time  # to simulate a real time data, time loop

import altair as alt
import numpy as np  # np mean, np random
import pandas as pd  # read csv, df manipulation
import plotly.express as px
# import plotly.express as px  # interactive charts
import streamlit as st  # 🎈 data web app development
import MySQLdb
import matplotlib.pyplot as plt
from plotly.subplots import make_subplots

import plotly.graph_objects as go

# Page Title
st.set_page_config(
    page_title="Real-Time KECS Commercial Dashboard",
    page_icon="✅",
    layout="wide",
)
st.sidebar.markdown('''
---
Created\ by [Team ITApps).
''')



# setting up connection
conn = MySQLdb.connect(host="184.154.139.152",
                       user="kadunael_read",
                       passwd="Password@2017",
                       db="kadunael_commonDb")
cursor = conn.cursor()

# Read database data
read_data = pd.read_sql_query(""" SELECT * FROM areaoffice   """, conn)

# == total billdelivery
bill_data = pd.read_sql_query("""SELECT * FROM billdeliverydev_check """, conn)

# ====Total Visits by Area Office===#
ao_data = pd.read_sql_query("""SELECT areaoffice.area_office AS AreaOffice, count(billdeliverydev_check.postedby) as Visits FROM billdeliverydev_check 
INNER JOIN users ON billdeliverydev_check.postedby = users.id
JOIN areaoffice on areaoffice.aoid = users.AreaOffice
WHERE billdeliverydev_check.trans_date between "2023-01-01" and "2023-01-31" AND users.Role ='nmd' 
GROUP BY AreaOffice 
""", conn)

# ====total delivered by area office===#
ao_data1 = pd.read_sql_query("""SELECT DISTINCT areaoffice.area_office AS AreaOffice, count(billdeliverydev_check.postedby) as BillDelivered FROM billdeliverydev_check 
INNER JOIN users ON billdeliverydev_check.postedby = users.id
JOIN areaoffice on areaoffice.aoid = users.AreaOffice
WHERE billdeliverydev_check.trans_date between "2023-01-01" and "2023-01-31" AND billdeliverydev_check.status = "delivered"
GROUP BY AreaOffice 
order by BillDelivered desc
""", conn)

# ====total undelivered by area office===#
ao_data2 = pd.read_sql_query("""SELECT DISTINCT areaoffice.area_office AS AreaOffice, count(billdeliverydev_check.postedby) as BillDelivered FROM billdeliverydev_check 
INNER JOIN users ON billdeliverydev_check.postedby = users.id
JOIN areaoffice on areaoffice.aoid = users.AreaOffice
WHERE billdeliverydev_check.trans_date between "2023-01-01" and "2023-01-31" AND billdeliverydev_check.status = "undelivered"
GROUP BY AreaOffice 
order by BillDelivered desc
""", conn)

feeder = pd.read_sql_query(""" SELECT users.FullName AS Staff, COUNT(billdelivery.AccountNumber) AS DeliveredBills, feeder.feeder_name AS Feeder, areaoffice.area_office AS AreaOffice from users
INNER JOIN billdelivery ON users.ID = billdelivery.postedby
Join feeder ON feeder.feederid = users.feederid
Join areaoffice ON areaoffice.aoid = users.AreaOffice
WHERE trans_date between "2023-01-01" and "2023-01-31" AND users.Role = 'nmd'
GROUP by Staff
ORDER BY AreaOffice desc""", conn)

st.markdown('### Metrics')
row1_1, row1_2 = st.columns((2))
with row1_1:
    st.title("Real-Time / Live Commercial Dashboard")

with row1_2:
    st.text(time.strftime("%Y-%m-%d %H:%M"))



placeholder = st.empty()
with placeholder.container():
    # create three columns
    kpi1, kpi2, kpi3 = st.columns(3)

    kpi1.metric(
        label="No. of Area Office 🏠 ",
        value=read_data.shape[0],
        delta=read_data.shape[1],
    )
    kpi2.metric(
        label="Total No. of Bills Delivered 🏠 ",
        value=bill_data.shape[0],
        delta=bill_data.shape[1],
    )
    # kpi3.metric(
    #     label="No. of Total Visits by Area Office 🏠 ",
    #     value=ao_data.shape[0],
    #     delta=ao_data.shape[1],
    # )
    # kpi4.metric(
    #     label="No. Total Delivered by Area Office 🏠 ",
    #     value=ao_data1.shape[1],
    #     delta=ao_data1.shape[1],
    # )
    kpi3.metric(
        label="No. Total Visits by Feeder 🏠 ",
        value=feeder.shape[0],
        delta=feeder.shape[1],
    )

# Side_bar

option = st.sidebar.selectbox("Summary Report", ( 'Donut Chart','Area Office Summary'))

prices_games = ao_data[['Visits']].value_counts().to_frame().reset_index().rename(columns={0: 'counts'})
# prices_games['Visits'] = prices_games['Visits'].apply(lambda x : str(x) + ' ' + "video games")
labels = list(prices_games['Visits'])

if option == 'Donut Chart':
    st.markdown("""
    In this notebook, we will do some analysis by looking at the data of Top Play Store Games.
    * What is the percentage of free video games?
    * Which video game category has the most overall ratings?
    * What category of video games are the most installed?
    * What are the best video games according to google play?
    """)


if option == 'Area Office Summary':
    # Plot Area office by total no of visits
    category_tr = ao_data.groupby(by='AreaOffice')['Visits'].sum().to_frame().sort_values('Visits').reset_index()

    fig1 = px.bar(category_tr, x='Visits', y='AreaOffice',
                  color='AreaOffice',width=950,height=500,)
    fig1.update_layout(showlegend=False,
                       title="Total Visits by Area Office",
                       title_x=0.5,
                       xaxis_title='Visits',
                       yaxis_title='Area Offices')
    st.plotly_chart(fig1)
    #  delivered bills ==== pie plot
    category_tr = ao_data1.groupby(by='AreaOffice')['BillDelivered'].sum().to_frame().sort_values(
        'BillDelivered').reset_index()

    fig = px.pie(category_tr, values='BillDelivered', names='AreaOffice',
                 title='Total Bill Delivered By Area Office',width=1050,height=500,

                 hover_data=['BillDelivered'], labels={'AreaOffice': 'Total Bill Delivered By Area Office'})
    fig.update_traces(textposition='inside', textinfo='percent+label')

    st.plotly_chart(fig)

    # --undelivered bills

    category_tr = ao_data2.groupby(by='AreaOffice')['BillDelivered'].sum().to_frame().sort_values(
        'BillDelivered').reset_index()
    fig3 = px.bar(category_tr, x='BillDelivered', y='AreaOffice',
                  color='BillDelivered',width=950,height=500,)
    fig3.update_layout(showlegend=False,
                       title="Total Undelivered Bills By Area Office",
                       title_x=0.5,
                       xaxis_title='UndeliveredBills',
                       yaxis_title='Area Offices')
    st.plotly_chart(fig3)




clist = feeder['AreaOffice'].unique()
feeder_selection = st.selectbox("Select  Area Office", clist)
col1, col2 = st.columns(2)
fig = px.bar(feeder[feeder['AreaOffice'] == feeder_selection],
              y='Feeder', x='DeliveredBills', title="Delivered Bills By Feeders", color='Staff',width=1000,height=500,)

col1.plotly_chart(fig, use_container_width=True)

