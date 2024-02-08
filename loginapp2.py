from flask import Flask,redirect,render_template,request
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
import os

app = Flask(__name__)

#DBはSQLiteを使う
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///login.db'

#sessionを使う際にSECRET_KEYを設定
app.config['SECRET_KEY'] = os.urandom(24)

#SQLALchemyを使います宣言
db = SQLAlchemy(app)


# flask_loginを利用したサンプル
# login管理の初期化
login_manager = LoginManager()
login_manager.init_app(app)

#Userというクラスでテーブル定義する(データベースに格納するデータ)
class User(UserMixin, db.Model):
    # idは必須項目
    id = db.Column(db.Integer, primary_key=True)
    # その他は任意の項目
    username = db.Column(db.String(30))
    password = db.Column(db.String(50))
    email = db.Column(db.String(50))

#DBのクリエイト宣言
with app.app_context():
    db.create_all()

    #DBが空の状態(最初の1回)であれば初期化する
    user_count = db.session.query(User).count()
    if user_count == 0:
        testuser = User(username='testuser1', password='pass1', email='test@test')
        db.session.add(testuser)
        testuser = User(username='testuser2', password='pass2', email='test@test')
        db.session.add(testuser)
        db.session.commit()

# @login_requiredで指定された関数がログインなしで呼ばれた場合の処理
@login_manager.unauthorized_handler
def unauthorized():
    return redirect('/')

# ログイン中のユーザーデータの取得
@login_manager.user_loader
def load_user(user_id):
    # ログインユーザーの情報を取得する
    # current_userで参照するデータ
    return User.query.get(int(user_id))

@app.route('/')
def index():        
    return render_template('login/login.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    # POSTで呼び出されるとユーザーIDとパスワードのチェックを行う
    username = request.form['username']
    passwd = request.form['passwd']
    user = User.query.filter_by(username=username,password=passwd).first()
    # データベース上のチェックを行う
    if user is not None:
        # ユーザーIDとパスワードが一致した場合
        # login状態とする
        login_user(user)
        # protectedのURLを呼び出す
        return redirect("protected")

    # ユーザーIDとパスワードが一致しなかった場合はログインへ戻る
    return render_template('login/login.html',message = 'ログインできません')

@app.route('/signup')
def signup():        
    return render_template('login/signup.html')

@app.route('/regist', methods=['POST'])
def regist():        
    # POSTで呼び出されるとユーザーIDとパスワード,emailの追加を行う
    username = request.form['username']
    passwd = request.form['passwd']
    email = request.form['email']
    registuser = User(username=username, password=passwd, email=email)
    db.session.add(registuser)
    db.session.commit()
    return redirect('/')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return 'Now logout OK'

@app.route('/protected')
@login_required
def protected():
    return 'The current :id is ' + str(current_user.id) + ' :username is '+ current_user.username

if __name__=='__main__':
    app.run(host="0.0.0.0",port=80,debug=False)