from flask import Flask,render_template

app = Flask(__name__, static_folder="./static/")

# URLアクセスのパス指定すると次に記述しているメソッドが呼び出される
@app.route('/')
def display():
    # Jinjaテンプレートによる展開が行われる
    return render_template('talk/talk0.html')

if __name__=='__main__':
    app.run(host="0.0.0.0",port=80,debug=False)