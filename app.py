import requests
import pandas as pd
import streamlit as st
#import os.path
import time
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
st_code = 401
while st_code != 200:
    time.sleep(2)
    res=requests.get(r"https://www.nseindia.com/api/live-analysis-variations?index=gainers",headers=headers)
    st_code = res.status_code
if res.status_code == 200:
    gainer_dict = {}
    for val in sec_mappings.values():
        df = pd.DataFrame(res.json()[val]['data'])
        if df.shape[0] > 0:
            # df.columns
            dff = df[cols]
            dff.columns = ncols
            dff['STATUS'] = 'Gainer'
            gainer_dict[val] = dff
        else:
            gainer_dict[val] = df
    df_dict['Gainers'] = gainer_dict
looser_dict = {}
st_code = 401
while st_code != 200:
    time.sleep(2)
    res=requests.get(r"https://www.nseindia.com/api/live-analysis-variations?index=loosers",headers=headers)
    st_code = res.status_code
if res.status_code == 200:
    for val in sec_mappings.values():
        df = pd.DataFrame(res.json()[val]['data'])
        if df.shape[0] > 0:
            dff = df[cols]
            dff.columns = ncols
            dff['STATUS'] = 'Looser'
            looser_dict[val] = dff
        else:
            looser_dict[val] = df
    df_dict['Loosers'] = looser_dict


if len(df_dict) > 0:
    option = st.selectbox(
        "Select Index",
        ("NIFTY 50", "BANK NIFTY", "NIFTY NEXT 50", "Securities > Rs 20", "Securities < Rs 20", "F&O Securities","All Securities")
        )
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
else:
    st.write('Error loading data from NSE')
