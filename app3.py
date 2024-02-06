from flask import Flask,render_template
from PIL import Image
import csv

app = Flask(__name__, static_folder="./static/")
    
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

@app.route('/')
def display():
    return render_template('talk0.html')

@app.route('/<int:id>')
def loopmessage(id):
    talks = create_talk()
    return render_template('talk' + str(id) + '.html',talks = talks)
    
    return html

@app.route('/reset',methods=['GET', 'POST'])
def reset_words():
    with open('file.txt', mode='w') as f:
        f.close()
    im = Image.new("RGB", (800, 600), (255, 255, 255))
    im.save('templates/images/imgdraw1.jpg', quality=95)
    im.save('templates/images/imgdraw2.jpg', quality=95)
    html = render_template('index.html',srcname = "images/imgdraw1.jpg")
    
    return html

if __name__=='__main__':
    app.run(host="0.0.0.0",port=80,debug=False)