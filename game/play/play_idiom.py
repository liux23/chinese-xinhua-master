import json
import pandas as pd
import numpy as np
import time
import math
import flask

class play_idiom:

    def __init__(self):
        self.dialog_ai = []
        self.dialog_player = []
        self.min_dialog = 0
        self.is_head = ''
        self.duration_threshold = 0
        self.TIMEOUT = 60

    def remove_tone(self, pinyin):
        tone_map = {"ā": "a", "á": "a", "ǎ": "a", "à": "a",
                    "ē": "e", "é": "e", "ě": "e", "è": "e",
                    "ī": "i", "í": "i", "ǐ": "i", "ì": "i",
                    "ō": "o", "ó": "o", "ǒ": "o", "ò": "o",
                    "ū": "u", "ú": "u", "ǔ": "u", "ù": "u"}
        for k, v in tone_map.items():
            pinyin = pinyin.replace(k, v)
        return pinyin

    def time_input(self, duration_time, max_duration, text, content):
        start = time.time()
        word = input(text)
        end = time.time()
        duration = math.ceil(end - start)
        if duration_time < duration < max_duration:
            print(content)
        if duration > max_duration:
            print("你太久没回我消息，我还以为你不玩儿了呢。。。")
            exit()
        return word, duration

    def set_timeout(self, seconds):
        self.TIMEOUT = seconds
        return self.TIMEOUT

    def print_two_idiom(self, dialog_ai, dialog_player, chengyu, word):
        dialog_player.append(word)
        print(word)
        words = chengyu.index[chengyu["shoupin"] == chengyu.loc[word, "weipin"]]
        word2 = np.random.choice(words)
        dialog_ai.append(word2)
        print(word2)
        weipin = chengyu.loc[word2, "weipin"]
        return weipin, dialog_ai, dialog_player, word2

    def play(self, idiom_json):
        with open(idiom_json, 'r', encoding='UTF-8') as idiom:
            chengyu = json.load(idiom)
            chengyu_1 = pd.DataFrame(chengyu)
            chengyu_1['pinyin_no_tone'] = chengyu_1['pinyin'].apply(self.remove_tone)
            chengyu_1['shoupin'] = chengyu_1['pinyin_no_tone'].str.split().str[0]
            chengyu_1['weipin'] = chengyu_1['pinyin_no_tone'].str.split().str[-1]
            # print(chengyu_1['pinyin_no_tone'])
            chengyu_1 = chengyu_1.set_index("word")[["shoupin", "weipin"]]
            start = time.time()
            dialog_ai = []
            dialog_player = []
            word_all = ''
            self.set_timeout(10)
            # print("TIMEOUT =", self.TIMEOUT)
            self.is_head = input("是否先手(输入N/n表示后手，其他表示先手)：")
            end_time = time.time()
            duration_time = end_time - start
            if duration_time > self.TIMEOUT:
                print("你太久没回我消息，我还以为你不玩儿了呢。。。")
                exit()
            if self.is_head.lower() == 'n':
                word2 = np.random.choice(chengyu_1.index)
                dialog_ai.append(word2)
                print(word2)
                weipin = chengyu_1.loc[word2, "weipin"]
            else:
                weipin = ''
            while True:
                word, duration_1 = self.time_input(60, 100, "请输入一个成语（认输或离开请按Q/q）：", "（o_o) 等你等得花儿都谢了")
                # print("duration_1 =", duration_1)
                if word.lower() == "q":
                    print("你离开了游戏，再见！！！")
                    break
                if word == "提示" or word == "提示一下":
                    answer = chengyu_1.index[chengyu_1["shoupin"] == chengyu_1.loc[word2, "weipin"]]
                    word_all = np.random.choice(answer)
                    word_2 = word_all[:2]
                    print(word_2)
                    continue
                if word == "再提示一下":
                    print('长度', len(word_all))
                    if word_all == '':
                        answer = chengyu_1.index[chengyu_1["shoupin"] == chengyu_1.loc[word2, "weipin"]]
                        word = np.random.choice(answer)
                        weipin, dialog_ai, dialog_player, word2 = self.print_two_idiom(dialog_ai, dialog_player,
                                                                                       chengyu_1, word)
                    else:
                        if len(word_2) != '':
                            word_3 = word_all[:3]
                            print(word_3)
                            word, duration_1 = self.time_input(60, 100, "请输入一个成语（认输或离开请按Q/q）：",
                                                                    "（o_o) 等你等得花儿都谢了")
                        word_2 = ''
                        if len(word_3) != '':
                            word = word_all
                        weipin, dialog_ai, dialog_player, word2 = self.print_two_idiom(dialog_ai, dialog_player,
                                                                                           chengyu_1, word)
                        word_3 = ''
                        word_all = ''
                    continue
                if word == "不知道":
                    if word_all == '':
                        answer = chengyu_1.index[chengyu_1["shoupin"] == chengyu_1.loc[word2, "weipin"]]
                        word = np.random.choice(answer)
                    else:
                        word = word_all
                    weipin, dialog_ai, dialog_player, word2 = self.print_two_idiom(dialog_ai, dialog_player,
                                                                                       chengyu_1, word)
                    word_all = ''
                    continue
                if word == "不会" or word == "你来":
                    answer = chengyu_1.index[chengyu_1["shoupin"] == chengyu_1.loc[word2, "weipin"]]
                    word = np.random.choice(answer)
                    weipin, dialog_ai, dialog_player, word2 = self.print_two_idiom(dialog_ai, dialog_player,
                                                                                   chengyu_1, word)
                    # print("weipin = ", weipin)
                    continue

                if word not in chengyu_1.index:
                    print("你输入的不是一个成语，请重新输入！")
                    continue
                if weipin and chengyu_1.loc[word, "shoupin"] != weipin:
                    print("你输入的成语并不能与机器人出的成语接上来，你输了，游戏结束！！！")
                    break
                words = chengyu_1.index[chengyu_1["shoupin"] == chengyu_1.loc[word, "weipin"]]
                dialog_player.append(word)
                # print("words =", words)
                if words.shape[0] == 0:
                    print("恭喜你赢了！成语机器人已经被你打败！！！")
                    break

                word2 = np.random.choice(words)
                dialog_ai.append(word2)
                print(word2)
                weipin = chengyu_1.loc[word2, "weipin"]
                # print("weipin = ", weipin)
            end = time.time()
            duration = end - start
            duration = math.ceil(duration)
            print(f"游戏进行时长:{duration}秒")
            self.min_dialog = min(len(dialog_ai), len(dialog_player))
            self.dialog_ai = dialog_ai
            self.dialog_player = dialog_player
            # print("dialog_ai=", dialog_ai)
            # print("dialog_player=", dialog_player)
            # print("min_dialog =", min_dialog)

    def print_game(self):
        # print(self.dialog_ai)
        # print(self.dialog_player)
        if self.min_dialog == 0:
            exit()
        else:
            print("游戏回顾：")
            for i in range(self.min_dialog):
                if self.is_head == 'N' or self.is_head == 'n':
                    print(f"{self.dialog_ai[i]}->{self.dialog_player[i]}->", end="")
                else:
                    print(f"{self.dialog_player[i]}->{self.dialog_ai[i]}->", end="")
            last_index = self.min_dialog - 1
            if self.is_head == 'N' or self.is_head == 'n':
                if self.dialog_ai[last_index] == self.dialog_ai[-1]:
                    print("结束")
                else:
                    print(f"{self.dialog_ai[-1]}->结束")
            else:
                if self.dialog_player[last_index] == self.dialog_player[-1]:
                    print("结束")
                else:
                    print(f"{self.dialog_player[-1]}->结束")


if __name__ == '__main__':
    game = play_idiom()
    game.play("D:\Download\Idiom_Solitaire\chinese-xinhua-master\data\idiom.json")
    game.print_game()