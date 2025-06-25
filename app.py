import streamlit as st
import pandas as pd
import os

st.set_page_config(page_title="MarineTox Predictor", layout="wide")

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

# === 改造版 CSS 样式 ===
custom_style = """
<style>
/* 全局背景 */
body {
    background-color: #f4f7fa;
}

/* 标题样式 */
h1, h2, h3 {
    color: #003366;
    font-weight: bold;
}
.title-main {
    font-size: 48px;
    text-align: center;
    color: #003366;
    margin-top: 20px;
    margin-bottom: 10px;
}
.subtitle {
    font-size: 20px;
    text-align: center;
    color: #336699;
    margin-bottom: 30px;
}

/* 侧边栏 */
section[data-testid="stSidebar"] {
    background-color: #e3ecf3;
}
section[data-testid="stSidebar"] * {
    font-size: 16px;
    color: #003366;
}
.stRadio > label {
    font-size: 18px;
    font-weight: bold;
}

/* 搜索框、下拉菜单 */
.stTextInput > div > input, div[data-baseweb="select"] > div {
    border: 1.5px solid #003366;
    border-radius: 4px;
    font-size: 16px;
    min-height: 2.2em;
}
.stButton > button {
    background-color: #003366;
    color: white;
    border-radius: 4px;
    padding: 0.4em 1em;
}
.stButton > button:hover {
    background-color: #001d3d;
}

/* 结果卡片 */
.result-card {
    background-color: white;
    padding: 20px;
    border-radius: 8px;
    box-shadow: 1px 1px 10px rgba(0,0,0,0.1);
    margin-bottom: 20px;
}
.result-title {
    font-size: 22px;
    color: #003366;
    font-weight: bold;
    margin-bottom: 10px;
}
.data-label {
    font-weight: bold;
    color: #003366;
}
</style>
"""
st.markdown(custom_style, unsafe_allow_html=True)

# === 页面导航 ===
page = st.sidebar.radio("", ["Home", "Data Filters"])

# === HOME 页面 ===
if page == "Home":
    st.markdown('<div class="title-main">MarineTox Predictor</div>', unsafe_allow_html=True)
    st.markdown('<div class="subtitle">Marine Ecotoxicity Hazard Database & End-to-End Toxicity Prediction Tool</div>', unsafe_allow_html=True)
    st.image("https://raw.githubusercontent.com/Zhu-lele/Chemical-Hazard-Database-for-marine-ecological-risk-assessment/main/model_diagram.jpg", use_container_width=True)
    st.info("Developed by: School of Environmental Science and Technology, Dalian University of Technology, China | Contact: Zhu_lll@163.com")

# === DATA FILTERS 页面 ===
elif page == "Data Filters":
    st.markdown('<div class="title-main">MarineTox Predictor</div>', unsafe_allow_html=True)
    st.markdown('<div class="subtitle">Search Chemical Hazard Data</div>', unsafe_allow_html=True)

    with st.sidebar:
        search_column = st.selectbox("Select search column", ["Chemical name", "SMILES", "Molecular formula"])
        search_value = st.text_input(f"Enter exact {search_column}")
        dropdown_value = st.selectbox(f"Or select from {search_column}", [""] + sorted(df[search_column].dropna().unique().tolist()))
        selected_value = search_value.strip() if search_value else dropdown_value

    if selected_value:
        filtered_df = df[df[search_column].astype(str).str.strip().str.lower() == selected_value.lower()]
        if not filtered_df.empty:
            for _, row in filtered_df.iterrows():
                st.markdown('<div class="result-card">', unsafe_allow_html=True)

                col1, col2, col3 = st.columns(3)

                with col1:
                    st.markdown('<div class="result-title">Chemical Information</div>', unsafe_allow_html=True)
                    st.write(f"**Name:** {row['Chemical name']}")
                    st.write(f"**SMILES:** {row['SMILES']}")
                    st.write(f"**Formula:** {row['Molecular formula']}")

                with col2:
                    st.markdown('<div class="result-title">Marine Ecotoxicity [log (mg/L)]</div>', unsafe_allow_html=True)
                    st.write("**LC50 / EC50 Values**")
                    for col in df.columns[3:23]:
                        st.write(f"{col}: {row[col]}")
                    st.write("**NOEC Values**")
                    for col in df.columns[23:27]:
                        st.write(f"{col}: {row[col]}")

                with col3:
                    st.markdown('<div class="result-title">SSD Curve (log-normal)</div>', unsafe_allow_html=True)
                    for col in df.columns[27:32]:
                        st.write(f"{col}: {row[col]}")

                st.markdown('</div>', unsafe_allow_html=True)
        else:
            st.warning(f"No exact match found for `{selected_value}` in `{search_column}`.")
