var $form = $("#new-message");

window.onload = function () {
    // ↪︎ windowがロードされた時にアクションを実行するように設定
    if (document.getElementById("area")) {
        // ↪︎ areaのIDがある場合に処理を実行させる（これがないとチャット画面がなくても常にJavaScriptが動いてしまいます）
        var scrollPosition = document.getElementById("area").scrollTop;
        // ↪︎ area要素のスクロールされた時の最も高い場所を取得
        var scrollHeight = document.getElementById("area").scrollHeight;
        // ↪︎ area要素自体の最も高い場所を取得
        document.getElementById("area").scrollTop = scrollHeight;
        // ↪︎ area要素のスクロールされた時の最も高い場所をarea要素自体の最も高い場所として指定してあげる
    }
}

function ajax(){
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
            // $("#message_area").append("<div class=\"bubble right\"><img class=\"righticon\" src=\"/static/images/boy.png\" alt=\"\">" + message + "</div>");
            $("#message_area").append("<div class=\"bubble right\"><div class=\"righticon\">" + face + "</div>" + message);
            // $('.result').html(data);
            var answer = data_json['answer'];
            $("#message_area").append("<div class=\"bubble left\"><img class=\"lefticon\" src=\"/static/images/cyber.png\" alt=\"\">" + answer + "</div>");
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
            $ta.val("");
        });

    //   $form.submit();
}

$(document).on("keydown", "#message-text", function (e) {
    var $ta = $("#message-text")
    if (e.keyCode == 13) { // Enterが押された
        if (e.shiftKey) { // Shiftキーも押された
            $.noop();
        } else if ($ta.val().replace("/\s/g", "").length > 0) {
            e.preventDefault();
            ajax();
        }
    } else {
        $.noop();
    }
});

$(document).on("mousedown", "#submit", function (e) {
    var $ta = $("#message-text")
    if ($ta.val().replace("/\s/g", "").length > 0) {
        e.preventDefault();
        ajax();
    }
});