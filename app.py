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

def read_data(index):
    gainers_df = pd.DataFrame()
    loosers_df = pd.DataFrame()
    gainers_file = "./data/" + index + "-gainers-" + str(datetime.today().date()) + ".csv"
    loosers_file = "./data/" + index + "-loosers-" + str(datetime.today().date()) + ".csv"
    if os.path.isfile(gainers_file) and os.path.isfile(loosers_file): 
        try:
            gainers_df = pd.read_csv(gainers_file)
        except:
            pass
        try:
            loosers_df = pd.read_csv(loosers_file)
        except:
            pass
    else:
        headers={"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36"}
        res=requests.get(r"https://www.nseindia.com/api/live-analysis-variations?index=gainers",headers=headers)
        #print(res.text)
        for key in res.json():
            if key != 'legends':
                df = pd.DataFrame(res.json()[key]['data'])
                df.to_csv('./data/' + key + "-gainers-" + str(datetime.today().date()) + ".csv", index=None)
        res=requests.get(r"https://www.nseindia.com/api/live-analysis-variations?index=loosers",headers=headers)
        for key in res.json():
            if key != 'legends':
                df = pd.DataFrame(res.json()[key]['data'])
                df.to_csv('./data/' + key + "-loosers-" + str(datetime.today().date()) + ".csv", index=None)
        try:
            gainers_df = pd.read_csv(gainers_file)
        except:
            pass
        try:
            loosers_df = pd.read_csv(loosers_file)
        except:
            pass
    return gainers_df, loosers_df

option = st.selectbox(
        "Select Index",
        ("NIFTY 50", "BANK NIFTY", "NIFTY NEXT 50", "Securities > Rs 20", "Securities < Rs 20", "F&O Securities","All Securities")
        )

#print(option)
#print(type(option))

gainers, loosers = read_data(sec_mappings[option])
st.write('Top Gainers today')
if gainers.shape[0] > 0:
    st.write(gainers)
else:
    st.write('No gainers')
st.write('Top Loosers today')
if loosers.shape[0] > 0:
    st.write(loosers)
else:
    st.write('No Loosers')
