from flask import Flask, render_template, jsonify, session, redirect, url_for

from sql import connect_mysql
from sql.connect_mysql import select_all_data, select_two_conditions, select_column_data

app = Flask(__name__, template_folder='D:\\Download\\Idiom_Solitaire\\chinese-xinhua-master\\templates',
            static_folder='D:\\Download\\Idiom_Solitaire\\chinese-xinhua-master\\src\\static')
app.secret_key = 'your_secret_key'  # 设置密钥以使用 session

@app.route('/favicon.ico')
def favicon():
    return '', 204  # 返回 no content

@app.route('/gameRecords', methods=['GET', 'POST'])
def gameRecords():
    # userName = session['username']
    conn = connect_mysql.create_connection()
    conn.commit()
    # records = select_all_data(conn, 'co_user_play_record', 'USER_NAME', userName)
    records = select_all_data(conn, 'co_user_play_record', 'USER_NAME', 'Anna')
    # print('records=', records)
    all_idioms = []
    # all_idioms = ViewResults()
    # print('all_idioms = ', all_idioms)
    return render_template('game_records.html', records=records, all_idioms=all_idioms)

@app.route('/get_idioms/<game_id>', methods=['GET'])
def get_idioms(game_id):
    # 根据 game_id 查询成语
    conn = connect_mysql.create_connection()
    conn.commit()
    user_name = select_column_data(conn, 'co_user_play_record', 'USER_NAME', 'ID', game_id)
    user_name = user_name[0][0]
    # print('user_name=', user_name)
    ai_no = select_column_data(conn, 'co_user_play_record', 'AI_NO', 'ID', game_id)
    ai_no = ai_no[0][0]
    # print('ai_no=', ai_no)
    situation = select_column_data(conn, 'co_user_play_record', 'BATTLE_SITUATION', 'ID', game_id)
    situation = situation[0][0]
    # print('situation=', situation)

    user_idioms = select_two_conditions(conn, 'co_user_play_dtl', 'IDIOM', 'USER_NAME', user_name, 'BATTLE_SITUATION',
                                        situation)
    # print('user_idioms=', user_idioms)
    if user_idioms is not None:
        user_idioms = [item[0] for item in user_idioms]
    else:
        user_idioms = []

    ai_idioms = select_two_conditions(conn, 'co_ai_play_dtl', 'IDIOM', 'AI_NO', ai_no, 'BATTLE_SITUATION', situation)
    # print('ai_idioms=', ai_idioms)
    if ai_idioms is not None:
        ai_idioms = [item[0] for item in ai_idioms]
    else:
        ai_idioms = []

    first_play = select_column_data(conn, 'co_user_play_record', 'FIRST_PLAY', 'ID', game_id)
    first_play = [item[0] for item in first_play][0]

    winner = select_column_data(conn, 'co_user_play_record', 'SCORE', 'ID', game_id)
    winner = [item[0] for item in winner][0]

    # print('firstPlay=', first_play)
    # print('winner=', winner)

    all_idioms = []
    if first_play == 'user' and winner == 'user':
        for idiom in range(len(ai_idioms)):
            all_idioms.append(user_idioms[idiom])
            all_idioms.append(ai_idioms[idiom])
        all_idioms.append(user_idioms[-1])
    elif first_play == 'user' and winner == 'AI':
        for idiom in range(len(ai_idioms)):
            all_idioms.append(user_idioms[idiom])
            all_idioms.append(ai_idioms[idiom])
    elif first_play == 'AI' and winner == 'user':
        for idiom in range(len(ai_idioms)):
            all_idioms.append(ai_idioms[idiom])
            all_idioms.append(user_idioms[idiom])
    else:
        for idiom in range(len(user_idioms)):
            all_idioms.append(ai_idioms[idiom])
            all_idioms.append(user_idioms[idiom])
        all_idioms.append(ai_idioms[-1])
    # print('all_idioms=', all_idioms)
    return jsonify({'idioms': all_idioms})

@app.route('/')
def home():
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('username', None)  # 清除 session 中的 username
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.debug = True
    app.run()