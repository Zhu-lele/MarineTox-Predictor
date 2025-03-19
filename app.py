import streamlit as st
import pandas as pd

# 🌊 设置 Streamlit 页面主题
st.set_page_config(page_title="Chemical Hazard Database", layout="wide")

# ✅ 读取 GitHub 上的 CSV 文件
file_url = "https://raw.githubusercontent.com/Zhu-lele/Chemical-Hazard-Database-for-marine-ecological-risk-assessment/main/Chemical-hazard-database-20250314.csv"

# 🔵 页面样式（UI 美化）
page_style = """
    <style>
        /* 顶部标题栏 */
        .title-large {
            font-size: 26px;
            font-weight: bold;
            text-align: center;
            color: #01579b; /* 深蓝色字体 */
            margin-bottom: 40px;
        }
        /* 页面描述 */
        .description-box {
            font-size: 22px;
            text-align: center;
            color: #01579b; /* 深蓝色字体 */
            margin-bottom: 30px;
        }
        /* 数据库和联系信息合并框 */
        .contact-box {
            font-size: 16px;
            text-align: center;
            color: #ffffff;
            background-color: #01579b;
            padding: 15px;
            border-radius: 10px;
            margin-top: 30px;
        }
        /* 侧边栏背景颜色 */
        section[data-testid="stSidebar"] {
            background-color: #01579b !important; /* 蓝色背景 */
        }
        /* 侧边栏文本字体加大 2 倍，变白色 */
        section[data-testid="stSidebar"] * {
            font-size: 24px !important;  /* 2 倍字体大小 */
            color: white !important;  /* 文字变白 */
        }
    </style>
"""
st.markdown(page_style, unsafe_allow_html=True)

# 🔹 **主页面导航**
page = st.sidebar.radio( ["Home", "Data Preview", "Data Filters"])

# ============================== 1️⃣ HOME 页面 ==============================
if page == "Home":
    st.markdown('<div class="title-large">🌊 Welcome to ChemMarineTox 🌍</div>', unsafe_allow_html=True)

    # 透明背景，深蓝色字体，居中
    st.markdown('<div class="description-box">Multi-task Deep learning model for predicting marine ecotoxicity.</div>', unsafe_allow_html=True)

    st.image("https://raw.githubusercontent.com/Zhu-lele/Chemical-Hazard-Database-for-marine-ecological-risk-assessment/main/model_diagram.png", use_column_width=True)

    # 📌 **数据库开发信息 + 联系方式**
    st.markdown("""
        <div class="contact-box">
            The ChemMarineTox was developed by Key Laboratory of Industrial Ecology and Environmental Engineering (MOE), Dalian Key Laboratory on Chemicals Risk Control and Pollution Prevention Technology, School of Environmental Science and Technology, Dalian University of Technology<br>
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
