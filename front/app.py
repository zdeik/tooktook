import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import plotly.express as px

def cons_chart1(consultations_df, consultants_df):
    """
    FastAPI에서 받아온 데이터를 사용하는 상담사 차트 함수
    """
    # 데이터 타입 변환 및 파생 변수 생성
    consultations_df = consultations_df.copy()
    consultants_df = consultants_df.copy()
    
    consultations_df['consultation_date'] = pd.to_datetime(consultations_df['consultation_date'])
    consultations_df['start_time'] = pd.to_datetime(consultations_df['start_time'])
    consultations_df['end_time'] = pd.to_datetime(consultations_df['end_time'])
    consultants_df['join_date'] = pd.to_datetime(consultants_df['join_date'])
    
    consultations_df['duration_minutes'] = (consultations_df['end_time'] - consultations_df['start_time']).dt.total_seconds() / 60
    
    merged_df = pd.merge(consultations_df, consultants_df, on='consultant_id', how='left')

    # 필터링
    col1, col2 = st.columns(2)

    with col1:
        period_options = ['전체', '최근 7일', '최근 30일', '이번 달', '지난 달']
        selected_period = st.selectbox(
            '기간 선택', 
            period_options,
            label_visibility='collapsed'
        )

    today = datetime.today().date()
    if selected_period == '전체':
        start_date = merged_df['consultation_date'].min().date()
        end_date = merged_df['consultation_date'].max().date()
    elif selected_period == '최근 7일':
        start_date = today - timedelta(days=7)
        end_date = today
    elif selected_period == '최근 30일':
        start_date = today - timedelta(days=30)
        end_date = today
    elif selected_period == '이번 달':
        start_date = today.replace(day=1)
        end_date = today
    elif selected_period == '지난 달':
        first_day_of_this_month = today.replace(day=1)
        end_date = first_day_of_this_month - timedelta(days=1)
        start_date = end_date.replace(day=1)

    with col2:
        date_range = st.date_input(
            '날짜 범위:',
            [start_date, end_date],
            label_visibility='collapsed'
        )

    if date_range and len(date_range) == 2:
        start_date_filter, end_date_filter = date_range[0], date_range[1]
        filtered_df = merged_df[
            (merged_df['consultation_date'].dt.date >= start_date_filter) &
            (merged_df['consultation_date'].dt.date <= end_date_filter)
        ]
    else:
        filtered_df = merged_df.copy()

    # 차트
    if not filtered_df.empty:
        consultant_performance = filtered_df.groupby('name').agg(
            총상담건수=('consultation_id', 'count'),
            평균만족도=('satisfaction_score', 'mean'),
            평균소요시간=('duration_minutes', 'mean')
        ).reset_index().sort_values(by='총상담건수', ascending=False)

        pastel_colors = ["#AEC6CF", "#FFD1DC", "#BFD8B8", "#FFFACD", "#CBAACB", "#FFB347", "#77DD77", "#FDFD96"]
        fig = px.bar(
            consultant_performance,
            x='name',
            y='총상담건수',
            title='상담사별 총 상담 건수',
            labels={'name': '상담사 이름', '총상담건수': '총 상담 건수'},
            hover_data=['평균만족도', '평균소요시간'],
            color='name',
            color_discrete_sequence=pastel_colors
        )
        
        fig.update_traces(
            hovertemplate="<b>%{x}</b><br><br>" +
                        "총 상담건수: %{y}건<br>" +
                        "평균 만족도: %{customdata[0]:.2f}점<br>" +
                        "평균 소요시간: %{customdata[1]:.1f}분<extra></extra>"
        )

        st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning("선택된 필터에 해당하는 데이터가 없습니다.")

if __name__ == "__main__":
    st.error("이 모듈은 직접 실행할 수 없습니다. main.py를 통해 실행하세요.")