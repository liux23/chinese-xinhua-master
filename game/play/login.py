from flask import Flask, render_template, request, redirect, url_for, flash, session

from game.play.routes import register_routes
from sql import connect_mysql
import datetime
import faulthandler
faulthandler.enable()

app = Flask(__name__, template_folder='D:\\Download\\Idiom_Solitaire\\chinese-xinhua-master\\templates',
            static_folder='D:\\Download\\Idiom_Solitaire\\chinese-xinhua-master\\src\\static')
app.secret_key = 'your_secret_key'  # 用于会话加密

current_time = datetime.datetime.now()
# 格式化时间
formatted_time = current_time.strftime("%Y-%m-%d %H:%M:%S")

def insert_user_pwd_data(username, password):
    user_pwd_data = {
        'password': password,
        'last_login': formatted_time,
        'is_superuser': 1,
        'user_name': username,
        'is_staff': 1,
        'is_active': 1,
        'date_joined': formatted_time
    }
    return user_pwd_data

def insert_user_info_data(username):
    user_info_data = {
        'user_name': username,
        'ROLE_CODE': '001',
        'ROLE_NAME': 'rabbit01',
        'ON_LINE': 10000001,
        'IS_USE': 10000001,
        'REMARK': None,
        'INST_TIME': formatted_time,
        'INST_USER_NO': 'sys'
    }
    return user_info_data


@app.route('/')
def home():
    # print('Welcome!!!')
    return render_template('login.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    # print('username=', username)
    # print('password=', password)

    # 查询用户数据库
    conn = connect_mysql.create_connection()
    is_user = connect_mysql.select_data(conn, 'auth_user', 'USER_NAME', username)
    # print('is_user=', is_user)
    if is_user:
        result = connect_mysql.select_column_data(conn, 'auth_user', 'password', 'USER_NAME', username)
        pwd = result[0]
        Pword = pwd[0]
        # print('pwd=', Pword)
        # 将结果转换为字典
        users = {username: Pword}
        # 输出字典
        # print('users=', users)
        # print('pwd=', users[username])
        if users[username] == password:
            # flash('登录成功！')
            session['username'] = username  # 保存用户会话
            connect_mysql.connect_sql_update('co_user_info', 'ON_LINE', '10000001', 'USER_NAME', username)

            return redirect(url_for('start'))
        else:
            flash('密码错误！')
            return redirect(url_for('home'))
    else:
        # flash('用户名错误！')
        # flash('新用户注册成功！')
        insert_pwd_data = insert_user_pwd_data(username, password)
        insert_user_data = insert_user_info_data(username)
        connect_mysql.connect_sql_insert('auth_user', insert_pwd_data)
        connect_mysql.connect_sql_insert('co_user_info', insert_user_data)
        return redirect(url_for('start'))

@app.route('/start', methods=['GET', 'POST'])
def start():
    # 清空特定的 session 数据
    session.pop('used_idioms', None)  # 移除 used_idioms
    session.pop('last_char', None)  # 移除 last_char
    session.pop('initial_ai_idiom', None)  # 移除 initial_ai_idiom

    if 'username' in session:
        return render_template('start.html')
    return redirect(url_for('start'))

@app.route('/logout')
def logout():
    session.clear()  # 清除会话数据
    return redirect(url_for('home'))


# 注册路由
register_routes(app)

if __name__ == '__main__':
    # app.debug = True
    # app.run()
    # 同一局域网下，可在手机上查看
    app.run(host='0.0.0.0', port=5000, debug=True, use_reloader=False)