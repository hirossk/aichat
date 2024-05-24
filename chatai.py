from flask import Flask,render_template,request, send_file,jsonify
import json
import boto3
from util import getface,getaiface
import os
from langchain_aws import BedrockLLM
from langchain import ConversationChain
from langchain.memory import ConversationBufferMemory
import voice

# LLMの定義
llm = BedrockLLM(
    model_id="anthropic.claude-v2:1",
    region_name='ap-northeast-1'
)
# memory = ConversationBufferMemory(return_messages=True)
conversation = ConversationChain(llm=llm)
#文章解析のエンジンへの接続
comprehend=boto3.client('comprehend', region_name='ap-northeast-1')
   
app = Flask(__name__, static_folder="./static/")
app.register_blueprint(voice.app)

# '/'URLに数値を指定すると呼び出される関数定義
@app.route('/')
def loopmessage():
    # create_talk関数の呼び出し
    # Jinjaテンプレートによる展開が行われる（talksはhtml内で利用される）
    return render_template('talk/chat.html')

# Ajax用コールメソッド
@app.route("/call_ajax", methods = ["POST"])
def callfromajax():
    sentiment_score = None
    aisentiment_score = None
    if request.method == "POST":
        # ここにPythonの処理を書く
        try:
            frommessage = request.form["sendmessage"]
            answer = "こんにちは" # frommessage
            # answer = f"あなたのメッセージは「{frommessage}」"

            # チャットメッセージの理解をする
            # response = comprehend.detect_sentiment(Text=frommessage, LanguageCode='ja')
            # sentiment_score = response['SentimentScore']

            # チャットメッセージのフレーズを取得する
            # keyresponse = comprehend.detect_key_phrases(Text=frommessage, LanguageCode='ja')
            # pprint.pprint(keyresponse)
            
            # 生成AIによるメッセージの返送
            # answer = conversation.predict(input=frommessage)

            # 生成AIの感情を判定
            # airesponse = comprehend.detect_sentiment(Text=answer, LanguageCode='ja')
            # aisentiment_score = airesponse['SentimentScore']

        except Exception as e:
            answer = str(e)
            
        voice.pollytext = answer
        frommessage = frommessage.replace('\n','<br>')
        answer = answer.replace('\n','<br>')
        face = getface(sentiment_score)
        aiface = getaiface(aisentiment_score)

        dict = {"answer": answer, # 回答
                "message": frommessage,# 元のメッセージ
                "face": face, # 送信メッセージの気分
                "aiface": aiface}  # aiメッセージの気分
    return json.dumps(dict, ensure_ascii=False)             

if __name__=='__main__':
    app.secret_key = os.urandom(24)
    app.debug = True
    app.run(host="0.0.0.0",port=80,debug=True)