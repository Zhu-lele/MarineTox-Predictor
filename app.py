import streamlit as st
import pandas as pd

# 🌊 设置 Streamlit 页面主题
st.set_page_config(page_title="Chemical Hazard Database", layout="wide")

# ✅ 读取 GitHub 上的 CSV 文件
file_url = "https://raw.githubusercontent.com/Zhu-lele/Chemical-Hazard-Database-for-marine-ecological-risk-assessment/main/Chemical-hazard-database-20250314.csv"

# 🔵 页面样式（UI 美化）
page_style = """
    <style>
        .nav-button {
            background-color: #01579b;
            color: white;
            padding: 15px;
            font-size: 22px;
            font-weight: bold;
            text-align: center;
            border-radius: 10px;
            margin-bottom: 20px;
        }
        .title-large {
            font-size: 26px;
            font-weight: bold;
            text-align: center;
            color: white;
            background-color: #01579b;
            padding: 15px;
            border-radius: 10px;
            margin-bottom: 20px;
        }
        .description-box {
            font-size: 20px;
            text-align: justify;
            background-color: #b3e5fc;
            padding: 15px;
            border-radius: 10px;
            color: #01579b;
            margin-bottom: 30px;
        }
        .contact-info {
            font-size: 16px;
            text-align: center;
            color: #ffffff;
            background-color: #01579b;
            padding: 10px;
            border-radius: 10px;
            margin-top: 30px;
        }
        .sidebar-title {
            font-size: 18px;
            font-weight: bold;
            color: #01579b;
        }
    </style>
"""
st.markdown(page_style, unsafe_allow_html=True)

# 🔹 **主页面导航**
page = st.sidebar.radio("📌 Navigation", ["Home", "Data Preview", "Data Filters"])

# ============================== 1️⃣ HOME 页面 ==============================
if page == "Home":
    st.markdown('<div class="title-large">🌊 Welcome to Chemical Hazard Database 🔬 🌍</div>', unsafe_allow_html=True)

    st.markdown('<div class="description-box">Deep learning model for predicting marine ecotoxicity.</div>', unsafe_allow_html=True)

    st.image("https://raw.githubusercontent.com/Zhu-lele/Chemical-Hazard-Database-for-marine-ecological-risk-assessment/main/model_diagram.png", use_column_width=True)

    st.markdown('<div class="description-box">A multi-task deep-learning model based on <b>molecular graph and exposure duration</b>, enabling <b>end-to-end prediction of chemical toxicity</b> for 18 marine organisms spanning five phyla.</div>', unsafe_allow_html=True)

    # 📌 **数据库开发信息**
    st.markdown('<div class="contact-info"><b>本数据库由大连理工大学环境学院发展</b></div>', unsafe_allow_html=True)

    # 📌 **大连理工大学 Logo**
    st.image("https://raw.githubusercontent.com/Zhu-lele/Chemical-Hazard-Database-for-marine-ecological-risk-assessment/main/dlut_logo.jpg", width=150)

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
        st.dataframe(df, height=600)  # 数据表加高
    except Exception as e:
        st.error(f"❌ Failed to load data: {e}")

# ============================== 3️⃣ Data Filters 页面 ==============================
elif page == "Data Filters":
    st.markdown('<div class="title-large">🔍 Search Toxicity Data</div>', unsafe_allow_html=True)

    try:
        df = pd.read_csv(file_url)

        # 🎯 **筛选选项**
        st.sidebar.markdown('<div class="sidebar-title">🔍 Enter Search Criteria</div>', unsafe_allow_html=True)

        # 用户可以手动输入或者下拉选择
        search_column = st.sidebar.selectbox("Select column to search", ["CAS", "Name", "SMILES"])
        search_value = st.sidebar.text_input(f"Enter {search_column} value")
        dropdown_value = st.sidebar.selectbox(f"Or select from {search_column}", [""] + list(df[search_column].dropna().unique()))

        # 选择用户输入或下拉值
        selected_value = search_value if search_value else dropdown_value

        # 🎯 **执行筛选**
        if selected_value:
            filtered_df = df[df[search_column].astype(str).str.contains(selected_value, case=False, na=False)]
            st.write(f"### Filtered Data - {search_column}: {selected_value}")
            st.dataframe(filtered_df, height=600)

            # 📥 **下载筛选后的数据**
            csv_filtered = filtered_df.to_csv(index=False).encode("utf-8")
            st.download_button("📥 Download Filtered Data (CSV)", data=csv_filtered, file_name="filtered_data.csv", mime="text/csv")
        else:
            st.info("Please enter a value or select from dropdown.")

    except Exception as e:
        st.error(f"❌ Failed to load data: {e}")
