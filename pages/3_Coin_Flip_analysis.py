import streamlit as st
import numpy as np
import pandas as pd
import time

def flipacoin():
    return 1 if np.random.randint(2) == 1 else -1

@st.experimental_memo
def qmean(xxf):
    return round(np.mean(xxf), 10)

@st.experimental_memo
def qstd(xxf):
    return round(np.std(xxf), 10)

st.title('Coin Flip Visualizer')

st.sidebar.header('Coin Flip Analysis')

col1,col2 = st.columns([2, 1])
col1.write('##### Head is +1, tail is -1. Each turn, a coin is flipped for a number of times and the total value is recorded')
play_pause = col2.checkbox('Simulation currently running')

max_coin_flip = 30
coin_columns = 5

coin_flip = st.slider('Coin flips', 1, max_coin_flip, 5)

def reset():
    st.session_state.cfa = {'c': [''] * max_coin_flip, 'h1': np.array([]), 'h2': np.array([]), 'cs': coin_flip, 'cc': 0, 'ram': 0}
    for i in range(coin_flip):
        st.session_state.cfa['c'][i] = 'Rolling'

if 'cfa' not in st.session_state:
    reset()

if coin_flip != st.session_state.cfa['cs']:
    reset()

metric_zone = st.empty()
coin_zone = st.empty()

cols = coin_zone.columns(coin_columns)
i_c = 0
for i in range(max_coin_flip):
    cols[i_c].write(st.session_state.cfa['c'][i])
    i_c += 1
    if i_c == coin_columns:
        i_c = 0

chart_zone = st.empty()

simulation_speed = st.slider('Time between simulation intervals (smaller is faster)', 0.00, 2.00, 0.50, 0.01)

#st.session_state

#updater = st.empty()


col_m = metric_zone.columns(4)
col_m[0].metric('Flip amount', coin_flip)
col_m[1].metric('Current value', st.session_state.cfa['ram'])
col_m[2].metric('Coin flipped (turns)', st.session_state.cfa['h1'].size)
col_m[3].metric('Coin flipped (flips)', st.session_state.cfa['h2'].size)
chart_cols = chart_zone.columns(2)
chart_cols[0].header('Histogram of history')
chart_cols[1].header('Heads vs Tails')
history_1 = np.unique(st.session_state.cfa['h1'], return_counts=True)
history_1 = pd.DataFrame({'Value': history_1[0], 'Count': history_1[1]})
history_2 = np.unique(st.session_state.cfa['h2'], return_counts=True)
history_2 = dict(zip(history_2[0], history_2[1]))
if -1 not in history_2:
    history_2[-1] = 0
if 1 not in history_2:
    history_2[1] = 0
history_2 = pd.DataFrame({'Value': ['Tails', 'Heads'], 'Count': [history_2[-1], history_2[1]]})
chart_cols[0].bar_chart(history_1, x='Value', y='Count')
chart_cols[1].bar_chart(history_2, x='Value', y='Count')
chart_cols[0].metric('History Mean', qmean(st.session_state.cfa['h1']))
chart_cols[1].metric('History Standard Deviation', qstd(st.session_state.cfa['h1']))


while play_pause:
    ttmmpp = flipacoin()
    if 'cfa' not in st.session_state:
        reset()
    if st.session_state.cfa['cc'] < coin_flip:
        st.session_state.cfa['c'][st.session_state.cfa['cc']] = 'Head: +1' if ttmmpp == 1 else 'Tail: -1'
        st.session_state.cfa['cc'] += 1
        st.session_state.cfa['ram'] += ttmmpp
        st.session_state.cfa['h2'] = np.append(st.session_state.cfa['h2'], ttmmpp)
        cols = coin_zone.columns(coin_columns)
        i_c = 0
        for i in range(max_coin_flip):
            cols[i_c].write(st.session_state.cfa['c'][i])
            i_c += 1
            if i_c == coin_columns:
                i_c = 0
    else:
        st.session_state.cfa['h1'] = np.append(st.session_state.cfa['h1'], st.session_state.cfa['ram'])
        for i in range(coin_flip):
            st.session_state.cfa['c'][i] = 'Rolling'
        st.session_state.cfa['ram'] = 0
        st.session_state.cfa['cc'] = 0
        cols = coin_zone.columns(coin_columns)
        i_c = 0
        for i in range(max_coin_flip):
            cols[i_c].write(st.session_state.cfa['c'][i])
            i_c += 1
            if i_c == coin_columns:
                i_c = 0
    col_m = metric_zone.columns(4)
    col_m[0].metric('Flip amount', coin_flip)
    col_m[1].metric('Current value', st.session_state.cfa['ram'])
    col_m[2].metric('Coin flipped (turns)', st.session_state.cfa['h1'].size)
    col_m[3].metric('Coin flipped (flips)', st.session_state.cfa['h2'].size)
    chart_cols = chart_zone.columns(2)
    chart_cols[0].header('Histogram of history')
    chart_cols[1].header('Heads vs Tails')
    history_1 = np.unique(st.session_state.cfa['h1'], return_counts=True)
    history_1 = pd.DataFrame({'Value': history_1[0], 'Count': history_1[1]})
    history_2 = np.unique(st.session_state.cfa['h2'], return_counts=True)
    history_2 = dict(zip(history_2[0], history_2[1]))
    if -1 not in history_2:
        history_2[-1] = 0
    if 1 not in history_2:
        history_2[1] = 0
    history_2 = pd.DataFrame({'Value': ['Tails', 'Heads'], 'Count': [history_2[-1], history_2[1]]})
    chart_cols[0].bar_chart(history_1, x='Value', y='Count')
    chart_cols[1].bar_chart(history_2, x='Value', y='Count')
    chart_cols[0].metric('History Mean', qmean(st.session_state.cfa['h1']))
    chart_cols[1].metric('History Standard Deviation', qstd(st.session_state.cfa['h1']))
    time.sleep(simulation_speed + 0.0001)
