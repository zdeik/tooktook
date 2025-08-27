import plotly.express as px
import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import numpy as np
from app import cons_chart1
from app2 import cons_cahrt2
from app3 import cons_cahrt3
from tab import predicti
from ui import ui_css
from define import load_data
from app_category import category_char1

# 페이지 설정
st.set_page_config(
    page_title="상담사 관리 대시보드",
    page_icon="👥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ui디자인
ui_css()

# FastAPI에서 데이터 로드
loaded_data = load_data()

# FastAPI 서버에서 데이터를 가져오지 못했을 경우
if loaded_data is None:
    st.error("FastAPI 서버에서 데이터를 가져올 수 없습니다. 서버가 실행 중인지 확인해주세요.")
    st.stop() # 대시보드 실행 중지
    
# 데이터프레임 추출
df_consultants = loaded_data['df_consultants']
df_consultation_documents = loaded_data['df_consultation_documents']
df_consultation_fund_types = loaded_data['df_consultation_fund_types']
df_consultations = loaded_data['df_consultations']
df_conversation_logs = loaded_data['df_conversation_logs']
df_customers = loaded_data['df_customers']
df_documents = loaded_data['df_documents']
df_fund_types = loaded_data['df_fund_types']
static_df = loaded_data['static_df']
df_predictions = loaded_data['df_predictions']
df_tomorrow_predictions = loaded_data['df_tomorrow_predictions']

# 메트릭 계산
try:
    # 총 상담건수 - metric
    total_cons = static_df['total_consultations'].sum() if 'total_consultations' in static_df.columns else len(df_consultations)

    # 총상담자수 - metric
    total_customer = df_customers['customer_id'].count() if 'customer_id' in df_customers.columns else len(df_customers)

    # 평균상담시간 - metric
    avg_time = static_df['avg_consultation_time'].mean() if 'avg_consultation_time' in static_df.columns else 0

    # 완료율 - metric
    completion_rate = (df_conversation_logs['status'] == '완료').sum() / len(df_conversation_logs) * 100 if len(df_conversation_logs) > 0 else 0

    # 평균 만족도 - metric
    good_rate = static_df['avg_satisfaction_score'].mean() if 'avg_satisfaction_score' in static_df.columns else 0
except Exception as e:
    st.error(f"메트릭 계산 중 오류 발생: {e}")
    total_cons = 0
    total_customer = 0
    avg_time = 0
    completion_rate = 0
    good_rate = 0

# 고객 페이지 데이터 준비
try:
    consultants_df_1 = df_consultants.drop(['consultant_id','major','join_date','team'], axis=1, errors='ignore')
    consultants_df_sorted = consultants_df_1.sort_values('department') if 'department' in consultants_df_1.columns else consultants_df_1

    # 서류 데이터 준비
    df_documents_renamed = df_documents.rename(columns={'document_name': '많이 찾는 서류'})
    document_t_df = df_documents_renamed['많이 찾는 서류'] if '많이 찾는 서류' in df_documents_renamed.columns else df_documents
except Exception as e:
    st.error(f"데이터 준비 중 오류 발생: {e}")
    consultants_df_sorted = pd.DataFrame()
    document_t_df = pd.DataFrame()

# 헤더
st.markdown("""
<div class="main-header">
    <h1 style="color: #2c3e50; margin-bottom: 0.5rem;">📝상담사 관리 대시보드</h1>
    <p style="color: #7f8c8d; font-size: 1.1rem; margin: 0;">실시간 상담사 현황 및 성과 모니터링</p>
</div>
""", unsafe_allow_html=True)

# 메인 대시보드
col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-value">{total_cons}</div>
        <div class="metric-label">총 상담건수 </div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-value">{total_customer}</div>
        <div class="metric-label">총 상담자수</div>
    </div>
    """, unsafe_allow_html=True)
    
with col3:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-value">{avg_time:.1f}</div>
        <div class="metric-label">평균 상담 시간(분)</div>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-value">{completion_rate:.1f}%</div>
        <div class="metric-label">완료율</div>
    </div>
    """, unsafe_allow_html=True)

with col5:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-value">{good_rate:.1f}</div>
        <div class="metric-label">평균 만족도</div>
    </div>
    """, unsafe_allow_html=True)
    
st.markdown("<br>", unsafe_allow_html=True)

# 차트 섹션
tab1, tab2, tab3, tab4 = st.tabs(["👩‍💻 상담사", "⏰ 시간대별", "🤖 머신러닝", "🤦 고객페이지"])

with tab1:
    with st.container():
        st.markdown("""
        <div style="background: rgba(255, 255, 255, 0.95); padding: 1.5rem; border-radius: 12px; 
                    box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1); margin-bottom: 1rem;">
            <h3 style="color: #2c3e50; margin-bottom: 1rem;">👩‍💻 상담사</h3>
        </div>
        """, unsafe_allow_html=True)
        col1, col2, col3 = st.columns(3)
        with col1:
            try:
                cons_chart1(df_consultations, df_consultants)
            except Exception as e:
                st.error(f"차트1 로딩 실패: {e}")
        with col2:
            try:
                cons_cahrt2(df_consultants, df_consultations)
            except Exception as e:
                st.error(f"차트2 로딩 실패: {e}")
        with col3:
            try:
                cons_cahrt3(df_consultation_fund_types, df_fund_types)
            except Exception as e:
                st.error(f"차트3 로딩 실패: {e}")

with tab2:
    with st.container():
        st.markdown("""
        <div style="background: rgba(255, 255, 255, 0.95); padding: 1.5rem; border-radius: 12px; 
                    box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1); margin-bottom: 1rem;">
            <h3 style="color: #2c3e50; margin-bottom: 1rem;">⏰시간대별</h3>
        </div>
        """, unsafe_allow_html=True)
        try:
            category_char1(df_customers, df_consultations)
        except Exception as e:
            st.error(f"시간대별 분석 로딩 실패: {e}")

with tab3:
    with st.container():
        st.markdown("""
        <div style="background: rgba(255, 255, 255, 0.95); padding: 1.5rem; border-radius: 12px; 
                    box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1); margin-bottom: 1rem;">
            <h3 style="color: #2c3e50; margin-bottom: 1rem;">🤖머신러닝</h3>
        </div>
        """, unsafe_allow_html=True)
        try:
            predicti(df_tomorrow_predictions, df_predictions, df_consultations)
        except Exception as e:
            st.error(f"머신러닝 분석 로딩 실패: {e}")
        
with tab4:
    with st.container():
        st.markdown("""
        <div style="background: rgba(255, 255, 255, 0.95); padding: 1.5rem; border-radius: 12px; 
                    box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1); margin-bottom: 1rem;">
            <h3 style="color: #2c3e50; margin-bottom: 1rem;">🤦고객페이지</h3>
        </div>
        """, unsafe_allow_html=True)
        tab1, tab2 = st.tabs(['유형별 상담자','많이 찾는서류'])
        with tab1:
            try:
                st.dataframe(consultants_df_sorted, use_container_width=True)
            except Exception as e:
                st.error(f"상담자 데이터 표시 실패: {e}")
        with tab2:
            try:
                st.dataframe(document_t_df, use_container_width=True)
            except Exception as e:
                st.error(f"서류 데이터 표시 실패: {e}")

# 푸터
st.markdown("""
<div style="margin-top: 3rem; padding: 2rem; background: rgba(255, 255, 255, 0.95); 
            border-radius: 12px; text-align: center; box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);">
    <p style="color: #7f8c8d; margin: 0;">© 2025 상담사 관리 시스템 | 마지막 업데이트: {}</p>
</div>
""".format(datetime.now().strftime("%Y-%m-%d %H:%M:%S")), unsafe_allow_html=True)