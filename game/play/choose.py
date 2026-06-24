
from flask import Flask, render_template, request, jsonify, session, redirect, url_for

from sql import connect_mysql

app = Flask(__name__, template_folder='D:\\Download\\Idiom_Solitaire\\chinese-xinhua-master\\templates',
            static_folder='D:\\Download\\Idiom_Solitaire\\chinese-xinhua-master\\src\\static')
app.secret_key = 'your_secret_key'  # 设置密钥以使用 session

@app.route('/favicon.ico')
def favicon():
    return '', 204  # 返回 no content

@app.route('/choose', methods=['GET', 'POST'])
def choose():
    conn = connect_mysql.create_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT AI_CODE, Img_url FROM sys_ai_info where IS_USE = '10000001'")
    # 获取所有结果
    result = cursor.fetchall()
    return render_template('choose.html', result=result)

@app.route('/submit', methods=['POST'])
def submit():
    value = request.json.get('value')
    print(f'Received value: {value}')
    session['aiNo'] = value
    return jsonify(success=True)

@app.route('/battle', methods=['GET', 'POST'])
def battle():
    if request.method == 'POST':
        return render_template('battle.html')  # 返回 battle 页面
    else:
        # 如果是 GET 请求，可以返回选择页面或报错
        return redirect(url_for('choose'))

# app.add_url_rule('/battle', view_func=battle, methods=['GET', 'POST'])
# app.add_url_rule('/AIFirst', view_func=AIFirst, methods=['POST'])
# app.add_url_rule('/userFirst', view_func=userFirst, methods=['POST'])


if __name__ == '__main__':
    app.debug = True
    app.run()


