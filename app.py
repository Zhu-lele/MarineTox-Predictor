import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from io import StringIO
import difflib

# 页面配置
st.set_page_config(page_title="MarineTox Predictor", layout="wide")

# 加载数据
@st.cache_data
def load_data():
    file_url = "https://raw.githubusercontent.com/Zhu-lele/Chemical-Hazard-Database-for-marine-ecological-risk-assessment/main/Chemical-hazard-database-20250314.csv"
    return pd.read_csv(file_url)

df = load_data()

# 页面样式
page_style = """<style> ... （你已有的 style 保留） ... </style>"""
st.markdown(page_style, unsafe_allow_html=True)

# 页面导航
page = st.sidebar.radio("", ["Home", "Data Filters"])

# ========================== HOME 页面 ==========================
if page == "Home":
    st.markdown('<div class="main-title">MarineTox Predictor</div>', unsafe_allow_html=True)
    st.markdown('<div class="description-box">MarineTox Predictor enables end-to-end toxicity predictions...</div>', unsafe_allow_html=True)
    st.image("https://raw.githubusercontent.com/Zhu-lele/Chemical-Hazard-Database-for-marine-ecological-risk-assessment/main/model_diagram.jpg", use_container_width=True)
    st.markdown("""<div class="contact-box">School of Environmental Science and Technology, Dalian University of Technology... </div>""", unsafe_allow_html=True)

# ========================== DATA FILTERS 页面 ==========================
elif page == "Data Filters":
    st.markdown('<div class="title-large">Search or Upload CAS for Batch Toxicity Data</div>', unsafe_allow_html=True)

    # ---- 用户输入查询 ----
    st.markdown("### 🔍 单个化学品名称或 CAS 查询（支持模糊匹配）")
    user_input = st.text_input("请输入化学品名称或 CAS 编号：")

    if user_input:
        suggestions_name = difflib.get_close_matches(user_input, df['Name'].dropna().astype(str), n=5, cutoff=0.3)
        suggestions_cas = difflib.get_close_matches(user_input, df['CAS'].dropna().astype(str), n=5, cutoff=0.3)
        suggestions = list(dict.fromkeys(suggestions_name + suggestions_cas))  # 去重合并

        if suggestions:
            selected = st.selectbox("是否指以下化学品之一？", suggestions)
            match_df = df[(df['Name'].astype(str) == selected) | (df['CAS'].astype(str) == selected)]

            if not match_df.empty:
                st.success(f"找到化学品：{selected}")
                st.dataframe(match_df, height=400)

                # ---- 毒性图谱展示 ----
                tox_cols = [col for col in match_df.columns if "LC50" in col or "EC50" in col or "NOEC" in col]
                tox_data = match_df[tox_cols].T
                tox_data.columns = ['Toxicity']

                st.markdown("#### 📊 多物种毒性图谱")
                fig, ax = plt.subplots(figsize=(10, 5))
                tox_data.plot(kind='bar', ax=ax, legend=False)
                ax.set_ylabel("Toxicity (log µg/L)")
                ax.set_xlabel("Species")
                ax.tick_params(axis='x', rotation=45)
                st.pyplot(fig)

        else:
            st.warning("未找到相似化学品，请检查拼写。")

    # ---- 批量查找（保留原功能）----
    st.markdown("### 📥 批量上传 CAS 查询")

    cas_template = pd.DataFrame({"CAS": ["50-00-0", "75-07-0", "108-88-3"]})
    st.download_button("📄 下载 CAS 模板", data=cas_template.to_csv(index=False).encode("utf-8"),
                       file_name="CAS_batch_template.csv", mime="text/csv")

    uploaded_file = st.file_uploader("请上传包含 'CAS' 列的 CSV 文件", type=["csv"])
    if uploaded_file:
        try:
            content = pd.read_csv(uploaded_file)
            if "CAS" not in content.columns:
                st.error("CSV 中缺少 'CAS' 列")
            else:
                cas_list = content["CAS"].dropna().astype(str).str.strip().unique().tolist()
                matched_df = df[df["CAS"].astype(str).isin(cas_list)]

                if not matched_df.empty:
                    st.write("匹配结果：")
                    st.dataframe(matched_df, height=400)

                    unmatched = sorted(set(cas_list) - set(matched_df["CAS"].astype(str)))
                    if unmatched:
                        st.warning("未匹配到以下 CAS：")
                        st.code(", ".join(unmatched))

                    download_csv = matched_df.to_csv(index=False).encode("utf-8")
                    st.download_button("⬇ 下载结果", data=download_csv, file_name="batch_result.csv", mime="text/csv")
                else:
                    st.error("未匹配到任何 CAS。")
        except Exception as e:
            st.error(f"处理文件失败：{e}")
