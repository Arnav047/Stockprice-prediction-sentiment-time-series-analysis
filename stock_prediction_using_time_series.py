# -*- coding: utf-8 -*-
"""Stock prediction using Time series.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1b7LZuzVCWWwEVwn4Iewthzng2DRqq71q
"""

import streamlit as st
from datetime import date
import yfinance as yf
from prophet import Prophet
from prophet.plot import plot_plotly
from plotly import graph_objs as go

START="2020-01-01"
TODAY=date.today().strftime("%Y-%m-%d")

st.title("Stock Prediction App")

stocks=("AAPL","GOOG","MSFT")
selected_stock=st.selectbox("Select dataset for prediction",stocks)

n_years=st.slider("years of prediction:",1,4)

period=n_years*365

def load_data(ticker):
    data=yf.download(ticker,START,TODAY)
    data.reset_index(inplace=True)
    return data

data_load_state=st.text("Load data...")
data=load_data(selected_stock)
data_load_state.text("Loading data...done!")

st.subheader('Raw Data')
st.write(data.tail())



def plot_raw_data():
  fig=go.Figure()
  fig.add_trace(go.Scatter(x=data['Date'],y=data['Open'],name="stock_open"))
  fig.add_trace(go.Scatter(x=data['Date'],y=data['Close'],name="stock_close"))
  fig.layout.update(title_text="Time Series Data with slider",xaxis_rangeslider_visible=True)
  st.plotly_chart(fig)

plot_raw_data()



import pandas as pd

df_train=data[['Date','Close']]
df_train = data[['Date', 'Close']].rename(columns={"Date": "ds", "Close": "y"})

# Flatten multi-level column names
data.columns = ['_'.join(col).strip() if isinstance(col, tuple) else col for col in data.columns]

# Check the updated columns
print("Flattened Columns:", data.columns)

# Create df_train with correct flattened column names
df_train = df_train.rename(columns={"Date": "ds", "Close": "y"})
print(df_train.head())



m=Prophet()
m.fit(df_train)
future=m.make_future_dataframe(periods=period)
forecast=m.predict(future)

st.subheader('Forecast Data')
st.write(forecast.tail())

st.write(f'Forecast plot for {n_years} years')
fig1 = plot_plotly(m, forecast)
st.plotly_chart(fig1)

st.write("Forecast components")
fig2 = m.plot_components(forecast)
st.write(fig2)

