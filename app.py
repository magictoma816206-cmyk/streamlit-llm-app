import streamlit as st
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain.schema import SystemMessage, HumanMessage

# .envファイルから環境変数を読み込み
load_dotenv()

def get_llm_response(user_input, expert_type):
    """
    ユーザーの入力と専門家の種類を受け取り、LLMからの回答を返す関数
    """
    # LLMのインスタンス化（モデルの設定）
    llm = ChatOpenAI(model_name="gpt-4o-mini", temperature=0.7)

    # ラジオボタンの選択値に応じて、役割を切り替え
    if expert_type == "料理研究家":
        system_content = "あなたはプロの料理研究家です。初心者でも作れる美味しいレシピやコツを教えてください。"
    elif expert_type == "現役エンジニア":
        system_content = "あなたは経験豊富なプログラミング講師です。技術的な質問に対して、初心者にも分かりやすく論理的に回答してください。"
    else:
        system_content = "あなたは親切なアシスタントです。"

    # メッセージのリストを作成
    messages = [
        SystemMessage(content=system_content),
        HumanMessage(content=user_input),
    ]

    # LLMにメッセージを渡して回答を得る
    # ※最新のLangChainでは llm.invoke(messages) を使うのが推奨されています
    response = llm.invoke(messages)
    
    return response.content


#Streamlitの画面表示設定
st.title("専門家AIチャットアプリ")
st.write("このアプリは、選択した専門家があなたの質問に答えてくれるLLMアプリです。")

# 操作方法の明示
st.info("""
**【使い方】**
1. 相談したい専門家の種類をラジオボタンから選んでください。
2. 下の入力フォームに質問したい内容を入力してください。
3. 送信すると、専門家からの回答が表示されます。
""")

# ラジオボタンの設置
expert_choice = st.radio(
    "専門家を選択してください：",
    ("料理研究家", "現役エンジニア")
)

# 入力フォームの設置
user_text = st.text_input("質問を入力してください：")

# 実行ボタン
if st.button("回答を生成"):
    if user_text:
        with st.spinner("回答を生成中..."):
            # 関数の呼び出し
            answer = get_llm_response(user_text, expert_choice)
            
            st.subheader(f"【{expert_choice}からの回答】")
            st.write(answer)
    else:
        st.warning("質問を入力してください。")