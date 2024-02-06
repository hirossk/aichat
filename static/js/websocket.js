var socket = io();

function ping() {
    t = new Date();
    socket.emit('ping', { data: t.getTime() });  // サーバにpingイベントを投げつける
    document.getElementById("log").innerHTML += ('ping: ' + t.getTime() + "<br>");
}
socket.on('connect', function () { // 初期化時に呼ばれるコールバック
    socket.on('pong', (msg) => { // pongが帰ってきたら呼ばれるコールバック
        t = new Date();
        document.getElementById("log").innerHTML += ('pong: ' + t.getTime() + msg + "<br>");
    });
});
window.addEventListener('load', function () {
    socket.emit('ping', { data: "hello" });
})
