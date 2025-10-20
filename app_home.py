import streamlit as st
import pandas as pd
import os
import altair as alt


def _load_data(path: str) -> pd.DataFrame:
    if not os.path.exists(path):
        return pd.DataFrame()
    return pd.read_csv(path)


def run_home():
    """홈 화면을 새롭게 디자인하여 사용자에게 데이터 요약과 사용법을 안내합니다."""


    st.markdown(
        """
        이 작은 데모 앱은 50개 스타트업 데이터를 기반으로 수익을 예측합니다.
        좌측 메뉴에서 EDA(데이터 탐색)와 ML(모델 예측)을 선택해 보세요.
        """
    )

    data_path = os.path.join('data', '50_Startups.csv')
    df = _load_data(data_path)

    if df.empty:
        st.error('데이터 파일이 없습니다: data/50_Startups.csv')
        return

    # Top summary KPIs
    avg_profit = df['Profit'].mean()
    med_profit = df['Profit'].median()
    total_samples = len(df)

    c1, c2, c3 = st.columns(3)
    c1.metric('샘플 수', f"{total_samples}")
    c2.metric('평균 수익', f"{avg_profit:,.0f} 원")
    c3.metric('중간값 수익', f"{med_profit:,.0f} 원")

    st.markdown('---')

    # Small visuals: state distribution and top features box
    left, right = st.columns([1, 2])
    with left:
        st.subheader('주별 샘플 분포')
        state_counts = df['State'].value_counts().reset_index()
        state_counts.columns = ['State', 'count']
        chart = alt.Chart(state_counts).mark_bar().encode(
            x='State:N',
            y='count:Q',
            color='State:N'
        ).properties(width=250, height=200)
        st.altair_chart(chart, use_container_width=True)

    with right:
        st.subheader('간단 사용법')
        st.write(
            "- EDA: 데이터 분포와 상관관계를 살펴보세요.\n"
            "- ML: 입력값을 조정해 예측 결과를 확인하고, 유사한 기존 사례를 확인하세요.\n"
        )

    st.markdown('---')

    st.subheader('데이터 샘플 (Top 10)')
    st.dataframe(df.head(10))

    st.markdown('데이터 다운로드')
    st.download_button('CSV 다운로드', data=df.to_csv(index=False).encode('utf-8-sig'), file_name='50_Startups_sample.csv')