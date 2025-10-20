import streamlit as st
import pandas as pd
import os
import altair as alt


def _load_data(path: str) -> pd.DataFrame:
    if not os.path.exists(path):
        return pd.DataFrame()
    return pd.read_csv(path)


def run_eda():
    st.subheader('EDA (탐색적 데이터 분석)')
    data_path = os.path.join('data', '50_Startups.csv')
    df = _load_data(data_path)

    if df.empty:
        st.warning('데이터 파일을 찾을 수 없습니다: data/50_Startups.csv')
        return

    st.markdown('데이터 샘플')
    st.dataframe(df.head(10))

    st.markdown('## 변수별 분포')
    numeric_cols = ['R&D Spend', 'Administration', 'Marketing Spend', 'Profit']
    col = st.selectbox('분포를 볼 열 선택', numeric_cols)
    bins = st.slider('히스토그램 빈 개수', 5, 100, 20)

    chart = alt.Chart(df).mark_bar().encode(
        alt.X(f"{col}:Q", bin=alt.Bin(maxbins=bins)),
        y='count()'
    ).properties(width=700, height=300)

    st.altair_chart(chart, use_container_width=True)

    st.markdown('## 산점도 (상호작용형)')
    x_axis = st.selectbox('X축', numeric_cols, index=0)
    y_axis = st.selectbox('Y축', numeric_cols, index=3)
    color_by = st.selectbox('색상 기준 (카테고리)', ['State', 'None'])

    enc = alt.Color('State:N') if color_by == 'State' else alt.value('steelblue')

    scatter = alt.Chart(df).mark_circle(size=60).encode(
        x=f'{x_axis}:Q',
        y=f'{y_axis}:Q',
        color=enc,
        tooltip=['R&D Spend', 'Administration', 'Marketing Spend', 'State', 'Profit']
    ).interactive().properties(width=700, height=400)

    st.altair_chart(scatter, use_container_width=True)

    st.markdown('## 상태별 수익 비교')
    box = alt.Chart(df).mark_boxplot().encode(
        x='State:N',
        y='Profit:Q',
        color='State:N'
    ).properties(width=700, height=300)

    st.altair_chart(box, use_container_width=True)

    st.markdown('---')
    st.write('요약 통계 (주별 평균)')
    # avoid duplicate column names by using numeric_cols which already contains 'Profit'
    st.table(df.groupby('State')[numeric_cols].mean().round(2))