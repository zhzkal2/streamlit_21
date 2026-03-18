import os
import streamlit as st
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate

load_dotenv()

if "OPENAI_API_KEY" in st.secrets:
    os.environ["OPENAI_API_KEY"] = st.secrets["OPENAI_API_KEY"]

# --- 専門家ごとのシステムメッセージ ---
EXPERT_PROMPTS = {
    "日本料理の専門家": "あなたは日本料理の専門家です。与えられた食材を使って作れる日本料理を提案してください。レシピの簡単な手順も含めてください。",
    "韓国料理の専門家": "あなたは韓国料理の専門家です。与えられた食材を使って作れる韓国料理を提案してください。レシピの簡単な手順も含めてください。",
    "洋食の専門家": "あなたは洋食の専門家です。与えられた食材を使って作れる洋食を提案してください。レシピの簡単な手順も含めてください。",
}


def get_recipe_suggestion(ingredients, expert):
    """食材と専門家の選択に基づいてLLMから料理提案を取得する"""
    llm = ChatOpenAI(model_name="gpt-4o-mini", temperature=0.7)
    prompt = ChatPromptTemplate.from_messages([
        ("system", EXPERT_PROMPTS[expert]),
        ("human", "冷蔵庫にある食材: {ingredients}\nこの食材で作れる料理を提案してください。"),
    ])
    chain = prompt | llm
    response = chain.invoke({"ingredients": ingredients})
    return response.content


# --- Streamlit UI ---
st.title("🍳 冷蔵庫の食材でレシピ提案")

st.markdown("""
### アプリ概要
冷蔵庫にある食材を入力し、料理の専門家を選ぶと、その食材で作れる料理を提案します。

### 操作方法
1. 下の入力欄に冷蔵庫の食材を入力してください（例: 鶏肉、玉ねぎ、卵、醤油）
2. ラジオボタンで専門家を選択してください
3.「提案を見る」ボタンを押してください
""")

ingredients = st.text_input("冷蔵庫の食材を入力してください（カンマ区切り）", placeholder="例: 鶏肉、玉ねぎ、卵、醤油")

expert = st.radio("専門家を選んでください", list(EXPERT_PROMPTS.keys()))

if st.button("提案を見る"):
    if not ingredients:
        st.warning("食材を入力してください。")
    else:
        with st.spinner("料理を考えています..."):
            result = get_recipe_suggestion(ingredients, expert)
        st.markdown("---")
        st.markdown(f"### 🧑‍🍳 {expert}の提案")
        st.markdown(result)

