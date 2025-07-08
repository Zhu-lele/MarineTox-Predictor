import streamlit as st
import pandas as pd

# 页面设置
st.set_page_config(page_title="MarineTox Predictor", layout="wide")

# 页面主标题
st.markdown("<h1 style='text-align: center; color: #01579b;'>MarineTox Predictor</h1>", unsafe_allow_html=True)

# 🔍 侧边栏：Chemical Search 功能
with st.sidebar:
    st.markdown("🔍 **Chemical Search**")

    # 选择搜索类型
    search_type = st.selectbox("Search by", ["Chemical name", "SMILES", "Molecular formula"])
    
    # 文本输入框
    input_text = st.text_input(f"Enter {search_type}")
    
    # 下拉列表供选择
    st.markdown("Or select from Chemical name")
    chemical_list = ['"amyl nitrite", mixed isomers']  # 示例内容，可替换为真实数据
    selected_chemical = st.selectbox("", chemical_list)

    st.markdown("---")

    # 📖 帮助文档下载区域
    st.markdown("📖 **Help File Download**")

    # Word文档的 GitHub 原始链接（确保是 raw 形式）
    help_file_url = "https://github.com/Zhu-lele/MarineTox-Predictor/raw/main/Help%20Files.docx"

    # 下载按钮（点击后下载 .docx 文件）
    st.markdown(
        f"""
        <a href="{help_file_url}" download target="_blank">
            <button style='background-color:#4da6ff;
                           color:white;
                           padding:10px 20px;
                           border:none;
                           border-radius:6px;
                           font-size:16px;
                           cursor:pointer;'>
                📥 Download Help File
            </button>
        </a>
        """,
        unsafe_allow_html=True
    )
