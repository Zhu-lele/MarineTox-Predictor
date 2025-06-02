import streamlit as st
import pandas as pd
import os

# 页面配置
st.set_page_config(page_title="MarineTox Predictor", layout="wide")

# 加载本地数据文件
@st.cache_data
def load_data():
    file_path = "chemical hazard databaset-20241231V2.csv"
    if os.path.exists(file_path):
        return pd.read_csv(file_path)
    else:
        st.error("❌ 数据文件未找到，请将 CSV 文件放置于应用根目录")
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
    st.markdown('<div class="description-box">MarineTox Predictor enables end-to-end toxicity predictions of 29 subtasks for chemical toxicity on 19 marine organisms and five freshwater organisms spanning algae, crustaceans, invertebrates, molluscs and fish simultaneously.</div>', unsafe_allow_html=True)
    st.image("https://raw.githubusercontent.com/Zhu-lele/Chemical-Hazard-Database-for-marine-ecological-risk-assessment/main/model_diagram.jpg", use_container_width=True)
    st.markdown("""
        <div class="contact-box">
            School of Environmental Science and Technology, Dalian University of Technology, China<br>
            Contact: <b>Zhu_lll@163.com</b>
        </div>
    """, unsafe_allow_html=True)

# ========================== DATA FILTERS 页面 ==========================
elif page == "Data Filters":
    st.markdown('<div class="title-large">Search Chemical Toxicity Data</div>', unsafe_allow_html=True)

    with st.sidebar:
        search_column = st.selectbox("Select search column", ["Chemical name", "SMILES", "Molecular formula"])
        search_value = st.text_input(f"Enter exact {search_column} value")
        dropdown_value = st.selectbox(f"Or select from {search_column}", [""] + sorted(df[search_column].dropna().unique().tolist()))
        selected_value = search_value.strip() if search_value else dropdown_value

    if selected_value:
        # 精准匹配（不区分大小写，去除空格）
        filtered_df = df[df[search_column].astype(str).str.strip().str.lower() == selected_value.lower()]

        if not filtered_df.empty:
            st.write(f"🔍 Showing results for **{search_column}**: `{selected_value}`")

            for i, row in filtered_df.iterrows():
                col1, col2, col3 = st.columns(3)

                with col1:
                    st.subheader("Chemical Information")
                    st.write(f"**Chemical Name:** {row['Chemical name']}")
                    st.write(f"**SMILES:** {row['SMILES']}")
                    st.write(f"**Molecular Formula:** {row['Molecular formula']}")

                with col2:
                    st.subheader("Marine Ecotoxicity Data")
                    ecotox_cols = df.columns[3:24].tolist() + df.columns[24:28].tolist()
                    for col in ecotox_cols:
                        st.write(f"**{col}:** {row[col]}")

                with col3:
                    st.subheader("SSD Curve")
                    ssd_cols = df.columns[27:32].tolist()
                    for col in ssd_cols:
                        st.write(f"**{col}:** {row[col]}")
        else:
            st.warning(f"No exact match found for `{selected_value}` in `{search_column}`.")
