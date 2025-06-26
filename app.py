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
        font-size: 30px;
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
    section[data-testid="stSidebar"] {
        display: none;
    }
</style>
"""
st.markdown(page_style, unsafe_allow_html=True)

# 选择页面
if "page" not in st.session_state:
    st.session_state.page = "home"  # 默认显示主页

# 页面标题和描述
st.markdown('<div class="main-title">MarineTox Predictor</div>', unsafe_allow_html=True)
st.markdown("""
    <div class="description-box">
        MarineTox Predictor enables end-to-end toxicity predictions for chemical acute and chronic toxicity on 20 marine organisms spanning algae, crustaceans, invertebrates, mollusks and fish simultaneously.
    </div>
""", unsafe_allow_html=True)

# 显示 Data Search 按钮
if st.button('Data Search', key="data_search", help="Search chemical hazard data"):
    st.session_state.page = "data_filters"  # 按钮点击后显示查询页面

# ------------------------- 页面内容 -------------------------
if st.session_state.page == "home":
    st.write("Welcome to the MarineTox Predictor! Click the button below to start searching chemical data.")
    # 主页内容可以根据需求扩展

elif st.session_state.page == "data_filters":
    st.markdown("<h2 style='text-align: center;'>Search Chemical Hazard Data</h2>", unsafe_allow_html=True)
    search_column = st.selectbox("Select search column", ["Chemical name", "SMILES", "Molecular formula"])
    search_value = st.text_input(f"Enter exact {search_column}")
    dropdown_value = st.selectbox(f"Or select from {search_column}", [""] + sorted(df[search_column].dropna().unique().tolist()))
    selected_value = search_value.strip() if search_value else dropdown_value

    if selected_value:
        filtered_df = df[df[search_column].astype(str).str.strip().str.lower() == selected_value.lower()]

        if not filtered_df.empty:
            for i, row in filtered_df.iterrows():
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.subheader("Chemical Information")
                    st.write(f"**Chemical Name:** {row['Chemical name']}")
                    st.write(f"**SMILES:** {row['SMILES']}")
                    st.write(f"**Molecular Formula:** {row['Molecular formula']}")

                with col2:
                    st.subheader("Marine Ecotoxicity Data [log (mg/L)]")
                    lc50_ec50_cols = df.columns[3:23].tolist()
                    for col in lc50_ec50_cols:
                        st.write(f"**{col}:** {row[col]}")

                    noec_cols = df.columns[23:27].tolist()
                    st.markdown("**🔸 NOEC Values**")
                    for col in noec_cols:
                        st.write(f"**{col}:** {row[col]}")

                with col3:
                    st.subheader("SSD Curve (log-normal distribution)")
                    ssd_cols = df.columns[27:32].tolist()
                    for col in ssd_cols:
                        st.write(f"**{col}:** {row[col]}")
        else:
            st.warning(f"No exact match found for `{selected_value}` in `{search_column}`.")
