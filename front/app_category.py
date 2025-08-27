import streamlit as st
import pandas as pd 
import matplotlib.pyplot as plt
import matplotlib as mpl
import plotly.express as px

def category_char1(customers_df, consultations_df):
    """
    FastAPI에서 받아온 데이터를 사용하는 카테고리별 분석 함수
    """
    # 한글폰트 Noto Sans KR
    mpl.rcParams['font.family'] = 'Noto Sans KR'
    mpl.rcParams['axes.unicode_minus'] = False

    st.title("상담 데이터 분석 대시보드")

    # 데이터 복사 (원본 보호)
    customers_df = customers_df.copy()
    consultations_df = consultations_df.copy()

    # 데이터 타입 변환
    consultations_df['start_time'] = pd.to_datetime(consultations_df['start_time'])
    consultations_df['consultation_date'] = pd.to_datetime(consultations_df['consultation_date'])

    # 1. 카테고리별 평균 시간
    merged_df = pd.merge(customers_df, consultations_df, on='customer_id', how='inner')
    
    # 시작 시간 평균 계산
    merged_df['start_hour'] = merged_df['start_time'].dt.hour
    merged_df['start_minute'] = merged_df['start_time'].dt.minute
    merged_df['start_time_minutes'] = merged_df['start_hour'] * 60 + merged_df['start_minute']
    
    result_cat = merged_df.groupby('business_type')['start_time_minutes'].mean().reset_index()
    result_cat['시간'] = result_cat['start_time_minutes'].apply(
        lambda x: f"{int(x//60):02d}:{int(x%60):02d}"
    )
    result_cat = result_cat[['business_type', '시간']].rename(columns={'business_type': '업종'})
    
    st.subheader("업종별 평균 상담 시작 시간")
    st.dataframe(result_cat, use_container_width=True)

    # 2. 최근 1달 상담 추이 (시간대별 건수)
    consultations_df['hour'] = consultations_df['start_time'].dt.hour
    result_hourly = consultations_df.groupby('hour').size().reset_index(name='COUNT')
    result_hourly.columns = ['time', 'COUNT']

    st.subheader("최근 1달 상담 추이 (시간대별)")
    
    # Plotly로 차트 생성 (matplotlib 대신)
    fig = px.bar(
        result_hourly,
        x='time',
        y='COUNT',
        title='최근 1달 상담 추이 (시간대별)',
        labels={'time': '시간대 (시)', 'COUNT': '상담 건수 (건)'},
        color='COUNT',
        color_continuous_scale='Blues'
    )
    
    fig.update_layout(
        xaxis_title='시간대 (시)',
        yaxis_title='상담 건수 (건)',
        showlegend=False
    )
    
    # 막대 위에 값 표시
    fig.update_traces(
        text=result_hourly['COUNT'],
        textposition='outside'
    )
    
    st.plotly_chart(fig, use_container_width=True)

    # 3. 최근 1달 상담 추이 (분 단위)
    consultations_df['minute'] = consultations_df['start_time'].dt.minute
    result_minute = consultations_df.groupby('minute').size().reset_index(name='COUNT')
    result_minute.columns = ['time', 'COUNT']
    
    st.subheader("최근 1달 상담 추이 (분 단위)")
    st.dataframe(result_minute, use_container_width=True)

    # 4. 업종별 상담 건수 분포 (추가 분석)
    business_count = merged_df.groupby('business_type').size().reset_index(name='상담건수')
    business_count = business_count.sort_values('상담건수', ascending=False)
    
    st.subheader("업종별 상담 건수 분포")
    fig_business = px.pie(
        business_count,
        values='상담건수',
        names='business_type',
        title='업종별 상담 건수 분포',
        color_discrete_sequence=px.colors.qualitative.Pastel
    )
    st.plotly_chart(fig_business, use_container_width=True)

if __name__ == "__main__":
    st.error("이 모듈은 직접 실행할 수 없습니다. main.py를 통해 실행하세요.")