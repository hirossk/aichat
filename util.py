import json
import boto3
import os
import glob
from uuid import uuid4
from PyPDF2 import PdfReader
from langchain_community.chat_message_histories import ChatMessageHistory


def getface(sentiment_score):
    if sentiment_score is None:
        return "😊";
    posi,nega,neu,mix = getsentimentscore(sentiment_score)
    # 感情を読み取ってアイコンを変更する
    printout("You:",posi,nega,neu,mix)
    # if posi > 90:
    #     return ""
    return "😶"

def getaiface(sentiment_score):
    if sentiment_score is None:
        return None;
    posi,nega,neu,mix = getsentimentscore(sentiment_score)
    # 感情を読み取ってアイコンを変更する
    printout("AI:",posi,nega,neu,mix)
    # if posi > 80:
    #     return ""
    return ""

def getsentimentscore(sentiment_score):
    posi = sentiment_score['Positive']
    nega = sentiment_score['Negative']
    neu = sentiment_score['Neutral']
    mix = sentiment_score['Mixed']
    return posi,nega,neu,mix

def printout(w,posi,nega,neu,mix):
    print(w)
    print("  前向きさ(Positive) = {:.2f}".format(posi))
    print("  後ろ向き(Negative) = {:.2f}".format(nega))
    print("  中立的(Neutral) = {:.2f}".format(neu))
    print("  入り組んだ気持ち(Mixed) = {:.2f}".format(mix))

# Simple exception class
class InvalidUsage(Exception):
    status_code = 400

    def __init__(self, message, status_code=None, payload=None):
        Exception.__init__(self)
        self.message = message
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload

    def to_dict(self):
        rv = dict(self.payload or ())
        rv['message'] = self.message
        return rv


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


def predict_message(message, session):
    # 履歴をセッションから取得
    if 'chat_history' not in session:
        session['chat_history'] = []
    messages = session['chat_history']

    # systemプロンプトをbodyのsystemフィールドで管理
    system_prompt = None
    if pdf_knowledge:
        system_prompt = (
            "あなたは次のルールを絶対に守ってください。\n"
            "・『サイバーズ』に関する質問のときだけ、以下の知識を参考にして答えること。\n"
            "・それ以外の日常会話や雑談では、絶対にこの知識を使わず、通常通り会話すること。\n"
            "違反しないでください。\n"
            f"{pdf_knowledge}"
        )

    # messagesからrole:systemを除外
    messages = [m for m in messages if m.get('role') != 'system']

    # 今回のユーザー発話を履歴に追加
    messages.append({"role": "user", "content": message})

    # Claude v4.5 API仕様に合わせてbodyを作成
    request_body = {
        "messages": messages,
        "max_tokens": 4096,
        "temperature": 0.7,
        "anthropic_version": "bedrock-2023-05-31"
    }
    if system_prompt:
        request_body["system"] = system_prompt
    response = bedrock_runtime.invoke_model(
        modelId='jp.anthropic.claude-sonnet-4-5-20250929-v1:0',
        body=json.dumps(request_body)
    )
    response_body = response["body"].read().decode()
    response_json = json.loads(response_body)
    # Claude v4.5 Messages APIの返答仕様に応じてanswerを取得
    answer_content = ""
    if "content" in response_json:
        content = response_json["content"]
        if isinstance(content, list):
            texts = []
            for c in content:
                if isinstance(c, dict) and c.get('type') == 'text' and 'text' in c:
                    texts.append(c['text'])
                else:
                    texts.append(str(c))
            answer_content = "".join(texts)
        else:
            answer_content = str(content)
    elif "choices" in response_json and response_json["choices"]:
        answer_content = response_json["choices"][0].get("message", {}).get("content", "")
    thinking_content = response_json.get("thinking", "")

    # AI応答も履歴に追加
    messages.append({"role": "assistant", "content": answer_content})
    session['chat_history'] = messages

    return {
        "thinking": thinking_content,
        "answer": answer_content
    }