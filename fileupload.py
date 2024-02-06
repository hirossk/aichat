from flask import Flask,render_template,request

app = Flask(__name__, static_folder="./static/")

@app.route('/')
def display():
    return render_template('form.html')

@app.route("/upload",methods=["POST"])
def upload():
    name = "picture"
    if name in request.files:
        fs = request.files[name]
        fs.save("uploadfiles/"+fs.filename)
        return "ok"
    else:
        return "ng"

if __name__ == "__main__":
    app.run(host="0.0.0.0",port=80,debug=False)