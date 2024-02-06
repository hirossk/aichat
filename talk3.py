from flask import Flask,render_template
from PIL import Image
import csv

app = Flask(__name__, static_folder="./static/")
    
# CSVファイルを使って辞書のリストを作成する関数
def create_talk():
    listdata = []
    filename = 'message.csv'
    try:
        with open(filename, encoding='utf8', newline='') as f:
            csvreader = csv.reader(f)
            for row in csvreader:
                dictdata = dict([('icon', row[0]), ('position', row[1]),
                                  ('message', row[2]), ('continue', row[3])])
                listdata.append(dictdata)
    except Exception as e:
        # pass
        print(e)
    if (len(listdata) < 0):
        listdata =  [
            {
            "icon": "girl.png",
            "position": "left",
            "message": "こんにちは",
            },
            {
            "icon": "boy.png",
            "position": "right",
            "message": "こんにちは",
            },
        ]
    return listdata

# URLアクセスのパス指定すると次に記述している関数が呼び出される
@app.route('/')
def display():
    # Jinjaテンプレートによる展開が行われる
    return render_template('talk/talk0.html')

# '/'URLに数値を指定すると呼び出される関数定義
@app.route('/<int:id>')
def loopmessage(id):
    # create_talk関数の呼び出し
    talks = create_talk()
    # Jinjaテンプレートによる展開が行われる（talksはhtml内で利用される）
    return render_template('talk/talk' + str(id) + '.html',talks = talks)
    
    return html

if __name__=='__main__':
    app.run(host="0.0.0.0",port=80,debug=False)