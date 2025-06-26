import streamlit as st
import pandas as pd
import os

# 页面配置
st.set_page_config(page_title="MarineTox Predictor", layout="wide", initial_sidebar_state="collapsed")

# 加载本地 Excel 数据文件
@st.cache_data
def load_data():
    file_path = os.path.join(os.path.dirname(__file__), "chemicalhazarddataset-20241231.xlsx")

    if os.path.exists(file_path):
        try:
            return pd.read_excel(file_path, engine="openpyxl")
        except Exception as e:
            st.error(f"❌ Excel 文件读取失败：{str(e)}")
            return pd.DataFrame()
    else:
        st.error("❌ 数据文件未找到，请将 Excel 文件放置于应用根目录")
        return pd.DataFrame()

df = load_data()

# 页面样式
page_style = """
<style>
    body {
        background-color: #e3f2fd;
    }
    .title-large {
        font-size: 48px;
        font-weight: bold;
        text-align: center;
        color: #01579b;
        margin-bottom: 40px;
    }
    .main-title {
        font-size: 80px;
        font-weight: bold;
        text-align: center;
        color: #01579b;
        margin-bottom: 50px;
    }
    .description-box {
        font-size: 28px;
        text-align: center;
        color: #01579b;
        margin-bottom: 30px;
    }
    .data-search-button {
        display: block;
        background-color: #01579b;
        color: white;
        font-size: 24px;
        font-weight: bold;
        padding: 20px 50px;
        border-radius: 10px;
        margin: 0 auto;
        text-align: center;
        cursor: pointer;
    }
    .data-search-button:hover {
        background-color: #013b6b;
    }
    /* 样式调整 */
    section[data-testid="stSidebar"] {
        display: none;
    }
</style>
"""
st.markdown(page_style, unsafe_allow_html=True)

# 页面标题和描述
st.markdown('<div class="main-title">MarineTox Predictor</div>', unsafe_allow_html=True)
st.markdown('<div class="description-box">MarineTox Predictor enables end-to-end toxicity predictions for chemical acute and chronic toxicity on 20 marine organisms spanning algae, crustaceans, invertebrates, mollusks and fish simultaneously.</div>', unsafe_allow_html=True)

# Data Search 按钮
if st.button('Data Search', key="data_search", help="Search chemical hazard data"):
    st.experimental_rerun()

# 说明部分
st.markdown("""
<div class="description-box">
    <strong>For more information or inquiries, please contact:</strong><br>
    School of Environmental Science and Technology, Dalian University of Technology, China<br>
    Contact: <b>Zhu_lll@163.com</b>
</div>
""", unsafe_allow_html=True)
