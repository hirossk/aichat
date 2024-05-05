from flask import Flask,render_template,request
import json
import random
import csv

app = Flask(__name__, static_folder="./static/")
    
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
        except Exception as e:
            answer = str(e)
        dict = {"answer": answer}      # 辞書
    return json.dumps(dict, ensure_ascii=False)             # 辞書をJSONにして返す

if __name__=='__main__':
    app.run(host="0.0.0.0",port=80,debug=False)