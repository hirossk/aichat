from flask import Blueprint
from flask import request, send_file,jsonify
from util import InvalidUsage
from botocore.exceptions import BotoCoreError, ClientError
import boto3

AUDIO_FORMATS = {"ogg_vorbis": "audio/ogg",
                 "mp3": "audio/mpeg",
                 "pcm": "audio/wave; codecs=1"}

polly = boto3.client('polly', region_name='ap-northeast-1')
pollytext = ""

# Blueprintのオブジェクトを生成する
app = Blueprint('func1', __name__)

# 読み上げ機能
@app.route('/read', methods=['GET'])
def read():
    """Handles routing for reading text (speech synthesis)"""
    # Get the parameters from the query string
    try:
        outputFormat = request.args.get('outputFormat')
        # text = request.args.get('text')
        text = pollytext
        separate = request.args.get('voiceId').split("@")
        # 声の種類
        voiceId = separate[0]
        # エンジンの指定
        engine =  separate[1].split(',')[0]
        
    except TypeError:
        raise InvalidUsage("Wrong parameters", status_code=400)

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

    return jsonify(voices)
