import streamlit as st
import numpy as np
import pandas as pd

@st.experimental_memo
def getData(data_size):
    return np.random.normal(size=data_size)

@st.experimental_memo
def qmean(xxf):
    return round(np.mean(xxf), 10)

@st.experimental_memo
def qstd(xxf):
    return round(np.std(xxf), 10)

st.sidebar.header('NumPy Demo')

st.title('Normal Distribution Visualizer')

data_length = 10000000

col1, col2 = st.columns([2, 1], gap='large')
col1.write('##### Histogram of numbers from NumPy normal random number generator')
col2.metric('Sample size', data_length)

xx = getData(data_length)
xx_bincount = st.slider('Chart resolution', 10, 1000, 100)
xx_hist, xx_bins_bound = np.histogram(xx, bins=xx_bincount)

xx_bins = [round((i[0] + i[1]) / 2, 8) for i in zip(xx_bins_bound[:-1], xx_bins_bound[1:])]

xx_dataset = pd.DataFrame({'Value': xx_bins, 'Count': xx_hist})

st.bar_chart(xx_dataset, x='Value', y='Count')

col3,col4 = st.columns(2, gap='large')
col3.metric('Mean', qmean(xx))
col4.metric('Standard Deviation', qstd(xx))
