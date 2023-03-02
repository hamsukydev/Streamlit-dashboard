import time  # to simulate a real time data, time loop

import numpy as np  # np mean, np random
import pandas as pd  # read csv, df manipulation
import plotly.express as px
# import plotly.express as px  # interactive charts
import streamlit as st  # 🎈 data web app development
import MySQLdb
import matplotlib as plt

#
# #
#
#
# # setting up connection
# setting up connection
conn = MySQLdb.connect(host="184.154.139.152",
                       user="kadunael_read",
                       passwd="Password@2017",
                       db="kadunael_commonDb")
cursor = conn.cursor()

# Read database data
read_data = pd.read_sql_query(""" SELECT areaoffice.area_office AS AreaOffice, count(billdeliverydev_check.postedby) as Visits FROM billdeliverydev_check 
INNER JOIN users ON billdeliverydev_check.postedby = users.id
JOIN areaoffice on areaoffice.aoid = users.AreaOffice
WHERE billdeliverydev_check.trans_date between "2023-01-01" and "2023-01-31" AND users.Role ='nmd' 
GROUP BY Visits    """, conn)

if st.checkbox("Display Data"):
    st.write(bill_data.head())

dimensions = st.radio("What Dimension Do You Want to Show?", ("Rows", "Columns"))
if dimensions == "Rows":
    st.text("Showing Length of Rows")
    ao_data1.shape[0]

if dimensions == "Columns":
    st.text("Showing Length of Columns")
    ao_data1.shape[1]

cursor.execute('select trans_date, AccountNumber, name, status from billdeliverydev_check')
rows = cursor.fetchall()
x = str(rows)[0:500]  ###
print(x)

df = pd.DataFrame([[ij for ij in i] for i in rows])
df.rename(columns={0: 'trans_date', 1: 'AccountNumber', 2: 'name', 3: 'status'}, inplace=True);
df = df.sort_values(['AccountNumber'], ascending=[1])

# dfObj = pd.DataFrame(ao_data, columns = ['aoid' , 'area_office', 'region_id'], index=False)
# x= dfObj.style.hide_index()


print(df)
clist = df['name'].unique()
print(clist)

#
# country_names = df['name']
# for i in range(len(country_names)):
#     try:
#         country_names[i] = str(country_names[i]).decode('utf-8')
#     except:
#         country_names[i] = 'Country name decode error'
#
#
# # df_filtered = ao_data[(ao_data.isin(ao_data))]
# # st.write(df_filtered)
# #
# print(dfObj)


# Display both charts together
