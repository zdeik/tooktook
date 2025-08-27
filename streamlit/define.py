import requests
import pandas as pd
import streamlit as st

# FastAPI 서버의 기본 URL을 상수로 정의
API_BASE_URL = "http://127.0.0.1:8000/api"  # 포트를 8001로 변경했다면 이대로 유지

@st.cache_data
def load_data():
    """FastAPI 서버의 각 엔드포인트에서 데이터를 가져와 DataFrame으로 반환하는 함수"""
    endpoints = {
        'df_consultants': '/consultants',
        'df_consultation_documents': '/consultation_documents',
        'df_consultation_fund_types': '/consultation_fund_types',
        'df_consultations': '/consultations',
        'df_conversation_logs': '/conversation_logs',
        'df_customers': '/customers',
        'df_documents': '/documents',
        'df_fund_types': '/fund_types',
        'static_df': '/statistics',
        'df_predictions': '/predictions',
        'df_tomorrow_predictions': '/tomorrow_predictions'
    }

    dataframes = {}
    
    # 각 엔드포인트를 순회하며 데이터 로드
    for name, endpoint in endpoints.items():
        url = f"{API_BASE_URL}{endpoint}"
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            data = response.json()
            dataframes[name] = pd.DataFrame(data)
        except requests.exceptions.RequestException as e:
            st.error(f"'{name}' 데이터 로드 실패: {e}")
            st.error(f"FastAPI 서버가 {API_BASE_URL}에서 실행 중인지 확인하세요.")
            return None

    return dataframes