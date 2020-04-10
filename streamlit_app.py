import numpy as np
import pandas as pd
import streamlit as st
import altair as alt
import plotly.graph_objects as go

st.title('東京23区滞在人口推計値の日別遷移')
st.write('【出典：ヤフー・データソリューション】')

data_all = pd.read_csv('data/tokyo_0409.csv')
erea_list = data_all['エリア'].unique()

data_all.set_index(['エリア', '対象分類'], inplace=True)

# 値を縦持ちに変更
data_all = data_all.T
# 日付をdatetime型に変換
data_all.index = map(lambda x: '2020年'+x, data_all.index)
data_all.index = pd.to_datetime(data_all.index, format='%Y年%m月%d日')
data_all.index.name = '月日'

# 表示エリアをセレクトボックスで選択
selected_erea = st.sidebar.selectbox(
    '表示するエリアを選択：',
    erea_list
)

# グラフ表示
st.write(f'## 表示中：{selected_erea}')
data_plotly = data_all[(selected_erea)]
data_plot = [
    go.Scatter(x=data_plotly.index,
               y=data_plotly['住人'],
               mode='lines',
               name='住人'),
    go.Scatter(x=data_plotly.index,
               y=data_plotly['来訪者'],
               mode='lines',
               name='来訪者'),
    go.Scatter(x=data_plotly.index,
               y=data_plotly['全体'],
               mode='lines',
               name='全体')]
layout = go.Layout(
    xaxis={"title": "日付"},
    yaxis={"title": "人数"}
)
st.plotly_chart(go.Figure(data=data_plot, layout=layout))
