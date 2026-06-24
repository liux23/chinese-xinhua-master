
from flask import Flask, render_template, request

from game.play.AI_first_play import AIFirst
from game.play.user_first_play import UserFirst

app = Flask(__name__, template_folder='D:\\Download\\Idiom_Solitaire\\chinese-xinhua-master\\templates',
            static_folder='D:\\Download\\Idiom_Solitaire\\chinese-xinhua-master\\src\\static')
app.secret_key = 'your_secret_key'  # 设置密钥以使用 session

@app.route('/favicon.ico')
def favicon():
    return '', 204  # 返回 no content

@app.route('/battle', methods=['GET', 'POST'])
def battle():
    if request.method == 'POST':
        return render_template('battle_page.html')

app.add_url_rule('/UserFirst', view_func=UserFirst, methods=['POST'])
app.add_url_rule('/AIFirst', view_func=AIFirst, methods=['POST'])

if __name__ == '__main__':
    app.debug = True
    app.run()
