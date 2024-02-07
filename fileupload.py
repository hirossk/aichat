from flask import Flask,render_template,request

app = Flask(__name__, static_folder="./static/")

# フォームを表示してファイルをアップロードさせる
@app.route('/')
def display():
    return render_template('upload/form.html')

# フォームのactionで指定したuploadをPOSTで呼び出す
@app.route("/upload",methods=["POST"])
def upload():
    name = "picture"
    # formの中にpictureが設定されているかチェック
    if name in request.files:
        fs = request.files[name]
        # uploadfilesフォルダーにファイルを保存する
        fs.save("uploadfiles/"+fs.filename)
        return "ok"
    else:
        # おかしなリクエストの場合はngの表示
        return "ng"

if __name__ == "__main__":
    app.run(host="0.0.0.0",port=80,debug=False)