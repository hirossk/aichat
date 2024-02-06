from flask import Flask,render_template
from flask_socketio import SocketIO, emit
 
import time
 
app = Flask(__name__)
sio = SocketIO(app)  # socketを初期化

@sio.on("ping")  # pingイベントが届いたら呼ばれるコールバック
def ping(data):
    print(data)
    emit("pong", str(time.time()))
 

@app.route("/")  # これはただのFlaskエンドポイント
def index():
    return render_template('websocket/websocket.html') 
 
 
if __name__ =="__main__":
    sio.run(app, host="0.0.0.0", port=5001)