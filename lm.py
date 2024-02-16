from flask import Flask,render_template,request, jsonify
from dblm import db_connect,db_close

app = Flask(__name__, static_folder="./static/")

@app.route('/')
def toppage():
    # トップページを表示する
    return 'toppage'

@app.route('/signup')
def signup():
    # トップページを表示する
    return render_template('lm/signup.html')

@app.route('/regist', methods=['GET', 'POST'])
def regist():
    if request.method == 'GET':
        return render_template('lm/signup.html',message = '不正なアクセス（GETはダメ）')
    # トップページを表示する
    else:
        if request.form.get('password') != request.form.get('confirmpassword'):
            return render_template('lm/signup.html',message = 'passwordが異なります。')
        return render_template('lm/login.html',message = '登録しました')

@app.route('/userpage')
def userpage():
    # ユーザーページ（ダミー）
    return 'ユーザーログインページ'

if __name__=='__main__':
    app.run(host="0.0.0.0",port=80,debug=False)