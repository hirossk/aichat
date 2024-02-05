from flask import Flask,render_template,request
from PIL import Image, ImageDraw

app = Flask(__name__, static_folder="./static/")

@app.route('/')
def display():
    return render_template('talk0.html')

if __name__=='__main__':
    app.run(host="0.0.0.0",port=80,debug=False)