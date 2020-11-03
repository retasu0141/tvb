import discord
from discord.ext import commands

import requests
import os

bot = commands.Bot(command_prefix="!")
token = os.environ['DISCORD_BOT_TOKEN']

if not discord.opus.is_loaded():
    #もし未ロードだったら
    discord.opus.load_opus('opus')
    discord.opus.load_opus("buildpack-libopus")
    discord.opus.load_opus("buildpack-ffmpeg-latest")

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


bot.run(token)
