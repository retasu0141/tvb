import discord
from discord.ext import commands

import requests
import os

import psycopg2
import random

bot = commands.Bot(command_prefix="!")
token = os.environ['DISCORD_BOT_TOKEN']

'''
if not discord.opus.is_loaded():
    #もし未ロードだったら
    discord.opus.load_opus('opus')
    discord.opus.load_opus("buildpack-libopus")
    discord.opus.load_opus("buildpack-ffmpeg-latest")
'''

def voicetext2(ID,speaker_number,pitch,speed,text):
	#print(speaker_number)
	url = 'https://api.voicetext.jp/v1/tts'
	API_KEY = 'x5pp7y8ltm89669p'
	#if speaker_number == '1':
	#	speaker = 'show'
		#男01

	if speaker_number == '1':
		speaker = 'takeru'
		#男02

	elif speaker_number == '2':
		speaker = 'haruka'
		#女01

	elif speaker_number == '3':
		speaker = 'hikari'
		#女02

	elif speaker_number == '4':
		speaker = 'santa'
		#サンタ

	elif speaker_number == '5':
		speaker = 'bear'
		#クマ

	#print(speaker)
	payload = {
	    'text': text,
	    'speaker': speaker,
	    'format':'mp3',
	    'volume':'150',
        'pitch':pitch,
        'speed':speed,
	    }

	send = requests.post(url, params = payload, auth = (API_KEY,''))

	result = open(ID + ".mp3", 'wb')
	result.write(send.content)
	result.close()

def random():
    speaker = random.uniform(1, 5)
    pitch = random.uniform(50, 200)
    speed = random.uniform(70, 300)
    return speaker,pitch,speed

def get_connection():
    dsn = os.environ.get('DATABASE_URL')
    return psycopg2.connect(dsn)

def Vcheck(ID,v_text):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("ROLLBACK")
    conn.commit()
    cur.execute('SELECT * FROM db')

    for row in cur:
        if ID in row:
            voicetext2(row[0],row[1],row[2],row[3],v_text)
            return #row[0],row[1],row[2],row[3]

    #speaker,pitch,speed
    speaker,pitch,speed = random()
    cur.execute("insert into db values('{ID}','{speaker}','{pitch}','{speed}','{text}')".format(ID=ID,speaker=speaker,pitch=pitch,speed=speed,text=''))
    conn.commit()
    voicetext2(ID,speaker,pitch,speed,v_text)
    return #ID,speaker,pitch,speed

def Gcheck(ID):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("ROLLBACK")
    conn.commit()
    cur.execute('SELECT * FROM db')

    for row in cur:
        if ID in row:
            return row[0],row[4]
    '''
    text = 'true'
    cur.execute("insert into db values('{ID}','{speaker}','{pitch}','{speed}','{text}')".format(ID=ID,speaker='',pitch='',speed='',text=text))
    conn.commit()
    return ID,text
    '''

def seve(ID,text):
    #ID=ユーザーID URL=youtube_url
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("ROLLBACK")
        conn.commit()
        cur.execute('SELECT * FROM db')
        for row in cur:
            if ID in row:
                print(row)
                cur.execute("UPDATE db SET text = '{text}' WHERE ID='{ID}';".format(text=text,ID=ID))
                conn.commit()
                return
        #cur.execute("UPDATE db SET name = '{name}' WHERE user_id='{user_id}';".format(name=ID2,user_id=ID+'Ms'))
        cur.execute("insert into db values('{ID}','{speaker}','{pitch}','{speed}','{text}')".format(ID=ID,speaker='',pitch='',speed='',text=text))
        conn.commit()
        return
    except Exception as e:
        print (str(e))
        return

def voicetext(text,speaker_number):
	#print(speaker_number)
	url = 'https://api.voicetext.jp/v1/tts'
	API_KEY = 'x5pp7y8ltm89669p'
	try:
		if speaker_number == '1':
			speaker = 'show'
			#男01

		elif speaker_number == '2':
			speaker = 'takeru'
			#男02

		elif speaker_number == '3':
			speaker = 'haruka'
			#女01

		elif speaker_number == '4':
			speaker = 'hikari'
			#女02

		elif speaker_number == '5':
			speaker = 'santa'
			#サンタ

		elif speaker_number == '6':
			speaker = 'bear'
			#クマ
		else:
			speaker = 'show'

	except:
		speaker = 'show'
		#その他 男01
	#print(speaker)
	payload = {
	    'text': text,
	    'speaker': speaker,
	    'format':'mp3',
	    'volume':'150',
	    }

	send = requests.post(url, params = payload, auth = (API_KEY,''))

	result = open("voice.mp3", 'wb')
	result.write(send.content)
	result.close()



@bot.event
async def on_ready():
    print('Botを起動しました。')

@bot.event
async def on_message(message):
    # メッセージの送信者がbotだった場合は無視する
    if message.author.bot:
        return
    print('Gcheck')
    voice_client = message.guild.voice_client
    text = Gcheck(message.channel.id)
    print(text)
    if text == 'true':
        Vcheck(message.author.id,message.content)
        ffmpeg_audio_source = discord.FFmpegPCMAudio(message.author.id+".mp3")
    await bot.process_commands(message)

@bot.command(aliases=["connect","come"]) #connectやsummonでも呼び出せる
async def join(ctx):
    """Botをボイスチャンネルに入室させます。"""
    voice_state = ctx.author.voice

    if (not voice_state) or (not voice_state.channel):
        await ctx.send("先にボイスチャンネルに入っている必要があります。")
        return

    channel = voice_state.channel

    await channel.connect()
    print("connected to:",channel.name)


@bot.command(aliases=["disconnect","bye"])
async def leave(ctx):
    """Botをボイスチャンネルから切断します。"""
    voice_client = ctx.message.guild.voice_client

    if not voice_client:
        await ctx.send("Botはこのサーバーのボイスチャンネルに参加していません。")
        return

    await voice_client.disconnect()
    await ctx.send("ボイスチャンネルから切断しました。")

@bot.command()
async def start(ctx):
    """読み上げを開始します"""
    seve(ctx.channel.id,'true')
    await ctx.send("読み上げを開始します")

@bot.command()
async def stop(ctx):
    """読み上げを停止します"""
    seve(ctx.channel.id,'false')
    await ctx.send("読み上げを停止します")

@bot.command()
async def t(ctx,left : str, right : str):
    """1~6の数字で話者を選択したの後にスペースを入れ喋らせたい文を入力してください"""
    voice_client = ctx.message.guild.voice_client
    voicetext(right,left)
    ffmpeg_audio_source = discord.FFmpegPCMAudio("voice.mp3")
    voice_client.play(ffmpeg_audio_source)

@bot.command()
async def k(ctx,text : str):
    """喋らせたい文を入力すると某k氏が喋ります"""
    voice_client = ctx.message.guild.voice_client
    voicetext(text,'1')
    ffmpeg_audio_source = discord.FFmpegPCMAudio("voice.mp3")
    voice_client.play(ffmpeg_audio_source)


        #message.author.id
        #message.guild


bot.run(token)
