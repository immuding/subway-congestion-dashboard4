import streamlit as st
import pandas as pd

# 1. 제목 및 설명
st.title("🚇 서울 지하철 혼잡도 예측 대시보드")
st.markdown("날짜, 시간대, 호선, 역명을 선택하면 예측된 혼잡도와 대안 교통수단 제안을 확인할 수 있습니다.")

# 2. 데이터 불러오기
@st.cache_data
def load_data():
    return pd.read_csv("prediction_results.csv", parse_dates=['date'])

df = load_data()

# 3. 사이드바 입력
st.sidebar.header("🔧 예측 조건 선택")
selected_date = st.sidebar.date_input("날짜 선택", value=df['date'].min().date())
selected_hour = st.sidebar.selectbox("시간대 선택", sorted(df['hour'].unique()))
selected_line = st.sidebar.selectbox("호선 선택", sorted(df['line_name'].unique()))
selected_station = st.sidebar.text_input("역명 입력", "강남")

# 4. 필터링
filtered = df[
    (df['date'] == pd.to_datetime(selected_date)) &
    (df['hour'] == selected_hour) &
    (df['line_name'] == selected_line) &
    (df['station_name'].str.contains(selected_station))
]

# 5. 예측 결과 출력
st.subheader("📈 예측 혼잡도 결과")
if not filtered.empty:
    row = filtered.iloc[0]
    st.metric(label="예측 혼잡도", value=f"{row['predicted_congestion']} ({row['congestion_score']:.2f})")
else:
    st.warning("해당 조건에 맞는 예측 결과가 없습니다.")

# 6. 대안 제안
st.subheader("🚦 대안 제안")
if not filtered.empty and row['predicted_congestion'] == "높음":
    st.markdown("- ⚠️ **탄력 배차 필요**: 배차 간격을 줄이는 방안 검토")
    st.markdown("- 🚌 **주변 버스 노선 활용** 권장")
elif not filtered.empty:
    st.markdown("- ✅ 현재 혼잡도는 양호합니다.")
