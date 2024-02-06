from flask import Flask,render_template

app = Flask(__name__, static_folder="./static/")
   
def create_talk():
    return  [
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

@app.route('/')
def display():
    return render_template('talk0.html')

@app.route('/<int:id>')
def loopmessage(id):
    talks = create_talk()
    return render_template('talk' + str(id) + '.html',talks = talks)
    
    return html

if __name__=='__main__':
    app.run(host="0.0.0.0",port=80,debug=False)