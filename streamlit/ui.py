import streamlit as st
def ui_css():
    # 커스텀 CSS
    st.markdown("""
    <style>
        /* 메인 배경 */
        .stApp {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        }
        
        /* 헤더 스타일 */
        .main-header {
            background: rgba(255, 255, 255, 0.95);
            padding: 2rem;
            border-radius: 15px;
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
            backdrop-filter: blur(10px);
            border: 1px solid rgba(255, 255, 255, 0.2);
            margin-bottom: 2rem;
            text-align: center;
        }
        
        /* 카드 스타일 */
        .metric-card {
            background: rgba(255, 255, 255, 0.95);
            padding: 1.5rem;
            border-radius: 12px;
            box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
            backdrop-filter: blur(10px);
            border: 1px solid rgba(255, 255, 255, 0.2);
            text-align: center;
            transition: transform 0.3s ease;
        }
        
        .metric-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 8px 25px rgba(0, 0, 0, 0.15);
        }
        
        /* 사이드바 스타일 */
        .css-1d391kg {
            background: rgba(255, 255, 255, 0.95);
            backdrop-filter: blur(10px);
        }
        
        /* 버튼 스타일 */
        .stButton > button {
            background: linear-gradient(45deg, #667eea, #764ba2);
            color: white;
            border: none;
            border-radius: 25px;
            padding: 0.5rem 2rem;
            font-weight: 600;
            transition: all 0.3s ease;
        }
        
        .stButton > button:hover {
            transform: translateY(-2px);
            box-shadow: 0 5px 15px rgba(0, 0, 0, 0.2);
        }
        
        /* 선택박스 스타일 */
        .stSelectbox > div > div {
            background: rgba(255, 255, 255, 0.9);
            border-radius: 10px;
        }
        
        /* 데이터프레임 스타일 */
        .dataframe {
            background: rgba(255, 255, 255, 0.95);
            border-radius: 10px;
            overflow: hidden;
        }
        
        /* 메트릭 숫자 스타일 */
        .metric-value {
            font-size: 2.5rem;
            font-weight: bold;
            color: #2c3e50;
            margin-bottom: 0.5rem;
        }
        
        .metric-label {
            font-size: 1rem;
            color: #7f8c8d;
            font-weight: 500;
        }
        
        /* 상태 배지 */
        .status-badge {
            padding: 0.3rem 0.8rem;
            border-radius: 20px;
            font-size: 0.8rem;
            font-weight: 600;
            display: inline-block;
        }
        
        .status-active {
            background: #d4edda;
            color: #155724;
        }
        
        .status-inactive {
            background: #f8d7da;
            color: #721c24;
        }
        
        .status-busy {
            background: #fff3cd;
            color: #856404;
        }
    </style>
    """, unsafe_allow_html=True)