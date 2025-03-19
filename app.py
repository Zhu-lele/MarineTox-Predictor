import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# 🌊 设置 Streamlit 页面主题
st.set_page_config(page_title="Chemical Hazard Database", layout="wide")

# ✅ 读取 GitHub 上的 CSV 文件
file_url = "https://raw.githubusercontent.com/Zhu-lele/Chemical-Hazard-Database-for-marine-ecological-risk-assessment/main/Chemical-hazard-database-20250314.csv"

# 🔵 页面样式（UI 美化）
page_style = """
    <style>
        .blue-box {
            background-color: #b3e5fc;
            padding: 20px;
            border-radius: 10px;
            text-align: center;
            font-size: 28px;
            font-weight: bold;
            color: #01579b;
        }
        .title-large {
            font-size: 26px;
            font-weight: bold;
            text-align: center;
            color: #01579b;
            margin-top: 20px;
        }
        .description-small {
            font-size: 16px;
            text-align: center;
            color: #333333;
            margin-bottom: 20px;
        }
        .contact-info {
            font-size: 16px;
            text-align: center;
            color: #666666;
            margin-top: 40px;
        }
        .sidebar-title {
            font-size: 18px;
            font-weight: bold;
            color: #01579b;
        }
    </style>
"""
st.markdown(page_style, unsafe_allow_html=True)

# 📌 **大连理工大学 Logo（调整大小）**
st.sidebar.image("https://raw.githubusercontent.com/Zhu-lele/Chemical-Hazard-Database-for-marine-ecological-risk-assessment/main/dlut_logo.jpg", width=120)

# 🔹 **主页面导航**
page = st.sidebar.radio("📌 Navigation", ["Home", "Data Preview", "Data Filters"])

# ============================== 1️⃣ HOME 页面 ==============================
if page == "Home":
    st.markdown('<div class="blue-box">🌊 Welcome to Chemical Hazard Database 🔬 🌍</div>', unsafe_allow_html=True)

    st.markdown("""
        <div class="title-large">Deep learning model for predicting marine ecotoxicity</div>
    """, unsafe_allow_html=True)

    st.image("https://raw.githubusercontent.com/Zhu-lele/Chemical-Hazard-Database-for-marine-ecological-risk-assessment/main/model_diagram.png", use_column_width=True)

    st.markdown("""
        <div style="font-size:20px; text-align:justify;">
           A multi-task deep-learning model based on <b>molecular graph and exposure duration</b>, enables <b>end-to-end prediction of chemical toxicity</b> for 18 marine organisms spanning five phyla.
        </div>
    """, unsafe_allow_html=True)

    # 📌 **联系信息**
    st.markdown("""
        <div class="contact-info">
            If the toxicity data is not in our database, please contact us: 📧 <b>Zhu_lll@163.com</b>
        </div>
    """, unsafe_allow_html=True)

# ============================== 2️⃣ Data Preview 页面 ==============================
elif page == "Data Preview":
    st.markdown('<div class="title-large">🔬 Toxicity Data Preview</div>', unsafe_allow_html=True)

    try:
        df = pd.read_csv(file_url)
        st.write("### 📊 Full Dataset")
        st.dataframe(df)  # 显示完整数据
    except Exception as e:
        st.error(f"❌ Failed to load data: {e}")

# ============================== 3️⃣ Data Filters 页面 ==============================
elif page == "Data Filters":
    st.markdown('<div class="title-large">🔍 Search Toxicity Data</div>', unsafe_allow_html=True)

    try:
        df = pd.read_csv(file_url)

        # 🎯 **筛选选项**
        st.sidebar.markdown('<div class="sidebar-title">🔍 Enter Search Criteria</div>', unsafe_allow_html=True)
        
        search_column = st.sidebar.selectbox("Select column to search", ["CAS", "Name", "SMILES"])
        search_value = st.sidebar.text_input(f"Enter {search_column} value")

        # 🎯 **执行筛选**
        if search_value:
            filtered_df = df[df[search_column].astype(str).str.contains(search_value, case=False, na=False)]
            st.write(f"### Filtered Data - {search_column}: {search_value}")
            st.dataframe(filtered_df)

            # 📥 **下载筛选后的数据**
            csv_filtered = filtered_df.to_csv(index=False).encode("utf-8")
            st.download_button("📥 Download Filtered Data (CSV)", data=csv_filtered, file_name="filtered_data.csv", mime="text/csv")
        else:
            st.info("Please enter a value to search.")

    except Exception as e:
        st.error(f"❌ Failed to load data: {e}")
