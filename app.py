import streamlit as st
import pandas as pd
import os

# 页面配置
st.set_page_config(page_title="MarineTox Predictor", layout="wide")

# 页面样式
page_style = """
<style>
    body { background-color: #f5f8fb; }
    .title { font-size: 55px; font-weight: bold; text-align: center; color: #01579b; margin: 20px 0; }
    section[data-testid="stSidebar"] * {
        font-size: 20px !important;
        font-weight: bold !important;
        color: #01579b !important;
    }
</style>
"""
st.markdown(page_style, unsafe_allow_html=True)

# 页面标题
st.markdown('<div class="title">MarineTox Predictor</div>', unsafe_allow_html=True)

# =================== 加载数据 ====================
@st.cache_data
def load_data():
    file_path = os.path.join(os.path.dirname(__file__), "chemicalhazarddataset-20241231.xlsx")
    if os.path.exists(file_path):
        try:
            return pd.read_excel(file_path, engine="openpyxl")
        except Exception as e:
            st.error(f"❌ 数据加载失败：{str(e)}")
            return pd.DataFrame()
    else:
        st.error("❌ 未找到数据文件，请放置于项目根目录")
        return pd.DataFrame()

df = load_data()

# =================== 侧边栏 ====================
with st.sidebar:
    st.markdown("### 🔍 Chemical Search")
    search_column = st.selectbox("Search by", ["Chemical name", "SMILES", "Molecular formula"])
    search_value = st.text_input(f"Enter {search_column}")
    dropdown_value = st.selectbox(f"Or select from {search_column}", [""] + sorted(df[search_column].dropna().unique().tolist()))
    selected_value = search_value.strip() if search_value else dropdown_value

    st.markdown("---")
    st.markdown("### 📄 Download Help File")

    try:
        with open("Help Files.docx", "rb") as file:
            st.download_button(
                label="📥 Click to Download Help (.docx)",
                data=file,
                file_name="MarineTox_Help.docx",
                mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
            )
    except FileNotFoundError:
        st.warning("⚠️ Help 文件未找到，请将 'Help Files.docx' 放入项目目录。")

# =================== 主页面展示 ====================
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

            st.markdown("### NOEC Values")
            noec_cols = df.columns[23:27].tolist()
            noec_df = pd.DataFrame({
                "Species": noec_cols,
                "NOEC": [row[col] for col in noec_cols]
            })
            st.dataframe(noec_df, hide_index=True)

            st.markdown("### SSD Curve (log-normal distribution)")
            ssd_cols = df.columns[27:32].tolist()
            ssd_df = pd.DataFrame({
                "Parameter": ssd_cols,
                "Value": [row[col] for col in ssd_cols]
            })
            st.dataframe(ssd_df, hide_index=True)

    else:
        st.warning(f"No match found for `{selected_value}` in `{search_column}`.")
