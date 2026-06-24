
from flask import Flask, render_template

from game.play.AI_first_play import AIFirst

app = Flask(__name__, template_folder='D:\\Download\\Idiom_Solitaire\\chinese-xinhua-master\\templates',
            static_folder='D:\\Download\\Idiom_Solitaire\\chinese-xinhua-master\\src\\static')
app.secret_key = 'your_secret_key'  # 设置密钥以使用 session

@app.route('/favicon.ico')
def favicon():
    return '', 204  # 返回 no content


@app.route('/start', methods=['GET', 'POST'])
def start():
    return render_template('start.html')

@app.route('/battle', methods=['GET', 'POST'])
def battle():
    return render_template('battle_page.html')

@app.route('/choose', methods=['GET', 'POST'])
def choose():
    return render_template('choose.html')

@app.route('/userFirst', methods=['GET', 'POST'])
def UserFirst():
    return render_template('user_first_play.html')

app.add_url_rule('/AIFirst', view_func=AIFirst, methods=['POST'])


if __name__ == '__main__':
    app.run(debug=True)


