from flask import Flask,render_template,request,session
import json
import boto3
from util import getface, getaiface, predict_message
import os
import voice
from langchain_community.chat_message_histories import ChatMessageHistory
import re
from uuid import uuid4
import glob
from PyPDF2 import PdfReader

# PDFファイルを読み込んで抽象化する関数
def load_pdf_knowledge():
    pdf_files = glob.glob("files/*.pdf")
    knowledge = ""
    for pdf_path in pdf_files:
        try:
            reader = PdfReader(pdf_path)
            text = ""
            for page in reader.pages:
                text += page.extract_text()
            knowledge += f"\n\n[{os.path.basename(pdf_path)}の内容]\n{text}\n"
        except Exception as e:
            print(f"PDF読み込みエラー ({pdf_path}): {e}")
    return knowledge

# 起動時にPDFを読み込み
pdf_knowledge = load_pdf_knowledge()

# セッションに一意のIDを割り当てて、チャット履歴を保持
session_id = str(uuid4())
history = ChatMessageHistory()


# Bedrockクライアントの初期化
bedrock_runtime = boto3.client(
    service_name='bedrock-runtime',
    region_name='ap-northeast-1'  # 利用可能なリージョンに変更してください
)


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
    thinking = ""
    if request.method == "POST":
        answer = "こんにちは"
        try:
            # 生成AIにメッセージを投げて、返信を受け取る
            # result = predict_message(frommessage, session)

            # 推論プロセスと回答を取得
            # thinking = result.get("thinking", "")
            # answer = result.get("answer", "")

            # コードブロック判定（例: ```で囲まれているか）
            is_code = bool(re.search(r"```[\s\S]+?```", answer))
        except Exception as e:
            answer = str(e)
            is_code = False
            # 生成AIの感情を判定
            # airesponse = comprehend.detect_sentiment(Text=answer, LanguageCode='ja')
            # aisentiment_score = airesponse['SentimentScore']

        voice.pollytext = answer
        answer_html = answer.replace('\n','<br>') if not is_code else answer
        thinking_html = thinking.replace('\n','<br>') if thinking else ""
        aiface = getaiface(aisentiment_score)

        dict = {
            "answer": answer_html,
            "aiface": aiface,
            "is_code": is_code,
            "thinking": thinking_html
        }
    return json.dumps(dict, ensure_ascii=False)

if __name__=='__main__':
    app.secret_key = os.urandom(24)
    app.debug = True
    app.run(host="0.0.0.0",port=80,debug=True)
