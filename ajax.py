from flask import Flask,render_template,request, jsonify

app = Flask(__name__, static_folder="./static/")

@app.route('/')
@app.route('/01ajax')
def ajax_one():
    # トップページを表示する
    return render_template('ajax/01ajax.html')

@app.route('/02ajax')
def ajax_two():
    # トップページを表示する
    return render_template('ajax/02ajax.html')

@app.route('/03ajax')
def ajax_three():
    # トップページを表示する
    return render_template('ajax/03ajax.html')

@app.route('/api01')
def ajax01_response():
    # APIの戻り値
    return "Hello Ajax"

@app.route('/api02', methods=['GET', 'POST'])
def ajax02_response():
    val1 = request.args.get('v1')
    val2 = request.args.get('v2')
    num1 = int(val1)
    num2 = int(val2)
    result = num1 + num2
    print(result)
    # # APIの戻り値
    return jsonify(result), 200

if __name__=='__main__':
    app.run(host="0.0.0.0",port=80,debug=False)