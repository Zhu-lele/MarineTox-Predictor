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
            font-size: 30px;
            font-weight: bold;
            text-align: center;
            color: #01579b; /* 深蓝色字体 */
            margin-bottom: 40px;
        }
        /* 页面描述 */
        .description-box {
            font-size: 22px;
            text-align: center;
            color: #01579b;
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
            background-color: #01579b !important;
        }
        /* 侧边栏文本字体加大 2 倍，变白色 */
        section[data-testid="stSidebar"] * {
            font-size: 24px !important;
            color: white !important;
        }
        /* 修改侧边栏输入框、下拉框的字体颜色为深蓝色 */
        section[data-testid="stSidebar"] input, 
        section[data-testid="stSidebar"] select,
        section[data-testid="stSidebar"] label, 
        section[data-testid="stSidebar"] div[data-testid="stSelectboxLabel"] {
            color: #01579b !important; /* 深蓝色 */
            font-weight: bold !important; /* 让文字更醒目 */
        }
        /* 修正下拉菜单展开后的字体颜色 */
        section[data-testid="stSidebar"] div[data-baseweb="select"] div {
            color: #01579b !important; /* 深蓝色 */
            font-weight: bold !important;
        }
        /* 增加输入框和下拉框的高度 */
        section[data-testid="stSidebar"] input, 
        section[data-testid="stSidebar"] select {
            height: 50px !important;  /* 你可以改成 60px, 70px 试试看 */
            font-size: 20px !important; /* 让字体也变大一些 */
            padding: 10px !important; /* 增加内部填充，使文本不贴边 */
        }
    </style>
"""
st.markdown(page_style, unsafe_allow_html=True)

# 🔹 **主页面导航**
page = st.sidebar.radio("", ["Home", "Data Preview", "Data Filters"])

# ============================== 3️⃣ Data Filters 页面 ==============================
if page == "Data Filters":
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
