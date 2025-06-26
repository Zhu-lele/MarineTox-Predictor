import streamlit as st
import pandas as pd
import os

# ---------------- 页面基础配置 ----------------
st.set_page_config(page_title="MarineTox Chatbot", layout="centered")

# ---------------- 数据加载 ----------------
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

# ---------------- 页面美化 ----------------
st.markdown("""
<style>
/* 固定聊天框在页面底部 */
.chat-container {
    width: 100%;
    height: 400px;
    max-height: 400px;
    overflow-y: scroll;
    margin: 0 auto;
    background-color: #f5f5f5;
    border-radius: 10px;
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
    padding: 10px;
    position: relative;
}

/* 用户消息气泡样式 */
.chat-bubble-user {
    background-color: #e3f2fd;
    padding: 10px;
    border-radius: 10px;
    margin-bottom: 10px;
    max-width: 80%;
    margin-left: auto;
}

/* 系统回复气泡样式 */
.chat-bubble-bot {
    background-color: #01579b;
    color: white;
    padding: 10px;
    border-radius: 10px;
    margin-bottom: 10px;
    max-width: 80%;
    margin-right: auto;
}

/* 输入框和发送按钮样式 */
input {
    width: 90%;
    padding: 10px;
    margin-bottom: 10px;
    border-radius: 5px;
    border: 1px solid #ccc;
}

/* 发送按钮样式 */
button {
    background-color: #01579b;
    color: white;
    border: none;
    padding: 10px 20px;
    border-radius: 5px;
}

/* 固定输入框和发送按钮位置在页面底部 */
.stTextInput, .stButton {
    position: fixed;
    bottom: 20px;
    width: 100%;
    padding: 10px;
    box-sizing: border-box;
    background-color: #fff;
}
</style>
""", unsafe_allow_html=True)

# ---------------- 模糊匹配关键词提取 ----------------
def extract_chemical_name(text):
    """模糊匹配：输入中模糊包含化学品名称即返回"""
    clean_text = text.lower().strip()
    for name in df["Chemical name"].dropna().astype(str).tolist():
        if name.lower().strip() in clean_text:
            return name
    return None

# ---------------- 页面主体 ----------------
st.title("💬 MarineTox Predictor - Chatbot风格智能数据库")
st.info("请用自然语言提问，例如：'请告诉我 amyl nitrite 的毒性数据'，系统会自动返回信息。")

# ---------------- 展示历史对话 ----------------
st.markdown('<div class="chat-container">', unsafe_allow_html=True)
for chat in st.session_state.chat_history:
    if chat["role"] == "user":
        st.markdown(f'<div class="chat-bubble-user">🧑 {chat["content"]}</div>', unsafe_allow_html=True)
    else:
        st.markdown(f'<div class="chat-bubble-bot">🤖 {chat["content"]}</div>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# ---------------- 用户输入区 ----------------
with st.form("chat_form"):
    user_input = st.text_input("请输入您的问题:")
    submitted = st.form_submit_button("发送")

# ---------------- 处理输入 ----------------
if submitted and user_input:
    st.session_state.chat_history.append({"role": "user", "content": user_input})
    
    chem_name = extract_chemical_name(user_input)
    
    if chem_name:
        row = df[df["Chemical name"].astype(str).str.lower() == chem_name.lower()].iloc[0]
        
        reply = f"""
**Chemical Name:** {row['Chemical name']}  
**SMILES:** {row['SMILES']}  
**Molecular Formula:** {row['Molecular formula']}  

**🔸 LC50 / EC50 Values:**  
"""
        for col in df.columns[3:23]:
            reply += f"{col}: {row[col]}  \n"
        
        reply += "\n**🔸 NOEC Values:**\n"
        for col in df.columns[23:27]:
            reply += f"{col}: {row[col]}  \n"
        
        reply += "\n**🔸 SSD Curve:**\n"
        for col in df.columns[27:32]:
            reply += f"{col}: {row[col]}  \n"

        st.session_state.chat_history.append({"role": "bot", "content": reply})
    else:
        st.session_state.chat_history.append({"role": "bot", "content": "很抱歉，未能识别出您提问中的化学品名称，请确保输入正确的化学品名称。"})

    # 页面刷新以显示新对话
    st.experimental_rerun()
