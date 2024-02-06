from flask import Flask,render_template,request
from dbaccess import db_connect,db_close,db_insert,db_select,db_initialize

app = Flask(__name__, static_folder="./static/")

@app.route('/')
def display():
    conn = db_connect()
    datalist = db_select(conn)    
    db_close(conn)
    return render_template('sqlite/form.html', datas = datalist)

@app.route("/commit",methods=["POST"])
def commit():
    conn = db_connect()
    # for key,value in request.form.items():
    #     print(key + ":" + value)    
    # if "name" in request.form:
    #     print("name is realize")
    db_insert(conn,request.form['name'],request.form['address'])
    datalist = db_select(conn)    
    db_close(conn)
    return render_template('sqlite/form.html', datas = datalist)

# データを初期化するためのエンドポイント
@app.route('/init')
def initialize():
    db_initialize()
    conn = db_connect()
    datalist = db_select(conn) 
    db_close(conn)
    return render_template('sqlite/form.html', datas = datalist)

if __name__ == "__main__":
    app.run(host="0.0.0.0",port=80,debug=False)