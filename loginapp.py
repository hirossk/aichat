from flask import Flask,request,redirect,url_for,render_template
from flask_login import UserMixin,LoginManager,current_user,login_user,login_required,logout_user
from dblogin import db_connect,db_initialize,db_check_login

app = Flask(__name__)
app.secret_key = "user"

# flask_loginを利用したサンプル

# ユーザーデータを格納するためのクラス
class User(UserMixin):
    pass

login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def user_loader(username: str):
    user = User()
    # idを設定しなければならない
    user.id = username
    user.hoge = "hogehoge"
    return user

@app.route('/')
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login/login.html')

    username = request.form['username']
    passwd = request.form['passwd']
    conn = db_connect()
    if (db_check_login(conn,username,passwd) == True):
        user = User()
        # idを設定しなければならない
        user.id = username
        login_user(user)
        return redirect(url_for("protected"))

    return 'Bad login'

@app.route("/auth")
@login_required
def authorized():
    return current_user.id + "認証済み"

@app.route('/protected')
@login_required
def protected():
    return f'''
    Logged in as: {current_user.hoge} <a href='logout'>logout</a>
    '''

@app.route('/logout')
def logout():
    logout_user()
    return f'''
    Logged out
    <a href='login'>login</a>
    '''

@app.route('/init')
def initialize():
    db_initialize()
    return "Initialized Database"

if __name__=='__main__':
    app.run(host="0.0.0.0",port=80,debug=False)