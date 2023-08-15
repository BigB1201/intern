# %%

import json
import requests
import re as regex
import matplotlib.pyplot as plt
import seaborn.colors # Required to use the Flare palette.
from numpy import arange, array, linspace
from matplotlib import colormaps as palettes
from matplotlib.colors import ListedColormap

initials = ['ng', 'gw', 'kw', 'b', 'p', 'm', 'f', 'd', 't', 'n', 'l', 'g', 'k', 'h', 'z', 'c', 's', 'j', 'w']
finals = ['aang','oeng','aai','aau','aam','aan','aap','aat','aak','ang','eng','ing','ong','ung','eoi','eon','eot','oet','oek','yun','yut','aa','ai','au','am','an','ap','at','ak','ei','eu','em','ep','ek','iu','im','in','ip','it','ik','oi','ou','on','ot','ok','oe','ui','un','ut','uk','yu','a','e','i','o','u','m','ng']
tones = ['1','2','3','4','5','6']

def flatmap(f, xs):
    return [y for ys in xs for y in f(ys)]
def tokenize(strings: list[str]):
    return flatmap(lambda str: regex.findall(r"\w+", str), strings)

class Bag:
    def __init__(self, dict):
        self.dict = dict # Hashmap of type Any -> Int
    def add(self, key):
        self.dict.update({key: self.count(key) + 1})
    def count(self, key):
        g = self.dict.get(key)
        if g != None : return g
        else: return 0

class Jyutping:
    rxi = f'({"|".join(initials)})'
    rxf = f'({"|".join(finals)})'

    cmap = palettes["flare_r"]
    newcolors = cmap(linspace(0, 1, 256))
    newcolors[0] = array([0,0,0,1])
    cmap = ListedColormap(newcolors)

    def separate(jyutping: str):
        if regex.match(f"{Jyutping.rxi}?{Jyutping.rxf}[1-6]$", jyutping) is None:
            return False, None, None, None

        initial = regex.search(Jyutping.rxi, jyutping)
        if initial != None: initial = initial.group() 
        else: initial = ''
        remainder = jyutping[len(initial):]
        final = regex.search(Jyutping.rxf, remainder)
        if final != None: final = final.group()
        tone = jyutping[-1]

        if final in ['ng', 'm'] and initial != None: return False, initial, final, tone # Special logic to stop ngng

        if final == None and initial != None: final = initial; initial = ''
        return True, initial, final, tone
    def into_pieces(jyutpings: list[str]):
        initialsDict = Bag({ w:0 for w in initials })
        finalsDict = Bag({ w:0 for w in finals })
        tonesDict = Bag({ w:0 for w in tones })

        for jyutping in tokenize(jyutpings):
            comprehensible, initial, final, tone = Jyutping.separate(jyutping)
            if not comprehensible: continue
            if initial != '': initialsDict.add(initial)
            finalsDict.add(final)
            tonesDict.add(tone)
        
        return { "Initials": initialsDict.dict, "Finals": finalsDict.dict, "Tones": tonesDict.dict }
    def heatmap(pieces, key: str):
        
        lower_key = key.lower()
        labels = globals()[lower_key]
        data = array([[x] for x in ji.get(key).values()])

        fig, ax = plt.subplots()
        fig.set_figheight(16)
        fig.set_figwidth(1)
        im = ax.imshow(data, cmap = Jyutping.cmap, vmin = 0, vmax = 50)

        # Show all ticks and label them with the respective list entries
        ax.set_xticks(arange(1), labels=[''])
        ax.set_yticks(arange(len(labels)), labels=labels)

        # Rotate the tick labels and set their alignment.
        plt.setp(ax.get_xticklabels(), rotation=45, ha="right",
                rotation_mode="anchor")

        # Loop over data dimensions and create text annotations.
        for i in range(len(labels)):
            text = ax.text(0, i, data[i, 0],
                            ha="center", va="center", color="w")

        # ax.set_title(f"Instances of {lower_key} in track")
        fig.tight_layout()
        plt.show()

# %%
longthing = ['haa6 sing1-kei4 heoi3 tai2 hei3 laa1',
 'teng1 jat6 tung4 baan1 pang4-jau5 joek3 heoi3 daa2 laam4 kau4',
 'cam4 jat6 ngo5 tung4 ngo5 baa1 maa1 heoi3 jam2 caa4',
 'ho2 m4 ho2-ji5 bong1 ngo5 ling1 ngo5 din6-waa2 gwo3 lei4',
 'hok6-haau6 jiu3 ngo5 maai5 bou6 din6-nou5',
 'gan6 lei4 jau5 me1 je5 wut6-dung6 hou2-waan2',
 'ne1 go3 hap6 hai6 zong1 me1 je5 gaa3 ？',
 'ji1 gin6 zan2 hou2 leng3 wo3',
 'waa1 ，gam1-jat6 zoek6 dou3 gam3 jing4',
 'ji1 bun2 syu1 hou2 m4 hou2 tai2 gaa3 ？']# %%

ji = Jyutping.into_pieces(longthing)

Jyutping.heatmap(ji, "Initials")
Jyutping.heatmap(ji, "Finals")
Jyutping.heatmap(ji, "Tones")

# %%


sentence = '''依條友咁怪嘅
今日同我朋友去逛街
好多囷喎依排
識唔識拍波咖
啲花草樹木好綠油油
下星期去睇戲啦
聽日同班朋友約去打籃球
尋日我同我爸媽去飲茶
可唔可以幫我拎我電話過梩
學校要我買部電腦
近離有咩嘢活動好玩
呢個盒係裝咩嘢㗎？
依件袗好靚喎
嘩，今日着到咁型
依本書好唔好睇㗎？
我唔記得左我鑰匙
我食左好多野啦， 好飽
我好鐘意食橙
我更鐘意食蘋果
我亦都好鐘意唱歌
我阿媽教我偷野係唔好
星期六我有一個補習堂
我每晚會摖牙
星期五我有一個測試
我最鐘意春天
我阿媽會聽日出街買褲
我全部錢都被人偷左
我頭出血
垃圾掉左啦
你雪糕被我舐， 得唔得
我手指夾左， 好疼
石頭好重
我好鐘意玩劍擊
你手有個貼紙
遊戲結束
你功課要做改正
呢個雞好乾
我要水去解渴
我無靴喔
我背好疼
依個野食好苦喔
我好悶， 你有無建議我可以做咩以加
茶定係咖啡
你有無忌廉
你邊度嚟㗎？
好開心識到你
各位先生女士，晚安
我好眼份
你可唔可以做我功課
'''

response = requests.post(
    'https://2fmwbbau5i.execute-api.ap-east-1.amazonaws.com/Prod/convertTextToJyutping',
    headers={'Content-Type': 'application/json'},
    data=json.dumps({'SentenceList': sentence})
)
longthing = json.loads(response.text)['data']
ji = Jyutping.into_pieces([longthing])

Jyutping.heatmap(ji, "Initials")
Jyutping.heatmap(ji, "Finals")
Jyutping.heatmap(ji, "Tones")

# %%
def jsep(jyutping):
    return Jyutping.separate(jyutping)
    # else: return f"{jyutping} is not comprehensible"
print(jsep("kwyun1"))
print(jsep("diu2"))
print(jsep("prince3"))
print(jsep("ngng4"))
print(jsep("cm5"))
print(jsep("wong6"))
# %%
