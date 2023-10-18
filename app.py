import requests
import pandas as pd
import streamlit as st
import os.path
from datetime import datetime

sec_mappings = {"NIFTY 50" : "NIFTY", 
                "BANK NIFTY" : "BANKNIFTY",
                "NIFTY NEXT 50" : "NIFTYNEXT50", 
                "Securities > Rs 20": "SecGtr20", 
                "Securities < Rs 20": "SecLwr20", 
                "F&O Securities": "FOSec",
                "All Securities": "allSec"
                }

cols = ['symbol', 'open_price', 'high_price', 'low_price', 'trade_quantity', 'perChange']
ncols = [x.upper() for x in cols]

df_dict = {}
headers={"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36"}
res=requests.get(r"https://www.nseindia.com/api/live-analysis-variations?index=gainers",headers=headers)
gainer_dict = {}
for key in res.json():
    if key != 'legends':
        df = pd.DataFrame(res.json()[key]['data'])
        if df.shape[0] > 0:
            # df.columns
            dff = df[cols]
            dff.columns = ncols
            dff['STATUS'] = 'Gainer'
            gainer_dict[key] = dff
        else:
            gainer_dict[key] = df
looser_dict = {}
res=requests.get(r"https://www.nseindia.com/api/live-analysis-variations?index=loosers",headers=headers)
for key in res.json():
    if key != 'legends':
        df = pd.DataFrame(res.json()[key]['data'])
        if df.shape[0] > 0:
            dff = df[cols]
            dff.columns = ncols
            dff['STATUS'] = 'Looser'
            looser_dict[key] = dff
        else:
            looser_dict[key] = df

df_dict['Gainers'] = gainer_dict
df_dict['Loosers'] = looser_dict

option = st.selectbox(
        "Select Index",
        ("NIFTY 50", "BANK NIFTY", "NIFTY NEXT 50", "Securities > Rs 20", "Securities < Rs 20", "F&O Securities","All Securities")
        )

#print(option)
#print(type(option))
# data_dict = read_data()
l_df = df_dict['Loosers'][sec_mappings[option]]
g_df = df_dict['Gainers'][sec_mappings[option]]

st.write('Top Gainers Today')
if g_df.shape[0] > 0:
    st.write(g_df)
else:
    st.write('No Gainers')
st.write('Top Loosers Today')
if l_df.shape[0] > 0:
    st.write(l_df)
else:
    st.write('No Loosers')

dff = pd.concat([g_df, l_df])
st.bar_chart(dff, x='SYMBOL', y='PERCHANGE', color='STATUS')
