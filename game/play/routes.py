
from flask import Flask
from game.play.battle_page import battle
from game.play.choose import choose, submit
from game.play.game_records import gameRecords, get_idioms
from game.play.user_first_play import UserFirstPlay, UserFirst
from game.play.AI_first_play import AIFirstPlay, AIFirst, stop_redis, get_countdown, reset_countdown, timeout_save

def register_routes(app: Flask):
    # 注册路由
    app.add_url_rule('/UserFirstPlay', view_func=UserFirstPlay, methods=['POST'])
    app.add_url_rule('/AIFirst', view_func=AIFirst, methods=['GET', 'POST'])
    app.add_url_rule('/AIFirstPlay', view_func=AIFirstPlay, methods=['POST'])
    app.add_url_rule('/choose', view_func=choose, methods=['POST'])
    app.add_url_rule('/battle', view_func=battle, methods=['POST'])
    app.add_url_rule('/UserFirst', view_func=UserFirst, methods=['POST'])
    app.add_url_rule('/submit', view_func=submit, methods=['POST'])
    app.add_url_rule('/stop_redis', view_func=stop_redis, methods=['POST', 'GET'])
    app.add_url_rule('/gameRecords', view_func=gameRecords, methods=['GET', 'POST'])
    app.add_url_rule('/get_idioms/<game_id>', view_func=get_idioms, methods=['GET'])
    app.add_url_rule('/get_countdown', view_func=get_countdown, methods=['GET'])
    app.add_url_rule('/reset_countdown', view_func=reset_countdown, methods=['POST'])
    app.add_url_rule('/timeout_save', view_func=timeout_save, methods=['POST'])

    # 打印注册的路由用于调试
    print('=== 已注册路由 ===')
    for rule in app.url_map.iter_rules():
        print(f'  {rule.methods}  {rule.rule}')
    print('==================')