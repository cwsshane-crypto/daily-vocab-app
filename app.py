import streamlit as st
import random
import pandas as pd
from datetime import datetime
import os
import json

# --- 強力讀取函數：不管檔案躲在哪裡都把它抓出來 ---
def load_vocab():
    # 列出所有可能被你誤建的路徑
    possible_paths = [
        os.path.join('data', 'words.json'),
        os.path.join('data', 'data', 'words.json'),
        os.path.join('data', 'data', 'data', 'words.json'),
        'words.json'
    ]
    
    for path in possible_paths:
        if os.path.exists(path):
            try:
                with open(path, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except:
                continue
                
    # 如果真的都找不到，才顯示這個
    return {"P3": [{"word": "檔案位置錯誤", "hint": "請確認 GitHub 上的 words.json 放在 data 資料夾內"}], "P6": []}

# --- 儲存紀錄 ---
def save_record(level, word, sentence):
    file_name = 'sentence_records.csv'
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    new_entry = {'時間': [now], '年級': [level], '生字': [word], '學生的造句': [sentence]}
    df_new = pd.DataFrame(new_entry)
    if not os.path.isfile(file_name):
        df_new.to_csv(file_name, index=False, encoding='utf-8-sig')
    else:
        df_new.to_csv(file_name, mode='a', index=False, header=False, encoding='utf-8-sig')

# --- 介面開始 ---
st.set_page_config(page_title="仔仔造句記錄本", page_icon="🍎")
st.title("🍎 仔仔每日造句記錄本")

vocab_db = load_vocab()
level = st.selectbox("請選擇年級：", list(vocab_db.keys()))

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
        if 'current_word' in st.session_state:
            st.session_state.current_word = random.choice(vocab_db[level])
        st.rerun()

st.divider()
if st.checkbox("查看歷史記錄"):
    if os.path.isfile('sentence_records.csv'):
        st.dataframe(pd.read_csv('sentence_records.csv').tail(10))
    else:
        st.write("目前還沒有紀錄喔！")
