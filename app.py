import streamlit as st
import pandas as pd
import os

# 页面配置
st.set_page_config(page_title="MarineTox Predictor", layout="wide")
# 加载本地 Excel 数据文件
@st.cache_data
def load_data():
    file_path = os.path.join(os.path.dirname(__file__), "chemicalhazarddataset-20241231.xlsx")

    if os.path.exists(file_path):
        try:
            # 显式指定 openpyxl 引擎
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
    .contact-box {
        font-size: 25px;
        text-align: center;
        color: white;
        background-color: #01579b;
        padding: 15px;
        border-radius: 10px;
        margin-top: 30px;
    }
    section[data-testid="stSidebar"] * {
        font-size: 24px !important;
        font-weight: bold !important;
        color: #01579b !important;
    }

    /* ✅ 下拉菜单字体大小优化，防止文字显示不全 */
    div[data-baseweb="select"] > div {
        font-size: 18px !important;
        line-height: 1.2em !important;
        min-height: 2em !important;
    }
</style>
"""
st.markdown(page_style, unsafe_allow_html=True)

# 页面导航
page = st.sidebar.radio("", ["Home", "Data Filters"])

# ========================== HOME 页面 ==========================
if page == "Home":
    st.markdown('<div class="main-title">MarineTox Predictor</div>', unsafe_allow_html=True)
    st.markdow
