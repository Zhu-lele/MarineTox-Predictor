import streamlit as st
import pandas as pd
import os
import base64

# 页面配置
st.set_page_config(page_title="MarineTox Predictor", layout="wide")

# 加载数据
# 加载数据
@st.cache_data
def load_data():
    file_path = os.path.join(os.path.dirname(__file__), "chemicalhazarddataset-20250708.xlsx")
    if os.path.exists(file_path):
        try:
            return pd.read_excel(file_path, engine="openpyxl")
        except Exception as e:
            st.error(f"❌ 数据加载失败：{str(e)}")
            return pd.DataFrame()
    else:
        st.error("❌ 未找到数据文件，请放置在应用根目录")
        return pd.DataFrame()

df = load_data()

# 页面样式
page_style = """
<style>
    body { background-color: #f5f8fb; }
    .title { font-size: 55px; font-weight: bold; text-align: center; color: #01579b; margin: 20px 0; }

    /* Sidebar 样式 */
    section[data-testid="stSidebar"] * {
        font-size: 20px !important;
        font-weight: bold !important;
        color: #01579b !important;
    }

    /* 表格字体放大 */
    .stDataFrame div[role="gridcell"], 
    .stDataFrame div[role="columnheader"] {
        font-size: 20px !important;
    }

    /* Chemical 信息字体放大 */
    .element-container h3, .element-container p {
        font-size: 18px !important;
    }
</style>
"""

st.markdown(page_style, unsafe_allow_html=True)
st.markdown('<div class="title">MarineTox Predictor</div>', unsafe_allow_html=True)

# ------------------ 侧边栏 ------------------
with st.sidebar:
    st.markdown("### 🔍 Chemical Search")
    search_column = st.selectbox("Search by", ["Chemical name", "SMILES", "Molecular formula"])
    search_value = st.text_input(f"Enter {search_column}")
    dropdown_value = st.selectbox(f"Or select from {search_column}", [""] + sorted(df[search_column].dropna().unique().tolist()))
    selected_value = search_value.strip() if search_value else dropdown_value

    st.markdown("---")

    # Help 文件下载按钮嵌入侧边栏底部
    help_file_path = os.path.join(os.path.dirname(__file__), "Help Files.docx")
    if os.path.exists(help_file_path):
        with open(help_file_path, "rb") as f:
            help_data = f.read()
            b64_help = base64.b64encode(help_data).decode()

            help_download_link = f'''
                <a href="data:application/vnd.openxmlformats-officedocument.wordprocessingml.document;base64,{b64_help}"
                   download="MarineTox_Help.docx"
                   style="display: inline-block; padding: 0.5em 1em; background-color: #f0f0f0; color: black;
                          text-decoration: none; border-radius: 5px; font-weight: bold;">
                   📄 Click here to download Help File (Word)
                </a>
            '''
            st.markdown("### 📘 Help File Download")
            st.markdown(help_download_link, unsafe_allow_html=True)
    else:
        st.warning("⚠️ Help file not found. Please ensure 'Help Files.docx' exists in the app directory.")

# ------------------ 主页面展示 ------------------
if selected_value:
    filtered_df = df[df[search_column].astype(str).str.strip().str.lower() == selected_value.lower()]
    
    if not filtered_df.empty:
        row = filtered_df.iloc[0]

        col1, col2 = st.columns([1, 2])

        with col1:
            st.markdown("### Chemical Information")
            st.write(f"**Chemical Name:** {row['Chemical name']}")
            st.write(f"**SMILES:** {row['SMILES']}")
            st.write(f"**Molecular Formula:** {row['Molecular formula']}")

        with col2:
            st.markdown("### Marine Ecotoxicity Data [log (mg/L)]")
            lc50_ec50_cols = df.columns[3:23].tolist()
            ecotox_df = pd.DataFrame({
                "Species": lc50_ec50_cols,
                "LC50/EC50": [row[col] for col in lc50_ec50_cols]
            })
            st.dataframe(ecotox_df, hide_index=True)

            # ✅ NOEC Values 表格，去除“.1”
            noec_cols = df.columns[23:27].tolist()
            clean_noec_species = [col.replace(".1", "").strip() for col in noec_cols]

            noec_df = pd.DataFrame({
                "Species": clean_noec_species,
                "NOEC": [row[col] for col in noec_cols]
            })
            st.dataframe(noec_df, hide_index=True)

            # ✅ SSD 曲线展示
            st.markdown("### SSD Curve (log-normal distribution)")
            ssd_cols = df.columns[27:32].tolist()
            ssd_df = pd.DataFrame({
                "Parameter": ssd_cols,
                "Value": [row[col] for col in ssd_cols]
            })
            st.dataframe(ssd_df, hide_index=True)
    else:
        st.warning(f"No match found for `{selected_value}` in `{search_column}`.")

# ------------------ 页脚（联系方式） ------------------
footer = """
<hr style="margin-top: 50px; margin-bottom: 10px;">
<div style="text-align: center; font-size:18px; color:#444;">
    If you have any questions, please contact 
    <a href="mailto:Zhu_lll@163.com" style="color:#01579b; text-decoration:none; font-weight:bold;">
        Zhu_lll@163.com
    </a><br>
    School of Environmental Science and Technology, Dalian University of Technology, Dalian, 116024, China
</div>
"""
st.markdown(footer, unsafe_allow_html=True)


