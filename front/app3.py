import streamlit as st
import pandas as pd
import plotly.express as px

def cons_cahrt3(consultation_fund_types_df, fund_types_df):
    """
    FastAPI에서 받아온 데이터를 사용하는 자금 유형별 상담 건수 차트 함수
    """
    st.subheader("자금 유형별 상담 건수")

    # 데이터 복사 (원본 보호)
    consultation_fund_types_df = consultation_fund_types_df.copy()
    fund_types_df = fund_types_df.copy()

    # 데이터 병합 및 집계
    if not consultation_fund_types_df.empty and not fund_types_df.empty:
        merged_df = pd.merge(consultation_fund_types_df, fund_types_df, on='fund_type_id', how='left')
        fund_type_counts = merged_df.groupby('fund_type_name').size().reset_index(name='상담 건수')
        fund_type_counts_sorted = fund_type_counts.sort_values(by='상담 건수', ascending=False)

        # 차트 생성
        if not fund_type_counts_sorted.empty:
            pastel_colors = ["#AEC6CF", "#FFD1DC", "#BFD8B8", "#FFFACD", "#CBAACB", "#FFB347", "#77DD77", "#FDFD96"]
            fig = px.bar(
                fund_type_counts_sorted,
                x='fund_type_name',
                y='상담 건수',
                title='자금 유형별 상담 건수',
                labels={'fund_type_name': '자금 유형', '상담 건수': '총 상담 건수'},
                color='fund_type_name',
                color_discrete_sequence=pastel_colors,
                text='상담 건수',
                range_y=[fund_type_counts_sorted['상담 건수'].min(), fund_type_counts_sorted['상담 건수'].max()]
            )
            
            fig.update_layout(
                xaxis_title='자금 유형',
                yaxis_title='총 상담 건수',
                xaxis=dict(tickangle=-45)
            )

            st.plotly_chart(fig, use_container_width=True)
        else:
            st.warning("자금 유형 데이터가 없습니다.")
    else:
        st.warning("필요한 데이터가 없습니다.")

if __name__ == "__main__":
    st.error("이 모듈은 직접 실행할 수 없습니다. main.py를 통해 실행하세요.")