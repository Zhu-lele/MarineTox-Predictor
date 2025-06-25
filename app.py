import streamlit as st
import pandas as pd
import re
import os

# ---------------- 页面基础配置 ----------------
st.set_page_config(page_title="MarineTox Chatbot", layout="centered")

# ---------------- 加载本地数据 ----------------
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

# ---------------- 初始化对话记录 ----------------
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# ---------------- 样式美化 ----------------
st.markdown("""
<style>
.chat-bubble-user {
    background-color: #e3f2fd;
    padding: 10px;
    border-radius: 10px;
    margin-bottom: 10px;
}
.chat-bubble-bot {
    background-color: #01579b;
    color: white;
    padding: 10px;
    border-radius: 10px;
    margin-bottom: 10px;
}
</style>
""", unsafe_allow_html=True)

# ---------------- 关键词提取函数 ----------------
def extract_chemical_name(text):
    """尝试提取化学品名称"""
    for name in df["Chemical name"].dropna().astype(str).tolist():
        if name.lower() in text.lower():
            return name
    return None

# ---------------- 聊天对话展示 ----------------
st.title("💬 MarineTox Predictor - Chatbot风格智能数据库")

st.info("请您用自然语言提问，例如：'请告诉我 amyl nitrite 的毒性数据'，系统会自动返回信息。")

for chat in st.session_state.chat_history:
    if chat["role"] == "user":
        st.markdown(f'<div class="chat-bubble-user">🧑 {chat["content"]}</div>', unsafe_allow_html=True)
    else:
        st.markdown(f'<div class="chat-bubble-bot">🤖 {chat["content"]}</div>', unsafe_allow_html=True)

# ---------------- 用户输入区 ----------------
user_input = st.text_input("请输入您的问题:")

if st.button("发送") and user_input:
    st.session_state.chat_history.append({"role": "user", "content": user_input})
    
    chem_name = extract_chemical_name(user_input)
    
    if chem_name:
        row = df[df["Chemical name"].astype(str).str.lower() == chem_name.lower()].iloc[0]
        
        reply = f"""
<b>Chemical Name:</b> {row['Chemical name']}  
<b>SMILES:</b> {row['SMILES']}  
<b>Molecular Formula:</b> {row['Molecular formula']}  

<b>🔸 LC50 / EC50 Values:</b>  
"""
        for col in df.columns[3:23]:
            reply += f"{col}: {row[col]}  \n"
        
        reply += "\n<b>🔸 NOEC Values:</b>\n"
        for col in df.columns[23:27]:
            reply += f"{col}: {row[col]}  \n"
        
        reply += "\n<b>🔸 SSD Curve:</b>\n"
        for col in df.columns[27:32]:
            reply += f"{col}: {row[col]}  \n"

        st.session_state.chat_history.append({"role": "bot", "content": reply})
    else:
        st.session_state.chat_history.append({"role": "bot", "content": "很抱歉，未能识别出您提问中的化学品名称，请确保输入正确的化学品名称。"})
    
    st.experimental_rerun()
