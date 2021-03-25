import discord
from discord.ext import commands
import random
import youtube_dl
import os

client = commands.Bot(command_prefix='.')



@client.event
async def on_ready():
    print('Bot')


@client.event
async def on_member_join(member):
    print(f'{member} залетел не в тот район.')


@client.event
async def on_member_remove(member):
    print(f'{member} прощай и больше не возвращайся ')


@client.command()
async def ping(ctx):
    await ctx.send(f'Pong! {round(client.latency * 1000)}ms')


@client.command(aliases=['8ball','test'])
async def _8ball(ctx, *, question):
    responses = [
                    "Точно ёп*",
                    "Инфа 100",
                    "Не ссы",
                    "Ес оф кусь",
                    "Положись на это",
                    "Как я погляжу это так",
                    "Скорее всего",
                    "Вангую успех",
                    "Да",
                    "Знаки указывают на то, что да. ",
                    "Попробуй позже",
                    "Спроси позже",
                    "Лучше тебе об этом не знать.",
                    "Я не ванга",
                    "Сконцентрируйтесь и спросите еще раз. ",
                    "Не рассчитывай на это. ",
                    "Я отвечу нет",
                    "Мои источники говорят нет. ",
                    "Скорее всего нет",
                    "Чё ты несёшь"
                ]
    await ctx.send(f'Вопрос: {question}\n{random.choice(responses)}')


@client.command()
async def clear(ctx, amount=5):
    await   ctx.channel.purge(limit=amount)


@client.command(pass_context=True)
async def join(ctx):
    if (ctx.author.voice):
        channel = ctx.message.author.voice.channel
        await channel.connect()
    else:
        await ctx.send('Join F**G voice channel, you stupid donut')


@client.command()
async def play(ctx, url : str):
    song_there = os.path.isfile("song.mp3")
    try:
        if song_there:
            os.remove("song.mp3")
    except PermissionError:
        await ctx.send("Wait for the current playing music to end or use the 'stop' command")
        return

    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)

    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])
    for file in os.listdir("./"):
        if file.endswith(".mp3"):
            os.rename(file, "song.mp3")
    voice.play(discord.FFmpegPCMAudio("song.mp3"))


@client.command()
async def leave(ctx):
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    if voice.is_connected():
        await voice.disconnect()
    else:
        await ctx.send("The bot is not connected to a voice channel.")


@client.command()
async def pause(ctx):
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    if voice.is_playing():
        voice.pause()
    else:
        await ctx.send("Currently no audio is playing.")


@client.command()
async def resume(ctx):
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    if voice.is_paused():
        voice.resume()
    else:
        await ctx.send("The audio is not paused.")


@client.command()
async def stop(ctx):
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    voice.stop()

client.run('ODI0NTQ1NTcwMTY5NDIxODQ2.YFw75w.KedupkrFJYiu544HH3wD0kPQrto')
