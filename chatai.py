from flask import Flask,render_template,request, send_file,jsonify
import json
import boto3
from util import getface,InvalidUsage
from botocore.exceptions import BotoCoreError, ClientError
import pprint
import os



app = Flask(__name__, static_folder="./static/")

#文章解析のエンジンへの接続
comprehend=boto3.client('comprehend', region_name='ap-northeast-1')

#生成AIエンジンへの接続
bedrock = boto3.client('bedrock', region_name='ap-northeast-1')
bedrock_runtime = boto3.client('bedrock-runtime', region_name='ap-northeast-1')

# Mapping the output format used in the client to the content type for the
# response
AUDIO_FORMATS = {"ogg_vorbis": "audio/ogg",
                 "mp3": "audio/mpeg",
                 "pcm": "audio/wave; codecs=1"}

# Create a client using the credentials and region defined in the adminuser
# section of the AWS credentials and configuration files
# session = Session(profile_name="hry-sasaki")
polly = boto3.client('polly', region_name='ap-northeast-1')

   
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
    if request.method == "POST":
        # ここにPythonの処理を書く
        try:
            frommessage = request.form["sendmessage"]
            answer = f"あなたのメッセージは「{frommessage}」"
            # チャットメッセージの理解をする
            response = comprehend.detect_sentiment(Text=frommessage, LanguageCode='ja')
            sentiment_score = response['SentimentScore']
            # チャットメッセージのχフレーズを取得する
            keyresponse = comprehend.detect_key_phrases(Text=frommessage, LanguageCode='ja')
            pprint.pprint(keyresponse)
            
            # 生成AIによるメッセージの返送
            # prompt = """Human: """ + frommessage + """
            #         Assistant:"""
            # body = json.dumps(
            #     {
            #     "prompt": prompt,
            #     "max_tokens_to_sample": 500,
            #     }
            # )
            # response = bedrock_runtime.invoke_model(
            #     modelId="anthropic.claude-v2:1",
            #     body=body,
            #     contentType="application/json",
            #     accept="application/json",
            #     )
            # decode_answer = response["body"].read().decode()
            # answer = json.loads(decode_answer)["completion"]

        except Exception as e:
            answer = str(e)
        
        frommessage = frommessage.replace('\n','<br>')
        answer = answer.replace('\n','<br>')
        face = getface(sentiment_score)

        dict = {"answer": answer,
                "message": frommessage,
                "face": face}      # 辞書
    return json.dumps(dict, ensure_ascii=False)             # 辞書をJSONにして返す

@app.route('/read', methods=['GET'])
def read():
    """Handles routing for reading text (speech synthesis)"""
    # Get the parameters from the query string
    try:
        outputFormat = request.args.get('outputFormat')
        text = request.args.get('text')
        separate = request.args.get('voiceId').split("@")
        voiceId = separate[0]
        engine =  separate[1].split(',')[0]
        # voiceId = request.args.get('voiceId')
    except TypeError:
        raise InvalidUsage("Wrong parameters", status_code=400)

    # Validate the parameters, set error flag in case of unexpected
    # values
    if len(text) == 0 or len(voiceId) == 0 or \
            outputFormat not in AUDIO_FORMATS:
        raise InvalidUsage("Wrong parameters", status_code=400)
    else:
        try:
            # Request speech synthesis
            response = polly.synthesize_speech(Text=text,
                                               VoiceId=voiceId,
                                               Engine= engine,
                                               OutputFormat=outputFormat)
        except (BotoCoreError, ClientError) as err:
            # The service returned an error
            print(str(err))
            raise InvalidUsage(str(err), status_code=500)

        return send_file(response.get("AudioStream"),
                         AUDIO_FORMATS[outputFormat])


@app.route('/voices', methods=['GET'])
def voices():
    """Handles routing for listing available voices"""
    params = {}
    voices = []

    try:
        # Request list of available voices, if a continuation token
        # was returned by the previous call then use it to continue
        # listing
        response = polly.describe_voices(**params)
    except (BotoCoreError, ClientError) as err:
        # The service returned an error
        raise InvalidUsage(str(err), status_code=500)

    # Collect all the voices
    voices.extend(response.get("Voices", []))
    pprint.pprint(response)

    return jsonify(voices)

if __name__=='__main__':
    app.secret_key = os.urandom(24)
    app.debug = True
    app.run(host="0.0.0.0",port=80,debug=True)