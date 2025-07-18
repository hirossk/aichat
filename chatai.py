from flask import Flask,render_template,request, send_file,jsonify
import json
import boto3
from util import getface,getaiface
import os
from langchain_aws import BedrockLLM,ChatBedrock
import voice
from langchain_core.runnables import RunnableWithMessageHistory
from langchain_community.chat_message_histories import ChatMessageHistory
import re
from uuid import uuid4
# セッションに一意のIDを割り当てて、チャット履歴を保持
session_id = str(uuid4())
history = ChatMessageHistory()
# LLMの定義 Anthropic(アンスロピック)の生成AI Claude（クロード）を利用します
llm = ChatBedrock(model_id="anthropic.claude-3-5-sonnet-20240620-v1:0",model_kwargs={"max_tokens": 1000,})
conversation = RunnableWithMessageHistory( runnable=llm, get_session_history=lambda session_id: history,)
def predict_message(message):
    return conversation.invoke( {"input": message}, config={"configurable": {"session_id": "default"}}
    ).content

#文章解析のエンジンへの接続
comprehend=boto3.client('comprehend', region_name='ap-northeast-1')

app = Flask(__name__, static_folder="./static/")
app.register_blueprint(voice.app)

@app.route('/') # トップページ
def index():
    return render_template('talk/chat.html' ,link="https://www.iijmio.jp/campaign/")

# Ajax-Callメソッド
@app.route("/call_ajax", methods = ["POST"])
def callfromajax():
    global frommessage
    sentiment_score = None
    if request.method == "POST":
        try:
            frommessage = request.form["sendmessage"] # 入力したメッセージ

            # チャットメッセージの理解をする
            # response = comprehend.detect_sentiment(Text=frommessage, LanguageCode='ja')
            # sentiment_score = response['SentimentScore']

        except Exception as e:
            answer = str(e)
            
        frommessage = frommessage.replace('\n','<br>')
        face = getface(sentiment_score)

        dict = {"message": frommessage,# 元のメッセージ
                "face": face}  # aiメッセージの気分
        

    return json.dumps(dict, ensure_ascii=False)             

# 生成AI-Callメソッド
@app.route("/response_ai", methods = ["POST"])
def responseai():
    aisentiment_score = None
    if request.method == "POST":
        try:
                        # answerには返信用メッセージが格納されます。
            answer = "こんにちは" # frommessage
            # answer = predict_message(frommessage) # 生成AIにメッセージを投げて、返信を受け取る
            # コードブロック判定（例: ```で囲まれているか）
            is_code = bool(re.search(r"```[\s\S]+?```", answer))
        except Exception as e:
            answer = str(e)
            # 生成AIの感情を判定
            # airesponse = comprehend.detect_sentiment(Text=answer, LanguageCode='ja')
            # aisentiment_score = airesponse['SentimentScore']
        is_code = bool(re.search(r"```[\s\S]+?```", answer))
        voice.pollytext = answer
        answer_html = answer.replace('\n','<br>') if not is_code else answer
        aiface = getaiface(aisentiment_score)

        dict = {
            "answer": answer_html,
            "aiface": aiface,
            "is_code": is_code
        }
    return json.dumps(dict, ensure_ascii=False)

if __name__=='__main__':
    app.secret_key = os.urandom(24)
    app.debug = True
    app.run(host="0.0.0.0",port=80,debug=True)
