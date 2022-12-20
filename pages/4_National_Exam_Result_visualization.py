import streamlit as st
import numpy as np
import pandas as pd
from decimal import Decimal as dcm

@st.experimental_memo
def getData(filename):
    return pd.read_csv(filename, dtype=str)

@st.experimental_memo
def getDataColumn(col, year):
    df = getData(f'data/national_exam_result_{year}.csv')
    return list(map(float, df[df[col].notnull()][col]))

@st.experimental_memo
def qmean(xxf):
    return round(np.mean(xxf), 10)

@st.experimental_memo
def qstd(xxf):
    return round(np.std(xxf), 10)

st.title('National Exam Result Visualizer')

st.sidebar.header('National Exam Result Visualization')

col1, col2 = st.columns([2, 1], gap='large')
col1.write('##### Histogram of National Exam result')

dblbl = ['math', 'lit', 'lang', 'phys', 'chem', 'bio', 'natsci', 'his', 'geo', 'civ', 'socsci']

option = st.selectbox('Choose a subject', dblbl)
year_chosen = st.selectbox('Choose a year', ['2022', '2018'])

xx = getDataColumn(option, year_chosen)
col2.metric('Sample size', len(xx))
#xx_bincount = st.slider('Chart resolution', 10, 1000, 100)
#xx_bincount = 41
xx_bincount = [(-0.125 + i * 0.25) for i in range(42)]
if option in ['math', 'lang']:
    xx_bincount = [(-0.1 + i * 0.2) for i in range(52)]

xx_hist, xx_bins_bound = np.histogram(xx, bins=xx_bincount)

xx_bins = [round((i[0] + i[1]) / 2, 8) for i in zip(xx_bins_bound[:-1], xx_bins_bound[1:])]

xx_dataset = pd.DataFrame({'Value': xx_bins, 'Count': xx_hist})

st.bar_chart(xx_dataset, x='Value', y='Count')

col3,col4 = st.columns(2, gap='large')
col3.metric('Mean', qmean(xx))
col4.metric('Standard Deviation', qstd(xx))
