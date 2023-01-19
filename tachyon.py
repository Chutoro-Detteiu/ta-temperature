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
dist_base = int(dt_now.strftime('%Y')) - 2023
year_name = ['ジュニア','クラシック','シニア']
if dist_base == 0 and int(dt_now.strftime('%m')) <= 6:
    season = 'デビュー前'
elif int(dt_now.strftime('%d')) < 15:
    if int(dt_now.strftime('%m')) < 10:
        season = dt_now.strftime('%m').strip('0') + '前半'
    else:
        season = dt_now.strftime('%m') + '前半'
else:
    if int(dt_now.strftime('%m')) < 10:
        season = dt_now.strftime('%m').strip('0') + '後半'
    else:
        season = dt_now.strftime('%m') + '後半'

client = discord.Client(activity=discord.Game(name=year_name[dist_base] + '級' + season))
isrunning = False
isPassingdeteal = False
input_pref = True

weather_data_url = 'https://weather.tsukumijima.net/api/forecast/city/'


@client.event
async def on_ready():
    # 起動したらターミナルにログイン通知が表示される
    print('ログインしました')
    print('Ready to sent message')



@client.event
async def on_message(message):
    isPassingdeteal = False
    input_pref = True
    input_area = True
    ispassingcomment = False
    sendtext = ''
    global isrunning
    def check(msg):
                    return msg.author == message.author
    if not isrunning:
        if 'タキオン' in message.content and '今日の天気' in message.content:

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
                    print('is_need_select_area')

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
                    #for i in range(0,len(area_db.area_name)):
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
                print(readurl)
                print(json_get)


                try:
                    #sendtext = '今日の' + json_get['title'] + 'は' + json_get['forecasts'][0]['telop'] + '、最高気温が' + json_get['forecasts'][0]['temperature']['max']['celsius'] + '度で最低気温が' + json_get['forecasts'][0]['temperature']['min']['celsius'] + '度だそうだ'
                    sendtext = '今日の' + json_get['location']['prefecture']  + ' '+ json_get['location']['district'] + 'の天気は' + json_get['forecasts'][0]['telop'] + '、最高気温が' + json_get['forecasts'][0]['temperature']['max']['celsius'] + '度で最低気温が' + json_get['forecasts'][0]['temperature']['min']['celsius'] + '度だそうだ'
                except:
                    print('except at line138')
                    while str(type(json_get['forecasts'][0]['telop'])) == "<class 'NoneType'>" or str(type(json_get['forecasts'][0]['temperature']['max']['celsius'])) == "<class 'NoneType'>" or str(type(json_get['forecasts'][0]['temperature']['min']['celsius'])) == "<class 'NoneType'>":
                        loop_count = loop_count + 1
                        print('looping at line139-141')
                        json_get = requests.get(readurl).json()
                        if loop_count == 10:
                            ispassingcomment = True
                            sendtext = "トレーナーくん、どうやらデータが配信されていないようだ。日付が変わるまで待ってもらってもいいかな?"
                            break
                            
                async with message.channel.typing(): # 送られてきたチャンネルで入力中と表示させる
                    await asyncio.sleep(15)

                await message.channel.send(sendtext)
                if not ispassingcomment:
                    mintemp = json_get['forecasts'][0]['temperature']['min']['celsius']
                    if float(mintemp) <= 15.0:
                        async with message.channel.typing(): # 送られてきたチャンネルで入力中と表示させる
                            await asyncio.sleep(27)
                        await message.channel.send('ヒトという生き物は15度を下回ると肌寒さを感じるらしい。それは私たちウマ娘も同様だ。ということでトレーナーくん、こたつの準備はいいね?')
                        


                isrunning = False
                input_pref = True
                input_area = True
                ispassingcomment = False
            except:
                await message.channel.send('トレーナー君、来たまえ！もろもろ検証し直しだ！')
                await message.channel.send(traceback.format_exc())
                pass

client.run(TOKEN)
