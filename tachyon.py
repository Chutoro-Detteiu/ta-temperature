import discord
import json
import requests
import traceback
import asyncio
from area_db import *
import area_db

TOKEN = 'hogehoge12345678'
client = discord.Client()
isrunning = False
isPassingdeteal = False

#whether_data_url = ['https://www.jma.go.jp/bosai/forecast/data/forecast/','.json']
#whether_data_url = ['https://www.jma.go.jp/bosai/forecast/data/overview_forecast/','.json']
weather_data_url = 'https://weather.tsukumijima.net/api/forecast/city/'



@client.event
async def on_ready():
    # 起動したらターミナルにログイン通知が表示される
    print('ログインしました')
    print('Ready to sent message')



@client.event
async def on_message(message):
    isPassingdeteal = False
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
                #if wait_message.content == "北海道":
                # deteal_area = [0,7]
                #  is_need_select_area = True
            #  elif wait_message.content == "沖縄":
                #   deteal_area = [51,55]
                    #is_need_select_area = True
                #is_need_select_area = True

                #try:
                for i in range(0,len(area_db.pref_data)):
                    print(area_db.pref_data[i][0])
                    print(str(wait_message.content))
                    if area_db.pref_data[i][0] in str(wait_message.content):
                        print('area_db.pref_data[i][0] in str(wait_message)')
                        is_need_select_area = True
                        if '大阪' in str(wait_message.content) or '香川' in str(wait_message.content):
                            isPassingdeteal = True 
                        prefnum = i
                        break
                    
                    
                    if not is_need_select_area and i == len(area_db.pref_data):
                        await message.channel.send('トレーナーくん?ちゃんと都道府県を入れたまえ')
                #except:
                    #await message.channel.send('トレーナーくん?ちゃんと都道府県を入れたまえ')

                if is_need_select_area:
                    print('is_need_select_area')
                    #for n in range(deteal_area[0],deteal_area[1]):
                    if not isPassingdeteal:
                        for n in range(area_db.pref_data[prefnum][1],area_db.pref_data[prefnum][2]):
                            sendtext = sendtext + area_db.area_name[n][0]
                            if n != area_db.pref_data[prefnum][2]-1:
                                sendtext = sendtext + ' , '
                            
                        #await message.channel.send(area_db.area_name[n][0])
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


                    for i in range(0,len(area_db.area_name)):
                        #if wait_message.content == area_db.area_name[i]:
                        if area_db.area_name[i][0] in wait_message.content:
                            readurl = weather_data_url + area_db.area_name[i][1]
                    #      readurl = whether_data_url[0] + area_code[i] + whether_data_url[1]

                    json_get = requests.get(readurl).json()

                    #await asyncio.sleep(4)
                    async with message.channel.typing(): # 送られてきたチャンネルで入力中と表示させる
                        await asyncio.sleep(15)
                # await message.channel.send(json_get['description']['text'])
                    sendtext = '今日の天気は' + json_get['forecasts'][0]['telop'] + '、最高気温が' + json_get['forecasts'][0]['temperature']['max']['celsius'] + '度で最低気温が' + json_get['forecasts'][0]['temperature']['min']['celsius'] + '度だそうだ'
                    await message.channel.send(sendtext)
                    mintemp = json_get['forecasts'][0]['temperature']['min']['celsius']
                    if float(mintemp) <= 15.0:
                        async with message.channel.typing(): # 送られてきたチャンネルで入力中と表示させる
                            await asyncio.sleep(27)
                        await message.channel.send('ヒトという生き物は15度を下回ると肌寒さを感じるらしい。それは私たちウマ娘も同様だ。ということでトレーナーくん、こたつの準備はいいね?')
                        

                    #async with message.channel.typing(): # 送られてきたチャンネルで入力中と表示させる
                        #await asyncio.sleep(3)
                    #asyncio.sleep(3)
                # await message.channel.send('...だそうだ')

                #print(json_get)
                isrunning = False
            except:
                await message.channel.send('トレーナー君、来たまえ！もろもろ検証し直しだ！')
                await message.channel.send(traceback.format_exc())

client.run(TOKEN)
