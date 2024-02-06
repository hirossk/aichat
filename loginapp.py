from flask import Flask
from flask_login import UserMixin,LoginManager,login_user,login_required

app = Flask(__name__)
app.secret_key = "user"

class User(UserMixin):
   def __init__(self,id):
      self.id = id

login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return User(user_id)

@app.route("/login")
def login():
    login_user(User(1))
    return "Login完了"

@app.route("/authorized")
@login_required
def authorized():
    return "認証済です"

if __name__=='__main__':
    app.run(host="0.0.0.0",port=80,debug=False)