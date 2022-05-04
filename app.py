from flask import Flask,render_template, request



#flaskオブジェクトの作成
app = Flask(__name__)

#htmlファイルの値を受け取る
@app.route('/', methods=['GET'])
def get():
    return render_template('form.html')

#postのときの処理 
@app.route('/', methods=['POST'])
def post():
    twitter_id = request.form['twitter_id']

    print(twitter_id)
    return render_template('form.html')

#pythonで実行されたときに処理をする
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)