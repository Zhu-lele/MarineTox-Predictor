import streamlit as st
import pandas as pd
import os

# 页面配置
st.set_page_config(page_title="MarineTox Predictor", layout="wide")

# 设置标题
st.markdown("<h1 style='text-align: center; color: #01579b;'>MarineTox Predictor</h1>", unsafe_allow_html=True)

# 加载数据
@st.cache_data
def load_data():
    file_path = os.path.join(os.path.dirname(__file__), "chemicalhazarddataset-20241231.xlsx")
    if os.path.exists(file_path):
        try:
            return pd.read_excel(file_path, engine="openpyxl")
        except Exception as e:
            st.error(f"❌ Failed to load Excel file: {str(e)}")
            return pd.DataFrame()
    else:
        st.error("❌ Excel file not found. Please ensure it is placed in the root directory.")
        return pd.DataFrame()

df = load_data()

# --- 🔍 左侧搜索栏 ---
with st.sidebar:
    st.markdown("### 🔍 Chemical Search")

    search_by = st.selectbox("Search by", ["Chemical name", "SMILES", "Molecular formula"])

    keyword = st.text_input(f"Enter {search_by}")

    st.markdown(f"#### Or select from {search_by}")
    existing_options = sorted(df[search_by].dropna().unique()) if search_by in df.columns else []
    selected_option = st.selectbox("", existing_options)

    st.divider()

    # ✅ 帮助文档下载按钮
    st.markdown("### 📖 Help File Download")

    help_file_url = "https://github.com/Zhu-lele/MarineTox-Predictor/raw/main/Help%20Files.docx"

    st.markdown(
        f"""
        <a href="{help_file_url}" download target="_blank">
            <button style='background-color:#1e88e5;
                           color:white;
                           padding:10px 20px;
                           border:none;
                           border-radius:6px;
                           font-size:16px;
                           cursor:pointer;
                           margin-top:10px'>
                📥 Download Help File (.docx)
            </button>
        </a>
        """,
        unsafe_allow_html=True
    )

# ✅ 注意：如你原先代码中包含了：
# if st.sidebar.button("📖 Show Help"):
#     st.markdown(...) 或读取 help.txt 内容，请全部删除或注释掉！
