from flask import Flask
from flask_socketio import SocketIO, emit
 
import time
 
app = Flask(__name__)
sio = SocketIO(app)  # socketを初期化
 
 
@sio.on("ping")  # pingイベントが届いたら呼ばれるコールバック
def ping(data):
    print(data)
    print(time.time())
    for cnt in range(10):
        time.sleep(2)
        emit("pong", str(time.time()))
 

@app.route("/")  # これはただのFlaskエンドポイント
def index():
    # 1ファイルで済ませるためjsを直書き
    script = """
    <!--JSのSocket.IOクライアントを読み込む-->
    <script src="https://cdnjs.cloudflare.com/ajax/libs/socket.io/4.0.1/socket.io.js" integrity="sha512-q/dWJ3kcmjBLU4Qc47E4A9kTB4m3wuTY7vkFJDTZKjTs8jhyGQnaUrxa0Ytd0ssMZhbNua9hE+E7Qv1j+DyZwA==" crossorigin="anonymous"></script>
<script type="text/javascript" charset="utf-8">
    var socket = io();
    function ping(){
        t = new Date();
        socket.emit('ping', {data: t.getTime()});  // サーバにpingイベントを投げつける
        document.getElementById("log").innerHTML += ('ping: ' + t.getTime() + "<br>");
    }
    socket.on('connect', function() { // 初期化時に呼ばれるコールバック
        socket.on('pong', (msg) => { // pongが帰ってきたら呼ばれるコールバック
            t = new Date();
            document.getElementById("log").innerHTML += ('pong: ' + t.getTime() + "<br>");
        });
        //ping();
    });
    window.addEventListener('load',function(){
    socket.emit('ping', {data: "hello"});
    })
</script>
<button type="button" onclick="ping();"> Ping </button>
<div id="log"></div>
    """
    return script 
 
 
if __name__ =="__main__":
    sio.run(app, host="0.0.0.0", port=5001)