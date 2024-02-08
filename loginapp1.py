from flask import Flask,request,redirect,render_template
from flask_login import UserMixin,LoginManager,login_user,login_required,logout_user
from dblogin import db_connect,db_initialize,db_check_login
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)

# flask_loginを利用したサンプル
# login管理の初期化
login_manager = LoginManager()
login_manager.init_app(app)

# ユーザーデータを格納するためのクラス
class User(UserMixin):
    def __init__(self,userid):
        self.id = userid

# current_userでユーザーを利用したい場合に呼び出される
@login_manager.user_loader
def user_loader(userid: str):
    user = User(userid)
    # idを設定しなければならない
    return user

# @login_requiredで指定された関数がログインなしで呼ばれた場合の処理
@login_manager.unauthorized_handler
def unauthorized():
    return redirect('/login')

@app.route('/')
@app.route('/login', methods=['GET', 'POST'])
def login():
    # このページがGETで表示されるとログイン画面（ユーザID,パスワード入力）
    if request.method == 'GET':
        return render_template('login/login.html')

    # POSTで呼び出されるとユーザーIDとパスワードのチェックを行う
    username = request.form['username']
    passwd = request.form['passwd']
    conn = db_connect()
    # データベース上のチェックを行う
    if (db_check_login(conn,username,passwd) == True):
        # ユーザーIDとパスワードが一致した場合
        # idを設定しなければならない
        user = User(username)
        login_user(user)
        # protectedのURLを呼び出す
        return redirect("protected")

    # ユーザーIDとパスワードが一致しなかった場合はログインへ戻る
    return render_template('login/login.html',message = 'ログインできません')

@app.route('/protected')
# ログインしていないと表示できないという意味
@login_required
def protected():
    return render_template('login/content.html')

@app.route('/logout')
def logout():
    # ログアウト処理はこの１行
    logout_user()
    return render_template('login/logout.html')

@app.route('/init')
def initialize():
    db_initialize()
    return "Initialized Database"

if __name__=='__main__':
    app.run(host="0.0.0.0",port=80,debug=False)