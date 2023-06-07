import requests
import os,json
from os.path import join
from PIL import Image
from io import BytesIO
MOUDULE_PATH = os.path.dirname(__file__)
def get_info():
     #获取卡牌信息
     url = 'https://shadowverse-portal.com/api/v1/cards'
     a = requests.get(url,params={"format":"json","lang":"zh-tw"})
     tw = json.loads(a.text)["data"]["cards"]
     nonamecard = []
     for i in tw:
          if i["card_name"] == None:
               print(f'remove  {i["card_id"]}')
               nonamecard.append(i)#筛选无名卡牌，一般为其他卡牌的激奏和结晶占位
          else:
               print(i["card_name"])
          if i["char_type"] == 3:
               i["char_type"] = 2
     for i in nonamecard:
          tw.remove(i)#删除无名卡
     with open(join(MOUDULE_PATH,"cardinfo_tw.json"),'w', encoding="utf-8") as f:
          json.dump(tw, f, indent=4, ensure_ascii=False)
     #获取图片
     img_url_e = 'https://shadowverse-portal.com/image/card/phase2/common/E/E_'#进化卡牌图片
     img_url_c = 'https://shadowverse-portal.com/image/card/phase2/common/C/C_'#卡牌图片
     name_url_tw = 'https://shadowverse-portal.com/image/card/phase2/zh-tw/N/N_'#卡牌名称
     cardnum = len(tw)
     count = 1
     for i in tw:
          if not os.path.exists(join(MOUDULE_PATH,f'pic/C_{i["card_id"]}.png')):
               print(f'generating {i["card_name"]}-C ({count}/{cardnum})')
               if i["card_id"] == 910441030:
                    card_pic = requests.get(f'{img_url_c}{i["card_id"]-10}.png')#爆破模式没有进化前卡面，另外两个有，替代一下
               else:
                    card_pic = requests.get(f'{img_url_c}{i["card_id"]}.png')
               card_name = requests.get(f'{name_url_tw}{i["card_id"]}.png')
               pic = Image.open(BytesIO(card_pic.content))
               name = Image.open(BytesIO(card_name.content))
               xn,yn = name.size
               #调整文字大小
               k = 40/yn
               newsize = (int(xn*k), 40)
               move = False
               if xn*k >= 300:
                    k = 340/xn
                    newsize = (340,int(yn*k))
                    move = True
               name = name.resize(newsize, resample=Image.LANCZOS)
               xn,yn = name.size
               if move:
                    left = int(290 - xn/2)
               else:
                    left = int(268 - xn/2)
               top = int(95 - yn/2)
               pic.paste(name,(left,top),name)
               pic.save(join(MOUDULE_PATH,f'pic/C_{i["card_id"]}.png'),'PNG')
          else:
               print(f'{i["card_name"]}-C already exists,pass ({count}/{cardnum})')
          if i["char_type"] == 1:
               if not os.path.exists(join(MOUDULE_PATH,f'pic/E_{i["card_id"]}.png')):
                    print(f'generating {i["card_name"]}-E ({count}/{cardnum})')
                    card_pic = requests.get(f'{img_url_e}{i["card_id"]}.png')
                    card_name = requests.get(f'{name_url_tw}{i["card_id"]}.png')
                    pic = Image.open(BytesIO(card_pic.content))
                    name = Image.open(BytesIO(card_name.content))
                    xn,yn = name.size
                    #调整文字大小
                    k = 40/yn
                    newsize = (int(xn*k), 40)
                    move = False
                    if xn*k >= 300:
                         k = 340/xn
                         newsize = (340,int(yn*k))
                         move = True
                    name = name.resize(newsize, resample=Image.LANCZOS)
                    xn,yn = name.size
                    if move:
                         left = int(290 - xn/2)
                    else:
                         left = int(268 - xn/2)
                    top = int(95 - yn/2)
                    pic.paste(name,(left,top),name)
                    pic.save(join(MOUDULE_PATH,f'pic/E_{i["card_id"]}.png'),'PNG')
               else:
                    print(f'{i["card_name"]}-E already exists,pass ({count}/{cardnum})')
          count += 1
          
