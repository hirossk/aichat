//JavaScriptファイル
var $form = $("#new-message");

window.onload = function () {
    // windowがロードされた時にアクションを実行するように設定
    if (document.getElementById("area")) {
        // area要素のスクロールされた時の最も高い場所を取得
        var scrollHeight = document.getElementById("area").scrollHeight;
        // area要素自体の最も高い場所を取得
        document.getElementById("area").scrollTop = scrollHeight;
        // area要素のスクロールされた時の最も高い場所をarea要素自体の最も高い場所として指定してあげる
    }
}

function ajax_ai(message) {
    var $ta = $("#message-text")
    // 生成AIによる思考時間を「くるくる」させて待つ
    // dispLoading("考え中...");
    $.ajax({
        url: './response_ai',
        type: 'POST',
        data: {
            'sendmessage': message
        }
    })
        // Ajax通信が成功したら発動
        .done((data) => {
            var data_json = JSON.parse(data);
            var aiface = data_json['aiface'];
            var answer = data_json['answer'];
            removeLoading();
            if(aiface == null){
                $("#chat-area").append("<div class=\"bubble left\"><img class=\"lefticon\" src=\"/static/images/cyber.png\" alt=\"\">" + answer + "</div>");
            }else{
                $("#chat-area").append("<div class=\"bubble left\"><div class=\"lefticon\">" + aiface + "</div>" + answer + "</div>");
            }
        })
        // Ajax通信が失敗したら発動
        .fail((jqXHR, textStatus, errorThrown) => {
            alert('Ajax通信に失敗しました。');
            console.log("jqXHR          : " + jqXHR.status); // HTTPステータスを表示
            console.log("textStatus     : " + textStatus);    // タイムアウト、パースエラーなどのエラー情報を表示
            console.log("errorThrown    : " + errorThrown.message); // 例外情報を表示
        })
        // Ajax通信が成功・失敗のどちらでも発動
        .always((data) => {
            autoscroll();
        });

}

function ajax_user() {
    var $ta = $("#message-text")
    // Ajax通信
    $.ajax({
        url: './call_ajax',
        type: 'POST',
        data: {
            'sendmessage': $ta.val()
        }
    })
        // Ajax通信が成功したら発動
        .done((data) => {
            var data_json = JSON.parse(data);
            var face = data_json['face'];
            var message = data_json['message'];
            $("#chat-area").append("<div class=\"bubble right\"><div class=\"righticon\">" + face + "</div>" + message);
            // 生成AIによるメッセージ生成を呼び出す
            ajax_ai(message);
        })
        // Ajax通信が失敗したら発動
        .fail((jqXHR, textStatus, errorThrown) => {
            alert('Ajax通信に失敗しました。');
            console.log("jqXHR          : " + jqXHR.status); // HTTPステータスを表示
            console.log("textStatus     : " + textStatus);    // タイムアウト、パースエラーなどのエラー情報を表示
            console.log("errorThrown    : " + errorThrown.message); // 例外情報を表示
        })
        // Ajax通信が成功・失敗のどちらでも発動
        .always((data) => {
            autoscroll();
            $ta.val("");
        });

}

//Enterキーを押したときの動作
$(document).on("keydown", "#message-text", function (e) {
    var $ta = $("#message-text")
    if (e.keyCode == 13) { // Enterが押された
        if (e.shiftKey) { // Shiftキーも押された
            $.noop();
        } else if ($ta.val().replace(/\s/g, "").length > 0) {
            e.preventDefault();
            ajax_user();
        }
    } else {
        $.noop();
    }
});
//送信ボタンを押したときの動作
$(document).on("mousedown", "#submit", function (e) {
    var $ta = $("#message-text")
    if ($ta.val().replace("/\s/g", "").length > 0) {
        e.preventDefault();
        ajax_user();
    }
});

function autoscroll(){
    if (document.getElementById("area")) {
        // ↪︎ areaのIDがある場合に処理を実行させる（これがないとチャット画面がなくても常にJavaScriptが動いてしまいます）
        var scrollHeight = document.getElementById("area").scrollHeight;
        // ↪︎ area要素自体の最も高い場所を取得
        let tgt;
        if ('scrollingElement' in document) {
            tgt = document.scrollingElement;
        } else if (this.browser.isWebKit) {
            tgt = document.body;
        } else {
            tgt = document.documentElement;
        }
        tgt.scrollTop = scrollHeight;
    }
}

// Loading開始用の関数
function dispLoading(msg){
  // 引数なしの場合、メッセージは非表示。
  if(msg === undefined ) msg = "";
  
  // 画面表示メッセージを埋め込み
  var innerMsg = "<div id='innerMsg'>" + msg + "</div>";  
  
  // ローディング画像が非表示かどうかチェックし、非表示の場合のみ出力。
  if($("#nowLoading").length == 0){
    $("#chat-area").append("<div id='nowLoading'>" + innerMsg + "</div>");
  }
}
 
// Loading終了用の関数
function removeLoading(){
  $("#nowLoading").remove();
}  