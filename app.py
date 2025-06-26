import streamlit as st
import pandas as pd
import os

# ---------------- 页面基础配置 ----------------
st.set_page_config(page_title="MarineTox Predictor", layout="wide")

# ---------------- 数据加载 ----------------
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

# ---------------- 页面美化 ----------------
st.markdown("""
<style>
/* 设置页面整体样式 */
body {
    font-family: Arial, sans-serif;
    background-color: #f7f7f7;
}

/* 设置标题样式 */
h1 {
    color: #01579b;
    text-align: center;
    font-size: 36px;
    margin-bottom: 30px;
}

/* 设置输入框样式 */
.stTextInput {
    margin: 20px auto;
    width: 60%;
    padding: 12px 20px;
    border-radius: 10px;
    border: 1px solid #ddd;
    font-size: 16px;
}

/* 设置按钮样式 */
.stButton {
    background-color: #01579b;
    color: white;
    padding: 12px 20px;
    border-radius: 10px;
    border: none;
    font-size: 16px;
    cursor: pointer;
}

/* 设置表格展示样式 */
.dataframe {
    background-color: #ffffff;
    border-radius: 10px;
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
    padding: 15px;
    margin-bottom: 20px;
}
</style>
""", unsafe_allow_html=True)

# ---------------- 查询功能 ----------------
st.title("MarineTox Predictor - 查询化学品数据")

# 用户输入化学品名称或SMILES
query = st.text_input("请输入化学品名称或 SMILES 进行查询:")

# 如果用户输入查询，显示结果
if query:
    # 模糊匹配：查询包含输入的化学品名称或SMILES
    query = query.lower().strip()
    filtered_df = df[df["Chemical name"].str.lower().str.contains(query) | df["SMILES"].str.lower().str.contains(query)]
    
    if not filtered_df.empty:
        st.dataframe(filtered_df[['Chemical name', 'SMILES', 'Molecular formula', 'LC50_0', 'LC50_1', 'LC50_2']].style.format({
            'LC50_0': '{:.2f}', 'LC50_1': '{:.2f}', 'LC50_2': '{:.2f}'
        }))
    else:
        st.warning("未找到匹配的化学品，请确保输入正确的名称或SMILES。")
