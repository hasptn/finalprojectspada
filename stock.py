# Import Library
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import yfinance as yf 
from ta.volatility import BollingerBands
from ta.trend import MACD
from ta.momentum import RSIIndicator

##################
# Set up sidebar #
##################

# Add in location to select image.

st.title('Stock Prediction App')

st.markdown("""
This app retrieves the stock value of the **BRI** (from Yahoo Finance) and its corresponding **stock closing price** (year-to-date)!
* **Python libraries:** keras, pandas, streamlit, numpy, matplotlib, seaborn, sklearn, yfinance, ta
""")

option = st.sidebar.selectbox('Selected company', ( 'BBRI.JK', '', '', ''))

import datetime

today = datetime.date.today()
before = today - datetime.timedelta(days=1460)
start_date = st.sidebar.date_input('Start date', before)
end_date = st.sidebar.date_input('End date', today)
if start_date < end_date:
    st.sidebar.success('Start date: `%s`\n\nEnd date:`%s`' % (start_date, end_date))
else:
    st.sidebar.error('Error: End date must fall after start date.')

##############
# Stock data #
##############

df = yf.download(option,start= start_date,end= end_date, progress=False)

# Describing Data
st.subheader('Dataset Head and Tail')
st.write(df.head())
st.write(df.tail())

# Visualizations
st.subheader('Closing Price vs Time Chart')
fig = plt.figure(figsize=(12, 6))
plt.plot(df.Close)
st.pyplot(fig)

st.subheader('Closing Price vs Time Chart 100MA')
ma100 = df.Close.rolling(100).mean()
fig = plt.figure(figsize=(12, 6))
plt.plot(ma100)
plt.plot(df.Close)
st.pyplot(fig)

st.subheader('Closing Price vs Time Chart 100MA & 200MA')
ma100 = df.Close.rolling(100).mean()
ma200 = df.Close.rolling(200).mean()
fig = plt.figure(figsize=(12, 6))
plt.plot(ma100, 'r')
plt.plot(ma200, 'g')
plt.plot(df.Close, 'b')
st.pyplot(fig)

indicator_bb = BollingerBands(df['Close'])

bb = df
bb['bb_h'] = indicator_bb.bollinger_hband()
bb['bb_l'] = indicator_bb.bollinger_lband()
bb = bb[['Close','bb_h','bb_l']]

macd = MACD(df['Close']).macd()

rsi = RSIIndicator(df['Close']).rsi()


###################
# Set up main app #
###################

st.subheader('Stock Bollinger Bands')

st.line_chart(bb)

progress_bar = st.progress(0)


st.subheader('Stock Moving Average Convergence Divergence (MACD)')
st.area_chart(macd)

st.subheader('Stock Relative Strength Index (RSI)')
st.line_chart(rsi)


st.subheader('Recent data ')
st.dataframe(df.tail(10))


################
# Download csv #
################

import base64
from io import BytesIO

def to_excel(df):
    output = BytesIO()
    writer = pd.ExcelWriter(output, engine='xlsxwriter')
    df.to_excel(writer, sheet_name='Sheet1')
    writer.save()
    processed_data = output.getvalue()
    return processed_data

def get_table_download_link(df):
    """Generates a link allowing the data in a given panda dataframe to be downloaded
    in:  dataframe
    out: href string
    """
    val = to_excel(df)
    b64 = base64.b64encode(val) 
    return f'<a href="data:application/octet-stream;base64,{b64.decode()}" download="download.xlsx">Download excel file</a>' # decode b'abc' => abc

st.markdown(get_table_download_link(df), unsafe_allow_html=True)
