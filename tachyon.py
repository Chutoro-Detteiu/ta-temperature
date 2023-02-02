import discord
import requests
import traceback
import asyncio
from area_db import *
import area_db
import datetime

TOKEN = 'hogehoge12345678'
dt_now = datetime.datetime.now()
year_base = 2022
dist_base = int(dt_now.strftime('%Y')) - year_base
year_name = ['ジュニア','クラシック','シニア']
if dist_base == 0 and int(dt_now.strftime('%m')) <= 6:
    season = 'デビュー前'
elif int(dt_now.strftime('%d')) < 15:
    if int(dt_now.strftime('%m')) < 10:
        season = dt_now.strftime('%m').strip('0') + '月前半'
    else:
        season = dt_now.strftime('%m') + '月前半'
else:
    if int(dt_now.strftime('%m')) < 10:
        season = dt_now.strftime('%m').strip('0') + '月後半'
    else:
        season = dt_now.strftime('%m') + '月後半'

client = discord.Client(activity=discord.Game(name=year_name[dist_base] + '級' + season))
isrunning = False
isPassingdeteal = False
input_pref = True

days_list = ['今日','明日','明後日']

weather_data_url = 'https://weather.tsukumijima.net/api/forecast/city/'


comments = [[15.0,27,'ヒトという生き物は15度を下回ると肌寒さを感じるらしい。それは私たちウマ娘も同様だ。ということでトレーナーくん、こたつの準備はいいね?']]


@client.event
async def on_ready():
    # 起動したらターミナルにログイン通知が表示される
    print('ログインしました')
    print('Ready to sent message')



@client.event
async def on_message(message):
    global days_list
    loop_count = 0
    isPassingdeteal = False
    input_pref = True
    input_area = True
    ispassingcomment = True
    sendtext = ''
    ispassing = False
    global isrunning
    def check(msg):
                    return msg.author == message.author
    if not isrunning:
        if 'タキオン' in message.content and '天気' in message.content:
            for i in range(0,len(days_list)):  
                if days_list[i] in message.content:
                    day = days_list[i]
                    daynum = i
                    break
                elif i == len(days_list)-1:
                    ispassing = True
                
                
            if not ispassing:
                try:
                    isrunning = True
                    async with message.channel.typing(): # 送られてきたチャンネルで入力中と表示させる
                            await asyncio.sleep(8)
                    await message.channel.send("アグネスタキオンだ。私の力が必要かい?")
                    async with message.channel.typing(): # 送られてきたチャンネルで入力中と表示させる
                            await asyncio.sleep(6)
                    await message.channel.send("どこの天気が知りたいか教えてくれたまえ")
                    wait_message = await client.wait_for("message",check=check)
                    is_need_select_area = False

                    while input_pref:
                        for i in range(0,len(area_db.pref_data)):
                            print(area_db.pref_data[i][0])
                            print(str(wait_message.content))
                            if area_db.pref_data[i][0] in str(wait_message.content):
                                print('area_db.pref_data[i][0] in str(wait_message)')
                                is_need_select_area = True
                                if '大阪' in str(wait_message.content) or '香川' in str(wait_message.content):
                                    isPassingdeteal = True 
                                prefnum = i
                                input_pref = False
                                break
                            
                            elif i == len(area_db.pref_data)-1:
                                async with message.channel.typing(): # 送られてきたチャンネルで入力中と表示させる
                                    await asyncio.sleep(7)
                                await message.channel.send('トレーナーくん?ちゃんと都道府県を入れたまえ')
                                wait_message = await client.wait_for("message",check=check)
                                break
                            


                    if is_need_select_area:

                        if not isPassingdeteal:
                            for n in range(area_db.pref_data[prefnum][1],area_db.pref_data[prefnum][2]):
                                sendtext = sendtext + area_db.area_name[n][0]
                                if n != area_db.pref_data[prefnum][2]-1:
                                    sendtext = sendtext + ' , '
                                

                            await asyncio.sleep(3)
                            async with message.channel.typing(): # 送られてきたチャンネルで入力中と表示させる
                                await asyncio.sleep(0.5)
                            await message.channel.send(sendtext)
                            async with message.channel.typing(): # 送られてきたチャンネルで入力中と表示させる
                                await asyncio.sleep(7)
                            await message.channel.send('地域を上から選んでくれたまえよ')
                        
                            wait_message = await client.wait_for("message",check=check)
                            is_need_select_area =False
                            isPassingdeteal = False

                        while input_area:
        
                            for i in range(area_db.pref_data[prefnum][1],area_db.pref_data[prefnum][2]):
                                if area_db.area_name[i][0] in wait_message.content:
                                    readurl = weather_data_url + area_db.area_name[i][1]
                                    input_area = False
                                    break

                                elif i == area_db.pref_data[prefnum][2]-1:
                                    async with message.channel.typing(): # 送られてきたチャンネルで入力中と表示させる
                                        await asyncio.sleep(7)
                                        await message.channel.send('トレーナーくん?ちゃんと地域を入れたまえ')
                                        wait_message = await client.wait_for("message",check=check)
                                        break
                                                    

                    json_get = requests.get(readurl).json()

                    try:
                        if isPassingdeteal:
                            if json_get['forecasts'][daynum]['temperature']['max']['celsius'] == None:
                                sendtext = day + 'の' + json_get['location']['prefecture']  + 'の天気は' + json_get['forecasts'][daynum]['telop'] + '、最低気温が'  + json_get['forecasts'][daynum]['temperature']['min']['celsius'] + '度だそうだ'
                            elif json_get['forecasts'][daynum]['temperature']['min']['celsius'] == None:    
                                sendtext = day + 'の' + json_get['location']['prefecture']  + 'の天気は' + json_get['forecasts'][daynum]['telop'] + '、最高気温が' + json_get['forecasts'][daynum]['temperature']['max']['celsius'] + '度だそうだ'
                            else:
                                sendtext = day + 'の' + json_get['location']['prefecture']  + 'の天気は' + json_get['forecasts'][daynum]['telop'] + '、最高気温が' + json_get['forecasts'][daynum]['temperature']['max']['celsius'] + '度で最低気温が' + json_get['forecasts'][daynum]['temperature']['min']['celsius'] + '度だそうだ'

                        else:
                            if json_get['forecasts'][daynum]['temperature']['max']['celsius'] == None:
                                sendtext = day + 'の' + json_get['location']['prefecture']  + ' '+ json_get['location']['district'] + 'の天気は' + json_get['forecasts'][daynum]['telop'] + '、最低気温が'  + json_get['forecasts'][daynum]['temperature']['min']['celsius'] + '度だそうだ'
                            elif json_get['forecasts'][daynum]['temperature']['min']['celsius'] == None:    
                                sendtext = day + 'の' + json_get['location']['prefecture']  + ' '+ json_get['location']['district'] + 'の天気は' + json_get['forecasts'][daynum]['telop'] + '、最高気温が' + json_get['forecasts'][daynum]['temperature']['max']['celsius'] + '度だそうだ'
                            else:
                                sendtext = day + 'の' + json_get['location']['prefecture']  + ' '+ json_get['location']['district'] + 'の天気は' + json_get['forecasts'][daynum]['telop'] + '、最高気温が' + json_get['forecasts'][daynum]['temperature']['max']['celsius'] + '度で最低気温が' + json_get['forecasts'][daynum]['temperature']['min']['celsius'] + '度だそうだ'

                    except:
                        while json_get['forecasts'][daynum]['temperature']['max']['celsius'] == None:
                            loop_count = loop_count + 1
                            json_get = requests.get(readurl).json()
                            await asyncio.sleep(0.5)
                            if loop_count == 3:
                                ispassingcomment = True
                                sendtext = "トレーナーくん、どうやらデータが配信されていないようだ。日付が変わるまで待ってもらってもいいかな?"
                                break
                                
                    async with message.channel.typing(): # 送られてきたチャンネルで入力中と表示させる
                        await asyncio.sleep(15)

                    await message.channel.send(sendtext)
                    if not ispassingcomment:
                        mintemp = json_get['forecasts'][daynum]['temperature']['min']['celsius']

                        for i in range(0,len(comments)):
                            if float(mintemp) <= comments[i][0]:
                                async with message.channel.typing(): # 送られてきたチャンネルで入力中と表示させる
                                    await asyncio.sleep(comments[i][1])
                                await message.channel.send(comments[i][2])
                                


                    isrunning = False
                    input_pref = True
                    input_area = True
                    ispassingcomment = True
                    loop_count = 0
                except:
                    await message.channel.send('トレーナー君、来たまえ！もろもろ検証し直しだ！')
                    await message.channel.send(traceback.format_exc())
                    pass

client.run(TOKEN)
