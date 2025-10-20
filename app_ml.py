import streamlit as st
import pandas as pd
import numpy as np
import joblib
import os
from sklearn.neighbors import NearestNeighbors


def _load_data(path: str) -> pd.DataFrame:
    if not os.path.exists(path):
        return pd.DataFrame()
    return pd.read_csv(path)


def run_ml():
    st.subheader('수익 예측 (ML)')
    st.info('입력값을 조정하여 예측을 확인하세요. 모델이 없으면 학습된 파이프파일(.pkl)을 업로드할 수 있습니다.')

    data_path = os.path.join('data', '50_Startups.csv')
    df = _load_data(data_path)

    if df.empty:
        st.warning('데이터 파일을 찾을 수 없습니다: data/50_Startups.csv')
        return

    # Determine sensible ranges from data
    rnd_min, rnd_max = int(df['R&D Spend'].min()), int(df['R&D Spend'].max())
    admin_min, admin_max = int(df['Administration'].min()), int(df['Administration'].max())
    mkt_min, mkt_max = int(df['Marketing Spend'].min()), int(df['Marketing Spend'].max())

    with st.form('predict_form'):
        col1, col2 = st.columns(2)
        with col1:
            rnd = st.slider('연구개발비 (R&D Spend)', rnd_min, rnd_max, int(df['R&D Spend'].median()))
            marketing = st.number_input('마케팅비 (Marketing Spend)', min_value=mkt_min, max_value=mkt_max, value=int(df['Marketing Spend'].median()))
        with col2:
            admin = st.number_input('운영비 (Administration)', min_value=admin_min, max_value=admin_max, value=int(df['Administration'].median()))
            state = st.selectbox('주 선택 (State)', df['State'].unique())

        submitted = st.form_submit_button('예측하기')

    model_path = os.path.join('model', 'pipe.pkl')
    if not os.path.exists(model_path):
        st.warning('학습된 모델 파일이 없습니다. model/pipe.pkl 을 준비하거나 업로드하세요.')
        uploaded = st.file_uploader('모델 업로드 (.pkl)', type=['pkl'])
        if uploaded:
            try:
                with open(model_path, 'wb') as f:
                    f.write(uploaded.getbuffer())
                st.success('모델 업로드 성공. 다시 예측을 실행하세요.')
            except Exception as e:
                st.error(f'업로드중 오류: {e}')
        return

    if submitted:
        try:
            model = joblib.load(model_path)
        except Exception as e:
            st.error(f'모델 로드 실패: {e}')
            return

        input_df = pd.DataFrame([{'R&D Spend': rnd, 'Administration': admin, 'Marketing Spend': marketing, 'State': state}])
        try:
            y_pred = model.predict(input_df)
        except Exception as e:
            st.error(f'예측 중 오류 발생: {e}')
            return

        pred_value = float(y_pred[0])
        st.success('예측 완료')
        st.markdown(f"### 예측된 수익: {pred_value:,.0f} 원")

        # Show nearest examples from dataset (by numeric features)
        try:
            features = df[['R&D Spend', 'Administration', 'Marketing Spend']].values
            nbrs = NearestNeighbors(n_neighbors=3).fit(features)
            dist, idx = nbrs.kneighbors([[rnd, admin, marketing]])
            st.markdown('### 입력과 가장 유사한 데이터 샘플')
            nearest = df.iloc[idx[0]][['R&D Spend', 'Administration', 'Marketing Spend', 'State', 'Profit']]
            st.table(nearest.reset_index(drop=True))
        except Exception:
            # fallback: show random samples
            st.info('유사 샘플을 계산할 수 없어 임의 샘플을 표시합니다.')
            st.dataframe(df.sample(3)[['R&D Spend', 'Administration', 'Marketing Spend', 'State', 'Profit']])
    