import discord
from discord.ext import commands

import requests
import os

import psycopg2
import random,time

bot = commands.Bot(command_prefix="_",activity=discord.Game("_help でコマンド確認！"))
bot.remove_command('help')
token = os.environ['DISCORD_BOT_TOKEN']
matti_data = {}
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
		speaker_ = 'takeru'
		#男02

	elif speaker_number == '2':
		speaker_ = 'haruka'
		#女01

	elif speaker_number == '3':
		speaker_ = 'hikari'
		#女02

	elif speaker_number == '4':
		speaker_ = 'santa'
		#サンタ

	elif speaker_number == '5':
		speaker_ = 'bear'
		#クマ

	#print(speaker)
	payload = {
	    'text': text,
	    'speaker': speaker_,
	    'format':'mp3',
	    'volume':'150',
        'pitch':pitch,
        'speed':speed,
	    }

	send = requests.post(url, params = payload, auth = (API_KEY,''))

	result = open(ID + ".mp3", 'wb')
	result.write(send.content)
	result.close()

def V_setting():
    speaker_number = random.randint(1, 5)
    pitch = random.randint(50, 200)
    speed = random.randint(70, 300)
    return speaker_number,pitch,speed

def get_connection():
    dsn = os.environ.get('DATABASE_URL').replace("://", "ql://", 1)
    return psycopg2.connect(dsn)

def Vcheck(ID,v_text,name):
    print(str(name))
    str_name = str(name)
    print(str_name.split('#')[0])
    #text = str_name.split('#')[0] + "さん。" + v_text
    text = v_text
    print(text)
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("ROLLBACK")
    conn.commit()
    cur.execute('SELECT * FROM db')

    for row in cur:
        if str(ID) in row:
            voicetext2(row[0],row[1],row[2],row[3],text)
            return #row[0],row[1],row[2],row[3]

    #speaker,pitch,speed
    speaker_number,pitch,speed = V_setting()
    cur.execute("insert into db values('{ID_}','{speaker}','{pitch}','{speed}','{text}')".format(ID_=ID,speaker=speaker_number,pitch=pitch,speed=speed,text='hoge'))
    conn.commit()
    voicetext2(str(ID),speaker_number,pitch,speed,text)
    return #ID,speaker,pitch,speed

def Mcheck():
    try:
        id_list = [id for id, v in matti_data.items() if v == 'mtrue']
        return id_list
    except:
        return 'none'
    """
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("ROLLBACK")
    conn.commit()
    cur.execute('SELECT * FROM db')
    print('mtrue')
    list = []
    for row in cur:
        print(row[0])
        if row[0] == 'mtrue':
            list.append(row[4])
    print(list)
    return list
    """
def Mcheck2(ID):
    try:
        matti = matti_data[ID]
        return matti
    except:
        return 'mfalse'
    """
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("ROLLBACK")
    conn.commit()
    cur.execute('SELECT * FROM db')
    print(ID)
    for row in cur:
        print(row[4])
        if row[4] == str(ID):
            return row[0]
    """

def Gcheck(ID):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("ROLLBACK")
    conn.commit()
    cur.execute('SELECT * FROM db')
    print(ID)
    for row in cur:
        print(row[0])
        if row[0] == str(ID):
            return row[4]
    '''
    text = 'true'
    cur.execute("insert into db values('{ID}','{speaker}','{pitch}','{speed}','{text}')".format(ID=ID,speaker='',pitch='',speed='',text=text))
    conn.commit()
    return ID,text
    '''

def seve(ID,text):
    print(ID)
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("ROLLBACK")
        conn.commit()
        cur.execute('SELECT * FROM db')
        for row in cur:
            print(row[0])
            if row[0] == str(ID):
                print(row)
                cur.execute('''UPDATE db SET text = '{text}' WHERE id_ ='{ID}';'''.format(text=text,ID=ID))
                conn.commit()
                return
        #cur.execute("UPDATE db SET name = '{name}' WHERE user_id='{user_id}';".format(name=ID2,user_id=ID+'Ms'))
        cur.execute("insert into db values('{ID_}','{speaker}','{pitch}','{speed}','{text}')".format(ID_=ID,speaker='hoge',pitch='hoge',speed='hoge',text=text))
        conn.commit()
        return
    except Exception as e:
        print (str(e))
        return


def seve2(ID,speaker,pitch,speed):
    print(ID)
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("ROLLBACK")
        conn.commit()
        cur.execute('SELECT * FROM db')
        for row in cur:
            print(row[0])
            if row[0] == str(ID):
                print(row)
                cur.execute('''UPDATE db SET speaker = '{speaker}', pitch = '{pitch}', speed = '{speed}'  WHERE id_ ='{ID}';'''.format(speaker=speaker,pitch=pitch,speed=speed,ID=ID))
                conn.commit()
                return
        #cur.execute("UPDATE db SET name = '{name}' WHERE user_id='{user_id}';".format(name=ID2,user_id=ID+'Ms'))
        cur.execute("insert into db values('{ID_}','{speaker}','{pitch}','{speed}','{text}')".format(ID_=ID,speaker=speaker,pitch=pitch,speed=speed,text='hoge'))
        conn.commit()
        return
    except Exception as e:
        print (str(e))
        return

def seve3(ID,matti):
    global matti_data
    matti_data[ID] = matti
    """
    print(ID)
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("ROLLBACK")
        conn.commit()
        cur.execute('SELECT * FROM db')
        for row in cur:
            print(row[0])
            if row[0] == str(matti):
                print(row)
                cur.execute('''UPDATE db SET id_ ='{ID}' WHERE text = '{text}';'''.format(text=ID,ID=matti))
                conn.commit()
                return
        #cur.execute("UPDATE db SET name = '{name}' WHERE user_id='{user_id}';".format(name=ID2,user_id=ID+'Ms'))
        cur.execute("insert into db values('{ID_}','{speaker}','{pitch}','{speed}','{text}')".format(ID_=matti,speaker='hoge',pitch='hoge',speed='hoge',text=ID))
        conn.commit()
        return
    except Exception as e:
        print (str(e))
        return
    """
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
    #voice_client = message.guild.voice_client
    text = Gcheck(message.channel.id)
    print(text)
    if text == 'true':
        if "_" in message.content:
            await bot.process_commands(message)
            return
        Vcheck(message.author.id,message.content,message.author)
        matti = Mcheck2(message.guild.voice_client)
        if matti == 'mtrue':
            print("m_start")
            mattilist = Mcheck()
            ffmpeg_audio_source = discord.FFmpegPCMAudio(str(message.author.id)+".mp3")
            if mattilist == 'none':
                voice_client = message.guild.voice_client
                try:
                    voice_client.play(ffmpeg_audio_source)
                except:
                    await bot.process_commands(message)
            else:
                for id in mattilist:
                    print(id)
                    voice_client = id
                    try:
                        voice_client.play(ffmpeg_audio_source)
                        time.sleep(1)
                    except:
                        await bot.process_commands(message)
        else:
            voice_client = message.guild.voice_client
            ffmpeg_audio_source = discord.FFmpegPCMAudio(str(message.author.id)+".mp3")
            try:
                voice_client.play(ffmpeg_audio_source)
            except:
                await bot.process_commands(message)
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
async def matchingon(ctx):
    """読み上げを開始します"""
    seve3(ctx.message.guild.voice_client,'mtrue')
    await ctx.send("マッチ読み上げを開始します。自動読み上げがオフの場合は別コマンドで起動してください。")

@bot.command()
async def matchingoff(ctx):
    """読み上げを停止します"""
    seve3(ctx.message.guild.voice_client,'mfalse')
    await ctx.send("マッチ読み上げを停止します。自動読み上げがオンの場合は別コマンドで停止してください。")

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


@bot.command()
async def s(ctx,speaker : str,pitch : str,speed : str):
    """話者(1～6)ピッチ(50～200)スピード(50～400)を数字で入力し、声を変更します\n例 !s 1 100 150 """
    seve2(ctx.message.author.id,speaker,pitch,speed)
    await ctx.send("設定しました")

@bot.command()
async def r(ctx):
    """話者,ピッチ,スピードをランダムで決定します"""
    speaker_number,pitch,speed = V_setting()
    seve2(ctx.message.author.id,speaker_number,pitch,speed)
    await ctx.send("設定しました")

@bot.command()
async def help(ctx):
    """コマンドの説明などを表示します"""
    embed = discord.Embed(title="TextVoiceBot Help",description="TextVoiceBotの使い方",color=discord.Colour.dark_green())
    embed.add_field(name="_join",value="Botをボイスチャンネルに入室させます。(_connect,_comeでも使えます)")
    embed.add_field(name="_leave",value="Botをボイスチャンネルから切断します。(_disconnect,_byeでも使えます)")
    embed.add_field(name="_t",value="1~6の数字で話者を選択したの後にスペースを入れ喋らせたい文を入力するとボイスチャンネルで喋ります")
    embed.add_field(name="_t の例",value="_s 1 これはテストです : この場合話者1の声で「これはテストです」と喋ります")
    embed.add_field(name="_k",value="喋らせたい文を入力すると某k氏が喋ります")
    embed.add_field(name="_k の例",value="_k これはテストです : 「これはテストです」とボイスチャンネルで喋ります")
    embed.add_field(name="_start",value="コマンドを実行したテキストチャンネルの読み上げを開始します")
    embed.add_field(name="_stop",value="コマンドを実行したテキストチャンネルの読み上げを停止します")
    embed.add_field(name="_s",value="話者(1～6)ピッチ(50～200)スピード(50～400)を数字で入力し、声を変更します")
    embed.add_field(name="_s の例",value="_s 1 100 150 : 自分のテキスト読み上げの声を 話者1,ピッチ100,速度150 に設定します")
    embed.add_field(name="_r",value="話者,ピッチ,スピードをランダムで決定します")
    embed.add_field(name="_matchingon",value="matchingモードを有効にしている全てのサーバーに自動読み上げ音声を流します。")
    embed.add_field(name="_matchingoff",value="matchingモードを停止します")
    await ctx.send(embed=embed)



bot.run(token)
