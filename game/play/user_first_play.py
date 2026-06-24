
from flask import Flask, render_template, request, session, jsonify, url_for
import pandas as pd
import json
from sql import connect_mysql
import datetime
import random

app = Flask(__name__, template_folder='D:\\Download\\Idiom_Solitaire\\chinese-xinhua-master\\templates',
            static_folder='D:\\Download\\Idiom_Solitaire\\chinese-xinhua-master\\src\\static')
app.secret_key = 'your_secret_key'  # 设置密钥以使用 session

# 全局变量存储对话记录
dialog_records = {
    'dialog_ai': [],
    'dialog_player': [],
    'first_speaker': 'user'
}

def remove_tone(pinyin):
    tone_map = {
        "ā": "a", "á": "a", "ǎ": "a", "à": "a",
        "ē": "e", "é": "e", "ě": "e", "è": "e",
        "ī": "i", "í": "i", "ǐ": "i", "ì": "i",
        "ō": "o", "ó": "o", "ǒ": "o", "ò": "o",
        "ū": "u", "ú": "u", "ǔ": "u", "ù": "u"
    }
    return ''.join(tone_map.get(char, char) for char in pinyin)

def insert_co_user_play_dtl_data(battleSituation, userName, aiNo, idiom, shouPin, weiPin, sort):
    current_time = datetime.datetime.now()
    co_user_info_data = {
        'BATTLE_SITUATION': battleSituation,
        'USER_NAME': userName,
        'AI_NO': aiNo,
        'IDIOM': idiom,
        'SHOU_PIN': shouPin,
        'WEI_PIN': weiPin,
        'SORT': sort,
        'REMARK': None,
        'INST_TIME': current_time,
        'INST_USER_NO': 'sys',
        'UPDT_TIME': None,
        'UPDT_USER_NO': None
    }
    return co_user_info_data
def insert_co_ai_play_dtl_data(battleSituation, userName, aiNo, idiom, shouPin, weiPin, sort):
    current_time = datetime.datetime.now()
    co_ai_info_data = {
        'BATTLE_SITUATION': battleSituation,
        'AI_NO': aiNo,
        'USER_NAME': userName,
        'IDIOM': idiom,
        'SHOU_PIN': shouPin,
        'WEI_PIN': weiPin,
        'SORT': sort,
        'REMARK': None,
        'INST_TIME': current_time,
        'INST_USER_NO': 'sys',
        'UPDT_TIME': None,
        'UPDT_USER_NO': None
    }
    return co_ai_info_data
def insert_co_user_play_record_data(userName, aiNo, battleSituation, first_play, startTime, endTime, totalTime,
                                    difficultyLevel, totalIdioms, score):
    current_time = datetime.datetime.now()
    co_ai_info_data = {
        'USER_NAME': userName,
        'AI_NO': aiNo,
        'BATTLE_SITUATION': battleSituation,
        'FIRST_PLAY': first_play,
        'START_TIME': startTime,
        'END_TIME': endTime,
        'TOTAL_TIME': totalTime,
        'DIFFICULTY_LEVEL': difficultyLevel,
        'TOTAL_IDIOMS': totalIdioms,
        'SCORE': score,
        'REMARK': None,
        'INST_TIME': current_time,
        'INST_USER_NO': 'sys',
        'UPDT_TIME': None,
        'UPDT_USER_NO': None
    }
    return co_ai_info_data

# 读取成语数据
with open('D:\Download\Idiom_Solitaire\chinese-xinhua-master\data\idiom.json', 'r', encoding='UTF-8') as idiom:
    idioms = json.load(idiom)
    idioms_df = pd.DataFrame(idioms)
    idioms_df['pinyin_no_tone'] = idioms_df['pinyin'].apply(remove_tone)
    idioms_df['shoupin'] = idioms_df['pinyin_no_tone'].str.split().str[0]
    idioms_df['weipin'] = idioms_df['pinyin_no_tone'].str.split().str[-1]
    idioms_df.set_index("word", inplace=True)

# 检查成语是否有效
def is_valid_idiom(idiom, last_char=None):
    if idiom not in idioms_df.index:
        return False, "成语不存在！"
    if last_char and idioms_df.loc[idiom, 'shoupin'] != last_char:
        return False, f"成语必须以 '{last_char}' 开头！"
    return True, ""

# 生成下一个成语
def generate_next_idiom(last_char):
    possible_idioms = idioms_df[idioms_df['shoupin'] == last_char].index
    if not possible_idioms.empty:
        return random.choice(possible_idioms)
    return None

# 游戏逻辑
def play_game(user_input):
    userName = session['username']
    # print('username=', userName)
    if 'used_idioms' not in session:
        session['used_idioms'] = []
    if 'last_char' not in session:
        session['last_char'] = None

    # 检查用户输入的成语是否有效
    is_valid, message = is_valid_idiom(user_input, session.get('last_char'))
    if not is_valid:
        return False, message

    # 记录用户输入的成语
    session['used_idioms'].append(user_input)
    session['last_char'] = idioms_df.loc[user_input, 'weipin']
    user_weipin = idioms_df.loc[user_input, 'weipin']
    user_shoupin = idioms_df.loc[user_input, 'shoupin']
    idiom_count = len(session['used_idioms'])
    insert_user_data = insert_co_user_play_dtl_data(session['Situation'], userName, session['aiNo'], user_input,
                                                    user_shoupin, user_weipin, idiom_count)
    connect_mysql.connect_sql_insert('co_user_play_dtl', insert_user_data)

    # AI 接龙
    next_idiom = generate_next_idiom(session['last_char'])
    # print('AI 接成语：',next_idiom)
    if not next_idiom:
        return True, "你赢了！AI 无法接出成语。"

    # 记录 AI 的成语
    session['used_idioms'].append(next_idiom)
    session['last_char'] = idioms_df.loc[next_idiom, 'weipin']
    ai_weipin = idioms_df.loc[next_idiom, 'weipin']
    ai_shoupin = idioms_df.loc[next_idiom, 'shoupin']
    idiom_count = len(session['used_idioms'])
    insert_ai_data = insert_co_ai_play_dtl_data(session['Situation'], userName, session['aiNo'], next_idiom, ai_shoupin,
                                                ai_weipin, idiom_count)
    connect_mysql.connect_sql_insert('co_ai_play_dtl', insert_ai_data)
    return False, f"AI 接龙：{next_idiom}"

@app.route('/favicon.ico')
def favicon():
    return '', 204  # 返回 no content

# 路由
@app.route('/UserFirst')
def UserFirst():
    if 'aiNo' not in session:
        # 生成新的游戏参数
        session['aiNo'] = random.randint(1, 999999)

    # print('aiNo=', session['aiNo'])
    session['Situation'] = random.randint(1, 999999)

    # 确保Situation唯一
    conn = connect_mysql.create_connection()
    Situation_db = connect_mysql.select_one_column_data(conn, 'co_ai_play_dtl', 'BATTLE_SITUATION')
    while session['Situation'] in Situation_db:
        session['Situation'] = random.randint(1, 9999)

    # 初始化游戏状态
    userName = session['username']
    session['used_idioms'] = []  # 初始化used_idioms
    session['last_char'] = None  # 初始化last_char

    return render_template('user_first_play.html')

@app.route('/UserFirstPlay', methods=['POST'])
def UserFirstPlay():
    user_input = request.form.get('user_input')
    # print('user_input=', user_input)
    if user_input.lower() == 'q':
        # 确保立即提交所有数据库操作
        conn = connect_mysql.create_connection()
        conn.commit()  # 显式提交
        used_idioms = session.get('used_idioms', [])
        finish_time = datetime.datetime.now()
        print('finish_time=', finish_time)
        # session.clear()
        print("游戏结束，使用的成语：", session.get('used_idioms', []))  # 调试信息

        # 记录用户与AI的时长和输赢
        user_idiom_count = connect_mysql.select_idiom_count(conn, 'co_user_play_dtl', 'BATTLE_SITUATION',
                                                            session['Situation'])
        ai_idiom_count = connect_mysql.select_idiom_count(conn, 'co_ai_play_dtl', 'BATTLE_SITUATION',
                                                          session['Situation'])
        if not isinstance(ai_idiom_count, (int, float)):
            ai_idiom_count = 0
        idiom_count = user_idiom_count + ai_idiom_count
        # print('idiom_count=', idiom_count)

        start_time = connect_mysql.select_two_conditions(conn, 'co_user_play_dtl', 'inst_time', 'BATTLE_SITUATION',
                                                         session['Situation'], 'SORT', '1')
        # print('start_time=', start_time)
        if ai_idiom_count >= user_idiom_count:
            winner = 'AI'
            end = finish_time
        else:
            winner = 'USER'
            end_time = connect_mysql.select_two_conditions(conn, 'co_user_play_dtl', 'inst_time', 'BATTLE_SITUATION',
                                                           session['Situation'], 'SORT', idiom_count)
            end = end_time[0][0]
        print('winner=', winner)

        start = start_time[0][0]

        # print('start=', start)
        # print('end=', end)

        # 计算时间差
        time_diff = end - start
        # print('time_diff=', time_diff)

        userName = session['username']

        insert_record_data = insert_co_user_play_record_data(userName, session['aiNo'], session['Situation'], 'user',
                                                             start, end, time_diff, 'easy', idiom_count, winner)
        connect_mysql.connect_sql_insert('co_user_play_record', insert_record_data)

        # 清空特定的 session 数据
        session.pop('used_idioms', None)  # 移除 used_idioms
        # print('移除session')
        session.pop('last_char', None)  # 移除 last_char
        session.pop('initial_ai_idiom', None)  # 移除 initial_ai_idiom
        session.pop('aiNo', None)  # 移除 aiNo
        session.pop('Situation', None)  # 移除 Situation

        # 返回 JSON 响应，指示前端跳转
        return jsonify({
            "status": "game_over",
            "message": "游戏结束！",
            "used_idioms": used_idioms,  # 传递本局所有成语
            "redirect_urls": {
                "exit": url_for('home'),  # 退出游戏路由
                "records": url_for('gameRecords')  # 历史战绩路由
            }
        })

        # 正常游戏逻辑
    game_over, message = play_game(user_input)
    return jsonify({
        "status": "playing",
        "message": message,
        "game_over": game_over,
        "used_idioms": session.get('used_idioms', [])
    })

@app.route('/gameRecords', methods=['GET', 'POST'])
def gameRecords():
    return render_template('game_records.html')

if __name__ == '__main__':
    app.debug = True
    app.run()

    # 同一局域网下，可在手机上查看
    # app.run(host='0.0.0.0', port=5000, debug=True)



