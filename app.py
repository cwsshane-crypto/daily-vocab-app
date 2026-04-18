import streamlit as st
import random
import pandas as pd
from datetime import datetime
import os
import json

# --- 1. 從 Folder 讀取字庫的函數 ---
def load_vocab():
    # 嘗試三個可能出現檔案嘅路徑
    possible_paths = [
        os.path.join('data', 'words.json'),       # 標準路徑
        'words.json',                             # 萬一你放咗喺最外面
        os.path.join('data', 'data', 'words.json') # 萬一資料夾重疊咗
    ]
    
    for path in possible_paths:
        if os.path.exists(path):
            with open(path, 'r', encoding='utf-8') as f:
                return json.load(f)
    
    # 如果全部都搵唔到，先會出「檔案遺失」
    return {"P3": [{"word": "檔案遺失", "hint": "請檢查 GitHub 路徑"}], "P6": []}

# --- 2. 儲存紀錄的函數 ---
def save_record(level, word, sentence):
    file_name = 'sentence_records.csv'
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    new_entry = {'時間': [now], '年級': [level], '生字': [word], '學生的造句': [sentence]}
    df_new = pd.DataFrame(new_entry)
    
    if not os.path.isfile(file_name):
        df_new.to_csv(file_name, index=False, encoding='utf-8-sig')
    else:
        df_new.to_csv(file_name, mode='a', index=False, header=False, encoding='utf-8-sig')

# --- Streamlit 介面 ---
st.set_page_config(page_title="造句記錄本", page_icon="✍️")
st.title("🍎 仔仔每日造句記錄本")

# 讀取字庫
vocab_db = load_vocab()

level = st.selectbox("請選擇年級：", list(vocab_db.keys()))

# 初始化題目
if 'current_word' not in st.session_state or st.session_state.get('last_level') != level:
    st.session_state.current_word = random.choice(vocab_db[level])
    st.session_state.last_level = level

word_info = st.session_state.current_word

st.info(f"### 今日生詞：**{word_info['word']}**")
st.write(f"💡 **意思提示：** {word_info['hint']}")

user_input = st.text_area("請在這裡輸入你的造句：", height=150)

col1, col2 = st.columns(2)
with col1:
    if st.button("✅ 提交並儲存記錄"):
        if user_input.strip():
            save_record(level, word_info['word'], user_input)
            st.success("紀錄成功！")
            st.balloons()
        else:
            st.warning("請先輸入句子喔！")

with col2:
    if st.button("🔄 換一個字"):
        st.session_state.current_word = random.choice(vocab_db[level])
        st.rerun()

st.divider()
if st.checkbox("查看歷史記錄"):
    if os.path.isfile('sentence_records.csv'):
        st.dataframe(pd.read_csv('sentence_records.csv').tail(10))
