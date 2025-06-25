import streamlit as st
import pandas as pd
import os

# 页面配置
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

# 页面样式
page_style = """
<style>
body {
    background-color: #e3f2fd;
}
h1, h2, h3, h4 {
    color: #01579b;
}
.stButton > button {
    background-color: #01579b;
    color: white;
    border-radius: 8px;
    padding: 0.5em 1em;
    font-size: 18px;
}
.stButton > button:hover {
    background-color: #003f6b;
}
.stTextInput > div > input {
    border: 2px solid #01579b;
    border-radius: 5px;
    font-size: 16px;
}
div[data-baseweb="select"] > div {
    font-size: 16px;
    border: 2px solid #01579b;
    border-radius: 5px;
    min-height: 2.5em;
}
section[data-testid="stSidebar"] * {
    font-size: 20px !important;
    font-weight: bold !important;
    color: #01579b !important;
}
.card {
    background-color: white;
    padding: 20px;
    border-radius: 15px;
    box-shadow: 2px 2px 10px rgba(0,0,0,0.1);
    margin-bottom: 20px;
}
.title-large {
    font-size: 60px;
    font-weight: bold;
    text-align: center;
    color: #01579b;
    margin-bottom: 30px;
}
.subtitle {
    font-size: 28px;
    text-align: center;
    color: #01579b;
    margin-bottom: 30px;
}
.contact-box {
    font-size: 20px;
    text-align: center;
    color: white;
    background-color: #01579b;
    padding: 15px;
    border-radius: 10px;
    margin-top: 30px;
}
</style>
"""
st.markdown(page_style, unsafe_allow_html=True)

# 页面导航
page = st.sidebar.radio("", ["Home", "Data Filters"])

# ------------------ HOME 页面 ------------------
if page == "Home":
    st.markdown('<div class="title-large">MarineTox Predictor</div>', unsafe_allow_html=True)
    st.markdown('<div class="subtitle">End-to-end toxicity predictions for marine organisms</div>', unsafe_allow_html=True)
    st.image("https://raw.githubusercontent.com/Zhu-lele/Chemical-Hazard-Database-for-marine-ecological-risk-assessment/main/model_diagram.jpg", use_container_width=True)
    st.markdown("""
        <div class="contact-box">
            School of Environmental Science and Technology, Dalian University of Technology, China<br>
            Contact: <b>Zhu_lll@163.com</b>
        </div>
    """, unsafe_allow_html=True)

# ------------------ DATA FILTERS 页面 ------------------
elif page == "Data Filters":
    st.markdown('<div class="title-large">MarineTox Predictor</div>', unsafe_allow_html=True)
    st.markdown('<div class="subtitle">Search Chemical Hazard Data</div>', unsafe_allow_html=True)

    with st.sidebar:
        search_column = st.selectbox("Select search column", ["Chemical name", "SMILES", "Molecular formula"])
        search_value = st.text_input(f"Enter exact {search_column}")
        dropdown_value = st.selectbox(f"Or select from {search_column}", [""] + sorted(df[search_column].dropna().unique().tolist()))
        selected_value = search_value.strip() if search_value else dropdown_value

    if selected_value:
        filtered_df = df[df[search_column].astype(str).str.strip().str.lower() == selected_value.lower()]
        if not filtered_df.empty:
            for i, row in filtered_df.iterrows():
                
                st.markdown('<div class="card">', unsafe_allow_html=True)
                col1, col2, col3 = st.columns(3)

                with col1:
                    st.subheader("Chemical Information")
                    st.write(f"**Name:** {row['Chemical name']}")
                    st.write(f"**SMILES:** {row['SMILES']}")
                    st.write(f"**Formula:** {row['Molecular formula']}")

                with col2:
                    st.subheader("Marine Ecotoxicity [log (mg/L)]")
                    st.markdown("**LC50 / EC50 Values**")
                    for col in df.columns[3:23]:
                        st.write(f"**{col}:** {row[col]}")
                    st.markdown("**NOEC Values**")
                    for col in df.columns[23:27]:
                        st.write(f"**{col}:** {row[col]}")

                with col3:
                    st.subheader("SSD Curve (log-normal)")
                    for col in df.columns[27:32]:
                        st.write(f"**{col}:** {row[col]}")
                
                st.markdown('</div>', unsafe_allow_html=True)

        else:
            st.warning(f"No exact match found for `{selected_value}` in `{search_column}`.")
