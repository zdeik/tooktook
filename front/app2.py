import streamlit as st
import pandas as pd
import plotly.express as px

def cons_cahrt2(consultants_df, consultations_df):
    """
    FastAPI에서 받아온 데이터를 사용하는 상담사별 평균 시간 차트 함수
    """
    # 데이터 준비 (copy를 사용해서 원본 데이터 보호)
    consultants_df = consultants_df.copy()
    consultations_df = consultations_df.copy()

    # 데이터 병합 및 가공
    merged_df = pd.merge(consultations_df, consultants_df, on='consultant_id')
    merged_df['start_time'] = pd.to_datetime(merged_df['start_time'])
    merged_df['end_time'] = pd.to_datetime(merged_df['end_time'])
    merged_df['duration_minutes'] = (merged_df['end_time'] - merged_df['start_time']).dt.total_seconds() / 60

    avg_duration_by_consultant = merged_df.groupby('name')['duration_minutes'].mean().reset_index()
    avg_duration_by_consultant.columns = ['상담자 이름', '평균 상담 시간 (분)']
    data = avg_duration_by_consultant.sort_values(by='평균 상담 시간 (분)', ascending=False)

    # 대시보드 제목
    st.subheader("상담자별 평균 상담 시간")

    # 차트 생성
    if not data.empty:
        min_duration = data['평균 상담 시간 (분)'].min()
        max_duration = data['평균 상담 시간 (분)'].max()
        range_y_min = max(0, min_duration - 1)
        range_y_max = max_duration + 1

        # 차트 속성
        pastel_colors = ["#AEC6CF", "#FFD1DC", "#BFD8B8", "#FFFACD", "#CBAACB", "#FFB347", "#77DD77", "#FDFD96"]
        fig = px.bar(
            data,
            x='상담자 이름',
            y='평균 상담 시간 (분)',
            title='상담자별 평균 상담 시간 (분)',
            labels={'평균 상담 시간 (분)': '평균 시간 (분)'},
            color='상담자 이름',
            color_discrete_sequence=pastel_colors,
            range_y=[range_y_min, range_y_max]
        )

        st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning("데이터가 없습니다.")

if __name__ == "__main__":
    st.error("이 모듈은 직접 실행할 수 없습니다. main.py를 통해 실행하세요.")