import streamlit as st
import pandas as pd
from io import StringIO

# 页面配置
st.set_page_config(page_title="MarineTox Predictor", layout="wide")

# 加载数据
@st.cache_data
def load_data():
    file_url = "https://raw.githubusercontent.com/Zhu-lele/Chemical-Hazard-Database-for-marine-ecological-risk-assessment/main/Chemical-hazard-database-20250314.csv"
    return pd.read_csv(file_url)

df = load_data()

# 页面样式：蓝色主题 + 大字号 + 侧边栏样式优化
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

    /* 👇 侧边栏样式优化 👇 */
    section[data-testid="stSidebar"] * {
        font-size: 24px !important;
        font-weight: bold !important;
        color: #01579b !important;
    }
    section[data-testid="stSidebar"] h3 {
        font-size: 24px !important;
        font-weight: bold;
    }
    section[data-testid="stSidebar"] input,
    section[data-testid="stSidebar"] select {
        height: 24px !important;
        font-size: 22px !important;
        padding: 10px !important;
    }
    /* 当前选中的下拉项样式（例如：Name） */
    section[data-testid="stSidebar"] div[data-baseweb="select"] div {
        font-size: 18px !important;
        font-weight: bold !important;
        color: #01579b !important;
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
    st.markdown('<div class="title-large">Search or Upload CAS for Batch Toxicity Data</div>', unsafe_allow_html=True)

    # ❌ 已删除 Dataset Column Preview
    # st.subheader("Dataset Column Preview")
    # st.dataframe(pd.DataFrame(columns=df.columns.tolist()), height=100)

    # --------- 单项查找 ----------
    with st.sidebar:
        # ❌ 已删除 "Single Entry Search"
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

                    unmatched = sorted(set(cas_list) - set(matched_df["CAS"].astype(str)))
                    if unmatched:
                        st.warning("The following CAS numbers were not found:")
                        st.code(", ".join(unmatched))

                    download_csv = matched_df.to_csv(index=False).encode("utf-8")
                    st.download_button("Download Batch Search Result", data=download_csv, file_name="batch_search_result.csv", mime="text/csv")
                else:
                    st.error("None of the uploaded CAS numbers were found.")
        except Exception as e:
            st.error(f"Failed to process the uploaded file: {e}")