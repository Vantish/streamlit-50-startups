# streamlit-50-startups

간단한 Streamlit 기반 데모 앱으로, 50개의 스타트업 데이터를 이용해 회사의 수익(Profit)을 예측합니다.

이 레포지토리는 다음을 포함합니다:
- Streamlit 앱: `app_main.py`, `app_home.py`, `app_eda.py`, `app_ml.py`
- 데이터: `data/50_Startups.csv`
- 간단한 라이브러리: `startup_predictor` (데이터 로드, 전처리, 모델 유틸)

## 빠른 시작

Windows (cmd.exe)에서 로컬 실행 예시:

```bat
cd c:\Users\402\Documents\GitHub\streamlit-50-startups
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
streamlit run app_main.py
```

브라우저가 열리고 좌측 사이드바에서 `Home`, `EDA`, `ML` 메뉴를 선택할 수 있습니다.

## 요구사항

필요한 주요 패키지는 `requirements.txt`에 명시되어 있습니다. 기본적으로 다음이 포함됩니다:
- pandas, numpy, scikit-learn, streamlit, altair, joblib 등

권장: 가상환경(venv 또는 conda)을 사용하세요.

## 프로젝트 구조 (주요 파일)

- `app_main.py` : Streamlit 앱 진입점
- `app_home.py` : 홈 화면(데이터 요약, KPI, 사용법)
- `app_eda.py` : 탐색적 데이터 분석(히스토그램, 산점도, 박스플롯)
- `app_ml.py` : 예측 UI (모델 로드/업로드, 입력, 예측 결과 및 유사 샘플)
- `data/50_Startups.csv` : 데이터 원본
- `model/pipe.pkl` : (옵션) 학습된 파이프라인 모델 파일
- `startup_predictor/` : 재사용 가능한 유틸 패키지 (데이터 로드·전처리·모델)

## `startup_predictor` 사용 예시

다음은 파이썬 코드로 패키지를 사용하는 간단한 예시입니다:

```python
from startup_predictor import load_data, train_model, prepare_input, predict

df = load_data()
model = train_model(df)  # model/pipe.pkl로 저장됩니다
inp = prepare_input(100000, 120000, 300000, 'California')
pred = predict(model, inp)
print('예측값:', pred)
```

## 테스트

간단한 pytest가 포함되어 있습니다. 설치 후 다음으로 테스트를 실행할 수 있습니다:

```bat
cd c:\Users\402\Documents\GitHub\streamlit-50-startups
.venv\Scripts\activate
pip install -r requirements.txt
pytest -q
```

## 모델 파일

앱의 ML 페이지는 `model/pipe.pkl` 파일을 예상합니다. 파일이 없는 경우 ML 페이지에서 업로드 기능을 통해 `.pkl` 파일을 업로드할 수 있습니다. 원하시면 `startup_predictor`의 `train_model`을 이용해 자동으로 학습해서 파일을 생성하도록 도와드릴게요.

## 기여 및 라이선스

자유롭게 포크하고 개선사항을 PR로 보내주세요. 본 레포는 교육/데모 목적입니다.

