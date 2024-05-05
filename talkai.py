from flask import Flask,render_template,request
import json
import boto3

import pprint

app = Flask(__name__, static_folder="./static/")

#文章解析のエンジンへの接続
comprehend=boto3.client('comprehend', region_name='ap-northeast-1')

#生成AIエンジンへの接続
bedrock = boto3.client('bedrock', region_name='ap-northeast-1')
bedrock_runtime = boto3.client('bedrock-runtime', region_name='ap-northeast-1')

# comdetect = ComprehendDetect(comprehend)
    
# '/'URLに数値を指定すると呼び出される関数定義
@app.route('/')
def loopmessage():
    # create_talk関数の呼び出し
    # Jinjaテンプレートによる展開が行われる（talksはhtml内で利用される）
    return render_template('talk/talk.html')

# Ajax用コールメソッド
@app.route("/call_ajax", methods = ["POST"])
def callfromajax():
    if request.method == "POST":
        # ここにPythonの処理を書く
        try:
            frommessage = request.form["sendmessage"]
            answer = f"あなたのメッセージは「{frommessage}」"
        # pprint(comdetect.detect_sentiment("",'ja'))
            # print(frommessage)
            response = comprehend.detect_sentiment(Text=frommessage, LanguageCode='ja')
            pprint.pprint(response['SentimentScore'])
            response = comprehend.detect_key_phrases(Text=frommessage, LanguageCode='ja')
            pprint.pprint(response['KeyPhrases'])
            prompt = """Human: """ + frommessage + """
                    Assistant:"""
            body = json.dumps(
                {
                "prompt": prompt,
                "max_tokens_to_sample": 500,
                }
            )
            response = bedrock_runtime.invoke_model(
                modelId="anthropic.claude-v2:1",
                body=body,
                contentType="application/json",
                accept="application/json",
                )
            decode_answer = response["body"].read().decode()
            answer = json.loads(decode_answer)["completion"]

        except Exception as e:
            answer = str(e)
        
        dict = {"answer": answer,
                "message": frommessage,
                "face": "😊"}      # 辞書
    return json.dumps(dict, ensure_ascii=False)             # 辞書をJSONにして返す

if __name__=='__main__':
    app.run(host="0.0.0.0",port=80,debug=False)