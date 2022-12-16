import streamlit as st
import numpy as np
import pandas as pd

@st.experimental_memo
def getPascalTriangleRow(row_index):
    if row_index == 1:
        return np.array([1])
    elif row_index == 2:
        return np.array([1, 1])
    oo = np.array([0] * row_index, dtype=np.float64)
    oo[0] = 1
    previous_row = getPascalTriangleRow(row_index - 1)
    for i in range(row_index - 2):
        oo[i + 1] = previous_row[i] + previous_row[i + 1]
    oo[row_index - 1] = 1
    return oo

@st.experimental_memo
def qmean(xxf):
    return round(np.mean(xxf))

@st.experimental_memo
def qstd(xxf):
    return round(np.std(xxf))

st.title('Pascal Triangle Visualizer')

st.sidebar.header('Pascal Triangle Demo')

col1, col2 = st.columns([2, 1], gap='large')
col1.write('##### Visualizing a row in Pascal Triangle')

max_row = 300

row_slider = st.slider('Row', 1, max_row, 10)

col2.metric('Row', row_slider)

xx = getPascalTriangleRow(row_slider)
xx = [float(int(i)) for i in xx]

xx_dataset = pd.DataFrame({'Value': xx, 'Item': [i + 1 for i in range(row_slider)]})

st.bar_chart(xx_dataset, x='Item', y='Value')

def numformat(nn):
    nn = int(nn)
    if nn < 1_000_000_000_000:
        return nn
    return '{:e}'.format(nn)

col3,col4 = st.columns(2, gap='large')
col3.metric('Mean', numformat(qmean(xx)))
col4.metric('Standard Deviation', numformat(qstd(xx)))
