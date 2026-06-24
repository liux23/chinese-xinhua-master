
import json
import pandas as pd
import numpy as np
import time

def remove_tone(pinyin):
    tone_map = {"ā": "a", "á": "a", "ǎ": "a", "à": "a",
                "ē": "e", "é": "e", "ě": "e", "è": "e",
                "ī": "i", "í": "i", "ǐ": "i", "ì": "i",
                "ō": "o", "ó": "o", "ǒ": "o", "ò": "o",
                "ū": "u", "ú": "u", "ǔ": "u", "ù": "u"}
    for k, v in tone_map.items():
        pinyin = pinyin.replace(k, v)
    return pinyin

def play(idiom_json):
    with open(idiom_json, 'r', encoding='UTF-8') as idiom:
        chengyu = json.load(idiom)
        chengyu_1 = pd.DataFrame(chengyu)
        chengyu_1['pinyin_no_tone'] = chengyu_1['pinyin'].apply(remove_tone)
        chengyu_1['shoupin'] = chengyu_1['pinyin_no_tone'].str.split().str[0]
        chengyu_1['weipin'] = chengyu_1['pinyin_no_tone'].str.split().str[-1]
        # print(chengyu_1['pinyin_no_tone'])
        chengyu_1 =chengyu_1.set_index("word")[["shoupin", "weipin"]]
        start = time.time()
        dialog_ai = []
        dialog_player = []
        is_head = input("是否先手(输入N/n表示后手，其他表示先手)：")
        if is_head == 'N' or is_head == 'n':
            word2 = np.random.choice(chengyu_1.index)
            dialog_ai.append(word2)
            print(word2)
            weipin = chengyu_1.loc[word2, "weipin"]
        else:
            weipin=''
        while True:
            word = input("请输入一个成语（认输或离开请按Q/q）：")
            if word == "Q" or word == "q":
                print("你离开了游戏，再见！！！")
                break
            if word == "不会" or word == "你来":
                answer = chengyu_1.index[chengyu_1["shoupin"] == chengyu_1.loc[word2, "weipin"]]
                word = np.random.choice(answer)
                dialog_player.append(word)
                print(word)
                words = chengyu_1.index[chengyu_1["shoupin"] == chengyu_1.loc[word, "weipin"]]
                word2 = np.random.choice(words)
                dialog_ai.append(word2)
                print(word2)
                weipin = chengyu_1.loc[word2, "weipin"]
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
        print(f"游戏进行时长:{end-start}秒")
        min_dialog = min(len(dialog_ai), len(dialog_player))
        # print("dialog_ai=", dialog_ai)
        # print("dialog_player=", dialog_player)
        # print("max_dialog =", min_dialog)
        print("游戏回顾：")
        for i in range(min_dialog):
            if is_head == 'N' or is_head == 'n':
                print(f"{dialog_ai[i]}->{dialog_player[i]}->", end="")
            else:
                print(f"{dialog_player[i]}->{dialog_ai[i]}->", end="")
        last_index = min_dialog - 1
        if is_head == 'N' or is_head == 'n':
            if dialog_ai[last_index] == dialog_ai[-1]:
                print("结束")
            else:
                print(f"{dialog_ai[-1]}->结束")
        else:
            if dialog_player[last_index] == dialog_player[-1]:
                print("结束")
            else:
                print(f"{dialog_player[-1]}->结束")

if __name__ == '__main__':
    play("D:\Download\Idiom_Solitaire\chinese-xinhua-master\data\idiom.json")
    # play("chengyu.json")