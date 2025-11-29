import os
import streamlit as st
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage

# 環境変数読込
load_dotenv()

# 専門家リスト
EXPERTS = {
    "プログラミング専門家": "あなたは経験豊富なプログラミング専門家です。プログラミングに関する質問に対して、わかりやすく丁寧に回答してください。",
    "医療専門家": "あなたは医療分野の専門家です。健康や医療に関する質問に対して、専門的な知識を持って回答してください。",
    "料理研究家": "あなたはプロの料理研究家です。料理やレシピに関する質問に対して、詳しく丁寧に回答してください。"
}

# LLM送信関数
def get_llm_response(user_input:str, expert_type:str) -> str:
    # LLM設定
    llm = ChatOpenAI(
        model_name="gpt-4o-mini",
        temperature=0.5,
        api_key=os.environ["OPENAI_API_KEY"],
    )
    
    system_message = SystemMessage(content=EXPERTS[expert_type])
    human_message = HumanMessage(content=user_input)
    
    messages = [system_message, human_message]
    result = llm.invoke(messages)
    
    return result.content

# Streamlitアプリのメイン部分
st.title("AI専門家相談アプリ")

st.markdown("""
## アプリの概要
このアプリでは、様々な分野の専門家AIに質問することができます。

## 使い方
1. 下のラジオボタンから相談したい専門家を選択してください
2. テキスト入力フォームに質問を入力してください
3. 「実行」ボタンをクリックすると、選択した専門家からの回答が表示されます
---
""")

# 専門家ラジオボタン
expert_type = st.radio(
    "相談したい専門家を選択してください：",
    list(EXPERTS.keys())
)

# 入力
with st.form(key="question_form"):
    user_input = st.text_input(label="質問を入力してください：")
    exec_button = st.form_submit_button("実行")

# 実行処理
if exec_button:
    if user_input == "":
        st.error("⚠️ 質問を入力してください。")
    else:
        try:
            # 回答を取得
            response = get_llm_response(user_input, expert_type)
            # 表示
            st.success("✅ 回答が生成されました！")
            st.markdown("### 回答：")
            st.markdown(response)
        except Exception as e:
            st.error(f"❌ エラーが発生しました: {str(e)}")
