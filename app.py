import streamlit as st
import pandas as pd
from io import StringIO

# 页面配置
st.set_page_config(page_title="Chemical Hazard Database", layout="wide")

# 加载数据
@st.cache_data
def load_data():
    file_url = "https://raw.githubusercontent.com/Zhu-lele/Chemical-Hazard-Database-for-marine-ecological-risk-assessment/main/Chemical-hazard-database-20250314.csv"
    return pd.read_csv(file_url)

df = load_data()

# 页面样式（蓝色主题 + 字号放大 + 极简设计）
page_style = """
<style>
    body {
        background-color: #e3f2fd;  /* 浅蓝背景 */
    }
    .title-large {
        font-size: 48px;  /* 页面标题扩大2倍 */
        font-weight: bold;
        text-align: center;
        color: #01579b;
        margin-bottom: 40px;
    }
    .main-title {
        font-size: 130px;  /* MarineTox Predictor 扩大5倍 */
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
        font-size: 18px;
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

# 页面导航（无图标）
page = st.sidebar.radio("", ["Home", "Data Filters"])

# ========================== 1️⃣ HOME ==========================
if page == "Home":
    st.markdown('<div class="main-title">MarineTox Predictor</div>', unsafe_allow_html=True)
    st.markdown('<div class="description-box">ChemMarineTox, a multi-task deep learning model for end-to-end prediction of chemical toxicity on 18 marine organisms and five freshwater organisms.</div>', unsafe_allow_html=True)
    st.image("https://raw.githubusercontent.com/Zhu-lele/Chemical-Hazard-Database-for-marine-ecological-risk-assessment/main/model_diagram.png", use_container_width=True)
    st.markdown("""
        <div class="contact-box">
            Developed by Key Laboratory of Industrial Ecology and Environmental Engineering (MOE), Dalian University of Technology<br>
            Contact: <b>Zhu_lll@163.com</b>
        </div>
    """, unsafe_allow_html=True)

# ========================== 2️⃣ DATA FILTERS ==========================
elif page == "Data Filters":
    st.markdown('<div class="title-large">Search or Upload CAS for Batch Toxicity Data</div>', unsafe_allow_html=True)

    # --------- 显示表头 ----------
    st.subheader("Dataset Column Preview")
    st.dataframe(pd.DataFrame(columns=df.columns.tolist()), height=100)

    # --------- 单项查找 ----------
    with st.sidebar:
        st.markdown("### Single Entry Search")
        search_column = st.selectbox("Select search column", ["CAS", "Name", "SMILES"])
        search_value = st.text_input(f"Enter {search_column}")
        dropdown_value = st.selectbox(f"Or select from {search_column}", [""] + sorted(df[search_column].dropna().unique().tolist()))
        selected_value = search_value.strip() if search_value else dropdown_value

    if selected_value:
        filtered_df = df[df[search_column].astype(str).str.contains(selected_value, case=False, na=False)]
        st.write(f"Showing results for {search_column}: {selected_value}")
        st.dataframe(filtered_df, height=500)

    # --------- 批量查找 ----------
    st.markdown("### Upload CSV for Batch Search by CAS")

    # 下载模板
    cas_template = pd.DataFrame({"CAS": ["50-00-0", "75-07-0", "108-88-3"]})
    template_csv = cas_template.to_csv(index=False).encode("utf-8")
    st.download_button("Download CAS Template CSV", data=template_csv, file_name="CAS_batch_template.csv", mime="text/csv")

    uploaded_file = st.file_uploader("Upload your CAS list CSV file", type=["csv"])

    if uploaded_file:
        try:
            content = pd.read_csv(uploaded_file)

            if "CAS" not in content.columns:
                st.error("The uploaded file must contain a column named 'CAS'.")
            elif content["CAS"].isnull().any() or content["CAS"].astype(str).str.strip().eq("").any():
                st.error("The file contains empty or invalid CAS entries.")
            else:
                cas_list = content["CAS"].dropna().astype(str).str.strip().unique().tolist()
                matched_df = df[df["CAS"].astype(str).isin(cas_list)]

                if not matched_df.empty:
                    st.write("Matching results:")
                    st.dataframe(matched_df, height=500)

                    # 显示未匹配项
                    unmatched = sorted(set(cas_list) - set(matched_df["CAS"].astype(str)))
                    if unmatched:
                        st.warning("The following CAS numbers were not found:")
                        st.code(", ".join(unmatched))

                    # 下载匹配结果
                    download_csv = matched_df.to_csv(index=False).encode("utf-8")
                    st.download_button("Download Batch Search Result", data=download_csv, file_name="batch_search_result.csv", mime="text/csv")
                else:
                    st.error("None of the uploaded CAS numbers were found.")

        except Exception as e:
            st.error(f"Failed to process the uploaded file: {e}")
