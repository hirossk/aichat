from flask import Flask,render_template,request, send_file,jsonify
import json
import boto3
from util import getface,getaiface
import os
from langchain_aws import BedrockLLM,ChatBedrock
from langchain.chains import ConversationChain
from langchain.memory import ConversationBufferMemory
import voice

# LLMの定義 Anthropic(アンスロピック)の生成AI Claude（クロード）を利用します
# llm = BedrockLLM(model_id="anthropic.claude-v2:1", region_name='ap-northeast-1') #古いバージョン
llm = ChatBedrock(model_id="anthropic.claude-3-sonnet-20240229-v1:0",model_kwargs={"max_tokens": 1000,})

# 記憶領域の拡大に使います
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
    # Jinjaテンプレートによる展開が行われる
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
            # answer = f"あなたのメッセージは「{frommessage}」"
        
            # 生成AIによるメッセージの返送
            # answer = conversation.predict(input=frommessage)

            # 生成AIの感情を判定
            # airesponse = comprehend.detect_sentiment(Text=answer, LanguageCode='ja')
            # aisentiment_score = airesponse['SentimentScore']

        except Exception as e:
            answer = str(e)
            
        # 生成AIの感情を読み取る
        voice.pollytext = answer
        answer = answer.replace('\n','<br>')
        aiface = getaiface(aisentiment_score)

        dict = {"answer": answer, # 回答
                "aiface": aiface}  # aiメッセージの気分
    return json.dumps(dict, ensure_ascii=False)

if __name__=='__main__':
    app.secret_key = os.urandom(24)
    app.debug = True
    app.run(host="0.0.0.0",port=80,debug=True)
