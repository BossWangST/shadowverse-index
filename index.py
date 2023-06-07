from hoshino import Service
from hoshino.typing import CQEvent
from PIL import Image, ImageDraw,ImageFont
import os,json
from os.path import join
import zhconv
from textwrap import fill
from io import BytesIO
import base64
import re
from fuzzywuzzy import fuzz
import traceback
sv_help = '''
wait to complete
'''
MOUDULE_PATH = os.path.dirname(__file__)
sv=Service('影之诗卡牌图鉴',help_=sv_help)
clan_color = {0:(220,220,220),#职业代表色，随便填的
              1:(0,128,0),
              2:(238,232,170),
              3:(25,25,112),
              4:(205,133,63),
              5:(147,112,219),
              6:(220,20,60),
              7:(255,250,250),
              8:(70,130,180)}
clan2w = {#职业编号
    0:"中立",
    1:"精靈",
    2:"皇家護衛",
    3:"巫師",
    4:"龍族",
    5:"死靈法師",
    6:"吸血鬼",
    7:"主教",
    8:"復仇者"
}
tribe_name =["指揮官","士兵","土之印","馬納利亞","創造物","財寶","機械","雷維翁","自然","宴樂","英雄","武裝","西洋棋","八獄","學園","全部"]#类型
card_set = {#卡包名
    10000:"基本卡",
    10001:"經典卡包",
    10002:"暗影進化",
    10003:"巴哈姆特降臨",
    10004:"諸神狂嵐",
    10005:"夢境奇想",
    10006:"星神傳說",
    10007:"時空轉生",
    10008:"起源之光‧終焉之闇",
    10009:"蒼空騎翔",
    10010:"滅禍十傑",
    10011:"扭曲次元",
    10012:"鋼鐵的反叛者",
    10013:"榮耀再臨",
    10014:"森羅咆哮",
    10015:"極鬥之巔",
    10016:"那塔拉的崩壞",
    10017:"命運諸神",
    10018:"勒比盧的旋風",
    10019:"十天覺醒",
    10020:"暗黑的威爾薩",
    10021:"物語重歸",
    10022:"超越災禍者",
    10023:"十禍鬥爭",
    10024:"天象樂土",
    10025:"極天龍鳴",
    10026:"示天龍劍",
    10027:"八獄魔境‧阿茲弗特",
    10028:"遙久學園",
    70001:"主題牌組 第1彈",
    70002:"主題牌組 第2彈",
    70003:"Anigera合作",
    70004:"劇場版Fate[HF]合作",
    70005:"主題牌組 第4彈",
    70006:"主題牌組 第5彈",
    70008:"超異域公主連結！Re:Dive合作",
    70009:"一拳超人合作",
    70010:"Re：從零開始的異世界生活合作",
    70011:"主題牌組 第6彈",
    70012:"Love Live! 學園偶像祭合作",
    70013:"涼宮春日的憂鬱合作",
    70014:"主題牌組 第7彈",
    70016:"尼爾：自動人形合作",
    70017:"CODE GEASS 反叛的魯路修合作",
    70018:"闇影詩章‧霸者之戰合作",
    70019:"闇影詩章‧霸者之戰套組",
    70020:"碧藍幻想合作",
    70021:"對戰通行證",
    70022:"輝夜姬想讓人告白？合作",
    70023:"偶像大師 灰姑娘女孩合作",
    70024:"通靈王合作",
    70025:"賽馬娘Pretty Derby合作",
    70026:"吉伊卡哇合作",
    70027:"闇影詩章F合作",
    20001:"初音未來合作",
    90000:"token"
}
text_color = (255,255,255)#文字颜色
def text_split(text):#文字排版
    t_list = text.replace("<br>","\n").split("\n")
    t_list = [fill(i,width=30) for i in t_list]
    text = '\n'.join(t_list)
    return text
def draw_rr(x,y,clan):#绘制圆角矩形
    square = Image.new("RGBA",(x+6,y+6),(255,255,255,0))
    draw = ImageDraw.Draw(square)
    draw.rounded_rectangle((3,3,x-3,y-3),15,(15,15,20),clan_color[clan],3)
    return(square)

font = ImageFont.truetype(join(MOUDULE_PATH,'font/font.ttc'),size = 30)
def fo_cardinfo_gen(card):#绘制随从卡
    skill = "进化前\n" + text_split(card["skill_disc"])
    eskill = "进化后\n" + text_split(card["evo_skill_disc"])
    des = text_split(card["description"])
    edes = text_split(card["evo_description"])
    cv = 'cv:' + card["cv"]
    card_info = '卡包:' + card_set[card["card_set_id"]] + '|類型:' + card["tribe_name"] + '|职业:' + clan2w[card["clan"]]
    y1 = font.getsize_multiline(des)[1]
    y2 = font.getsize_multiline(edes)[1]
    y3 = font.getsize_multiline(skill)[1]
    y4 = font.getsize_multiline(eskill)[1]
    xcv = font.getsize_multiline(cv)[0]
    id = card["card_id"]
    #绘制左侧
    left = Image.new("RGBA",(1100,810+y1+y2),(255,255,255,0))
    C_pic = Image.open(join(MOUDULE_PATH,f'pic/C_{id}.png'))
    E_pic = Image.open(join(MOUDULE_PATH,f'pic/E_{id}.png'))
    left.paste(C_pic,(0,0),C_pic)
    left.paste(E_pic,(560,0),E_pic)
    C_pic.close()
    E_pic.close()
    square = draw_rr(1100,90+y1+y2,card["clan"])
    left.paste(square,(0,720),square)
    square.close()
    ldraw = ImageDraw.Draw(left)
    ldraw.text((50,740),des,text_color,font)
    ldraw.text((50,790+y1),edes,text_color,font)
    ldraw.line([(45,765+y1),(1055,765+y1)],text_color,1)
    ldraw.text((1050-xcv,770+y1+y2),cv,text_color,font)
    #绘制右侧
    right = Image.new("RGBA",(1000,550+y3+y4),(255,255,255,0))
    square = draw_rr(1000,120,card["clan"])
    right.paste(square,(0,0),square)
    square.close()
    rdraw = ImageDraw.Draw(right)
    rdraw.text((500,30),card["card_name"],text_color,font,'mm')
    rdraw.line([(45,55),(955,55)],text_color,1)
    rdraw.text((500,75),card_info,text_color,font,'mm')
    square = draw_rr(1000,310+y3+y4,card["clan"])
    right.paste(square,(0,140),square)
    square.close()
    rdraw.text((50,240),skill,text_color,font)
    rdraw.text((50,350+y3),eskill,text_color,font)
    rdraw.line([(45,295+y3),(955,295+y3)],text_color,1)
    bg = Image.open(join(MOUDULE_PATH,'bg/bg.jpg'))
    bg.paste(left,(30,30),left)
    bg.paste(right,(1170,30),right)
    ym = max(810+y1+y2,550+y3+y4)
    bg = bg.crop((0,0,2200,ym+80))
    bgdraw = ImageDraw.Draw(bg)
    x,y = bg.size
    bgdraw.text((x-300,y-90),f'id:{id}\ncode by 夏绪\ngenerat by ddbot',text_color,font)
    return bg
def ma_cardinfo_gen(card):#绘制法术/护符卡
    skill = text_split(card["skill_disc"])
    des = text_split(card["description"])
    cv = 'cv:' + card["cv"]
    card_info = '卡包:' + card_set[card["card_set_id"]] + '|類型:' + card["tribe_name"] + '|职业:' + clan2w[card["clan"]]
    y1 = font.getsize_multiline(skill)[1]
    y2 = font.getsize_multiline(des)[1]
    xcv = font.getsize_multiline(cv)[0]
    id = card["card_id"]
    #绘制左侧
    left = Image.new("RGBA",(540,700),(255,255,255,0))
    C_pic = Image.open(join(MOUDULE_PATH,f'pic/C_{id}.png'))
    left.paste(C_pic,(0,0),C_pic)
    C_pic.close()
    #绘制右侧
    right = Image.new("RGBA",(1000,350+y1+y2),(255,255,255,0))
    square = draw_rr(1000,120,card["clan"])
    right.paste(square,(0,0),square)
    square.close()
    rdraw = ImageDraw.Draw(right)
    rdraw.text((500,30),card["card_name"],text_color,font,'mm')
    rdraw.line([(45,55),(955,55)],text_color,1)
    rdraw.text((500,75),card_info,text_color,font,'mm')
    square = draw_rr(1000,210+y1+y2,card["clan"])
    right.paste(square,(0,140),square)
    square.close()
    rdraw.text((50,190),skill,text_color,font)
    rdraw.text((50,300+y1),des,text_color,font)    
    rdraw.text((950-xcv,510+y1+y2),cv,text_color,font)
    rdraw.line([(45,245+y1),(955,245+y1)],text_color,1)
    bg = Image.open(join(MOUDULE_PATH,'bg/bg2.jpg'))
    bg.paste(left,(30,30),left)
    bg.paste(right,(610,30),right)
    ym = max(700,350+y1+y2)
    bg = bg.crop((0,0,1640,ym+30))
    bgdraw = ImageDraw.Draw(bg)
    x,y = bg.size
    bgdraw.text((x-300,y-90),f'id:{id}\ncode by 夏绪\ngenerat by ddbot',text_color,font)
    return bg

def check_cond(cond):
    with open(join(MOUDULE_PATH,'condition.json'),'r', encoding='UTF-8') as f:
        c = json.load(f)
    for i in c:
        for j in c[i]:
            if cond in c[i][j]:
                break
        if cond in c[i][j]:
                break
    return (i,int(j))

async def cardinfo_gen(card):#生成卡牌信息card:dict,直接返回cq码
    if card["char_type"] == 1:
        img = fo_cardinfo_gen(card)
    else:
        img = ma_cardinfo_gen(card)
    img = img.convert('RGB')
    buf = BytesIO()
    img.save(buf, format='JPEG')
    base64_str = f'base64://{base64.b64encode(buf.getvalue()).decode()}'
    img = f'[CQ:image,file={base64_str}]'
    return img

async def selectlist(cards):#生成待选列表图cards:list，直接返回cq码
    img = Image.open(join(MOUDULE_PATH,'bg/bg3.png'))
    card_num = len(cards)
    line = card_num//4
    if card_num % 4 ==0:
        line -= 1
    draw = ImageDraw.Draw(img)
    count = 0
    for i in range(0,line+1):
        for j in range(0,4):
            if j+i*4 == card_num:
                break
            card = cards[j+i*4]['card']
            dm = cards[j+i*4]['dm']
            id = card['card_id']
            name = card['card_name']
            text = f'id:{id}|匹配度:{dm}'
            C_img = Image.open(join(MOUDULE_PATH,f'pic/C_{id}.png'))
            img.paste(C_img,(30+j*570,30+i*800),C_img)
            count +=1
            draw.text((300+j*570,740+i*800),name,(0,0,0),font,'mm')
            draw.text((300+j*570,770+i*800),text,(0,0,0),font,'mm')
        if j+i*4 == card_num:
            break
    img = img.crop((0,0,2310,860+800*line))
    img = img.convert('RGB')
    buf = BytesIO()
    img.save(buf, format='JPEG')
    base64_str = f'base64://{base64.b64encode(buf.getvalue()).decode()}'
    img = f'[CQ:image,file={base64_str}]'
    return img

async def index_card(cond,words):#通过条件&关键词模糊搜索卡牌,返回cards:list->[{'card':card(dict),'dm':100}]
    cards = []
    costmatch = r'^\d{1,2}c$'
    lifematch = r'^life\d{1,2}$'
    atkmatch = r'^atk\d{1,2}$'
    with open(join(MOUDULE_PATH,'cardinfo_tw.json'),'r', encoding='UTF-8') as f:
        tw = json.load(f)
    for i in cond:#按条件筛选
        cardselect = []
        if re.match(costmatch,i):
            for card in tw:
                if card["cost"] == int(i[:-1]):
                    cardselect.append(card)
        elif re.match(lifematch,i):
            for card in tw:
                if card["life"] == int(i[4:]):
                    if card["char_type"] == 1:
                        cardselect.append(card)
        elif re.match(atkmatch,i):
            for card in tw:
                if card["atk"] == int(i[3:]):
                    if card["char_type"] == 1:
                        cardselect.append(card)
        elif i in tribe_name:
            for card in tw:
                if i in card["tribe_name"] or card["tribe_name"] == "全部":
                    cardselect.append(card)
        elif check_cond(i):
            a,b = check_cond(i)
            for card in tw:
                if card[a] == b:
                    cardselect.append(card)
        tw = cardselect
    if words == []:
        for card in tw:
            cards.append({"card":card,"dm":1.00})
    else:
        wordnum = len(words)
        for card in tw:
            dm = 0
            for word in words:
                dm += max(fuzz.partial_ratio(card["card_name"].replace(' ',''),word),fuzz.partial_ratio(card["skill_disc"].replace(' ',''),word),fuzz.partial_ratio(card["evo_skill_disc"].replace(' ',''),word))
            dm = int(dm/wordnum)
            if dm > 60:
                cards.append({'card':card,"dm":dm/100})
    return cards

@sv.on_prefix('sv查卡')
async def sv_index(bot,ev:CQEvent):
    words = ev.message.extract_plain_text().replace(' #','#').replace('#', ' #').strip()
    if words == '':
        await bot.send('请输入条件&关键词!',at_sender=True)
    words = zhconv.convert(words,'zh-tw').split(' ')
    cond = []
    for i in words:
        if i[0] == '#':
            cond.append(i[1:])
    for i in cond:
        words.remove('#'+i)
    cards = await index_card(cond,words)
    try:
        if len(cards) == 0:
            await bot.send(ev,'抱歉,未查询到符合条件的卡牌',at_sender = True)
            return 
        elif len(cards) == 1:
            card = cards[0]['card']
            img = await cardinfo_gen(card)
            await bot.send(ev,f'{card["card_name"]}\n匹配度{cards[0]["dm"]}\n{img}',at_sender = True)
            return
        elif len(cards) > 20:
            await bot.send(ev,f'查询到近似结果{len(cards)}张\n只显示最近似20张\n使用svcard+id可以查看卡牌详细信息',at_sender = True)
            cards_sorted = sorted(cards,key = lambda x : x['dm'],reverse=True)[:20] 
            img = await selectlist(cards_sorted)
            await bot.send(ev,img)
            return
        if len(cards) > 1:
            cards_sorted = sorted(cards,key = lambda x : x['dm'],reverse=True)
            img = await selectlist(cards_sorted)
            await bot.send(ev,f'查询到如下{len(cards)}张可能结果\n使用svcard+id可以查看卡牌详细信息',at_sender = True)
            await bot.send(ev,img)
            return
    except Exception as e:
        exstr = traceback.format_exc()
        await bot.send(ev,f'查询失败，{str(exstr)}')

@sv.on_prefix('svcard')
async def sv_card(bot,ev:CQEvent):
    id = ev.message.extract_plain_text().strip()
    if not id.isdigit() or not len(id) == 9:
        await bot.send(ev,'id应为9位整数',at_sender = True)
        return
    with open(join(MOUDULE_PATH,'cardinfo_tw.json'), 'r', encoding='UTF-8') as f:
        tw = json.load(f)
    check_card = next((d for d in tw if d["card_id"] == int(id)),None)
    if check_card:
        img = await cardinfo_gen(check_card)
        await bot.send(ev,img)
    else:
        await bot.send(ev,f'没有卡牌对应此id:{id}',at_sender = True)



