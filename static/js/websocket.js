// websocketの生成
var socket = io();

socket.on('connect', function () { // ソケットの初期化時に呼ばれるコールバック
    socket.on('my_response', (msg) => { // my_responseが送られてきたら呼ばれるコールバック
        //logの後ろにデータを追加している
        document.getElementById("log").innerHTML += 'Received #' + msg.count + ': ' + msg.data + '<br>';
    });
});

// エコーボタンが押されたときの処理
function my_event() {
    socket.emit('my_event', { data: document.getElementById("emit_data").value }); 
}
// ブロードキャストボタンが押されたときの処理
function my_broadcast_event() {
    socket.emit('my_broadcast_event', { data: document.getElementById("broadcast_data").value }); 
}

