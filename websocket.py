from flask import Flask, render_template, session
from flask_socketio import SocketIO, emit
import os

async_mode = None

app = Flask(__name__)
# セッションを利用する場合は必須
app.config['SECRET_KEY'] = os.urandom(24)
# websocketを使う通信のsocketioを生成
socketio = SocketIO(app)

# エンドポイント
@app.route('/')
def index():
    return render_template('websocket/websocket.html', async_mode=socketio.async_mode)

# emitで'my_event'を送られたときの処理
@socketio.event
def my_event(message):
    # セッションの値を更新しているだけ(セッションのカウンター) 
    session['receive_count'] = session.get('receive_count', 0) + 1
    # ブラウザーに'my_response'として受け取ったJSONのdataを送信
    emit('my_response',
         {'data': message['data'], 'count': session['receive_count']})

# emitで'my_broadcast_event'を送られたときの処理
@socketio.event
def my_broadcast_event(message):
    # セッションの値を更新しているだけ(セッションのカウンター) 
    session['receive_count'] = session.get('receive_count', 0) + 1
    # # ブラウザーに'my_response'として受け取ったJSONのdataを送信
    emit('my_response',
         {'data': message['data'], 'count': session['receive_count']},
         broadcast=True) # broadcast=Trueとすることで全体へ送り返す

if __name__ == '__main__':
    socketio.run(app,port=80,debug=False)