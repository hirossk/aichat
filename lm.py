from flask import Flask,render_template,request, jsonify
from dblm import db_connect,db_close

app = Flask(__name__, static_folder="./static/")

@app.route('/')
def toppage():
    # トップページを表示する
    return render_template('lm/login.html')

@app.route('/signup')
def signup():
    # トップページを表示する
    return render_template('lm/signup.html')

@app.route('/bookadd')
def books_add():
    # トップページを表示する
    return render_template('lm/bookadd.html')

@app.route('/registuser', methods=['GET', 'POST'])
def registuser():
    if request.method == 'GET':
        return render_template('lm/signup.html',message = '不正なアクセス（GETはダメ）')
    # トップページを表示する
    else:
        if request.form.get('password') != request.form.get('confirmpassword'):
            return render_template('lm/signup.html',message = 'passwordが異なります。')
        # データベースへ登録(insert)する

        return render_template('lm/login.html',message = '登録しました')

@app.route('/registbook', methods=['GET', 'POST'])
def registbook():
    if request.method == 'GET':
        return render_template('lm/bookadd.html',message = '不正なアクセス（GETはダメ）')
    # トップページを表示する
    else:
        return render_template('lm/login.html',message = '登録しました')
    
@app.route('/booklist', methods=['GET', 'POST'])
def booklist():
    if request.method == 'GET':
        return render_template('lm/booklist.html',message = '不正なアクセス（GETはダメ）')

@app.route('/userlist', methods=['GET', 'POST'])
def userlist():
    if request.method == 'GET':
        return render_template('lm/userlist.html',message = '不正なアクセス（GETはダメ）')
        
@app.route('/userpage')
def userpage():
    # ユーザーページ（ダミー）
    return 'ユーザーログインページ'

if __name__=='__main__':
    app.run(host="0.0.0.0",port=80,debug=False)