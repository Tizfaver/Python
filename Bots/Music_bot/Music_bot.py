#Author: @Tizfaver
#The bot is in Italian, you can use Google Translate, maybe I will translate it...
#install all libraries needed, works great with Python 3.9:
#pip install discord.py
#pip install discord.py[voice]
#pip install PyNaCl
#pip install yt_dlp
#if you are in linux to install FFMPEG use:
#sudo apt install ffmpeg
#else clone the github dir in the same folder of this main.py:
#git clone https://git.ffmpeg.org/ffmpeg.git ffmpeg

import discord
from discord.ext import commands
import yt_dlp
import os

client = commands.Bot(command_prefix="-f ", description="Helpfull Comands:")
client.remove_command('help')
last_ch = "null"

@client.command()

async def play(ctx, url : str):
    if isinstance(ctx.channel, discord.channel.DMChannel):
        await ctx.send("Non mi scrivere!")
        return
    
    global last_ch
    song_there = os.path.isfile("song.mp3")
    try:
        if song_there:
            os.remove("song.mp3")
    except PermissionError:
        await ctx.send(":x: ERRORE, RIAVVIARE IL BOT!")
        return
    
    try:
        if not is_connected(ctx):
            channel = ctx.author.voice.channel
            await channel.connect()
            last_ch = str(channel)
    except:
        voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
        await voice.disconnect()
    
    try:
        channel = ctx.author.voice.channel
        if not str(channel) == str(last_ch):
            await play_embed(ctx, '', ":x: Il bot è già collegato in un altro canale vocale: `" + str(last_ch) + "` mentre te sei in: `" + str(channel) + "`", discord.Colour.red())
            return
        else:
            temp = 0
    except:
        await play_embed(ctx, '', ':x: Devi essere connesso ad un canale vocale per eseguire questo comando!', discord.Colour.red())
        return
        
    if ValidURL(url) == False:
        await play_embed(ctx, '', ':x: Il tuo URL non è valido, ricontrolla!', discord.Colour.red())
        return
    
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)

    if voice.is_playing():
        voice.stop()
        await play_embed(ctx, '', ':stop_button: Fermo la canzone in esecuzione.', discord.Colour.red())

    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }
    
    await play_embed(ctx, '', ":hourglass_flowing_sand: Ricerca dell'url... Attendi 10 secondi", discord.Colour.red())
    
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        try:
            info_dict = ydl.extract_info(url, download=False)
            video_title = info_dict.get('title', None)
            video_lung = info_dict.get('duration', None)
            if(video_lung > 600): #600 = 10 minutes
                await play_embed(ctx, '', '', discord.Colour.red())
                return
            else:
                try:
                    ydl.download([url])
                except:
                    await play_embed(ctx, '', ':x: Il tuo URL non è valido!', discord.Colour.red())
                    return
                                    
                for file in os.listdir("./"):
                    if file.endswith(".mp3"):
                        os.rename(file, "song.mp3")
                voice.play(discord.FFmpegPCMAudio("song.mp3"))
                await play_embed(ctx, '', str(":white_check_mark: **Trovata! Riproduzione immediata!** \n\n:mag_right: In riproduzione: `" + str(video_title) + "` \n\n:stopwatch: Lunghezza brano: `" + str(Converti(video_lung)) + "`"), discord.Colour.red())

        except:
            await play_embed(ctx, '', ':x: Il tuo URL non è valido!', discord.Colour.red())

        
def Converti(video_lung):
    temp = video_lung
    m = 0
    
    if(temp < 60):
        return (str("0:" + str(temp)))
    elif (temp == 60):
        return ('1:00')
    else:
        while(temp >= 60):
            m += 1
            temp -= 60
        if(temp >= 10):
            return (str(str(m) + ':' + str(temp)))
        else:
            return (str(str(m) + ':0' + str(temp)))


def ValidURL(url):
    temp = url[0:32]
    
    if url == 'https://www.youtube.com/watch?v=':
        return False
    elif temp == 'https://www.youtube.com/watch?v=':
        return True
    else:
        return False


@client.command()
async def join(ctx):
    if isinstance(ctx.channel, discord.channel.DMChannel):
        await ctx.send("Non mi scrivere!")
        return
    
    global last_ch
    channel = ctx.author.voice.channel
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    
    try:
        if not is_connected(ctx):
            channel = ctx.author.voice.channel
            await channel.connect()
            await play_embed(ctx, '', ':person_running: Entro nel canale vocale: `' + str(channel) + '`', discord.Colour.red())
            last_ch = str(channel)
            return
        else:
            try:
                channel = ctx.author.voice.channel
                if not str(channel) == str(last_ch):
                    await play_embed(ctx, '', ":x: Non puoi eseguire questo comando fuori dal canale vocale: `" + str(last_ch) + "`", discord.Colour.red())
                    return
                else:
                    if is_connected(ctx):
                        await play_embed(ctx, '', ':x: Sono già connesso ad un canale vocale: `' + str(channel) + '`', discord.Colour.red())
                    else:
                        await play_embed(ctx, '', ':person_running: Entro nel canale vocale: `' + str(channel) + '`', discord.Colour.red())
                        await channel.connect()
            except:
                await play_embed(ctx, '', ':x: Per eseguire questo comando unisciti al canale vocale del bot!', discord.Colour.red())
                return
    except:
        voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
        await voice.disconnect()
    

@client.command()
async def leave(ctx):
    if isinstance(ctx.channel, discord.channel.DMChannel):
        await ctx.send("Non mi scrivere!")
        return
    
    global last_ch
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    
    try:
        channel = ctx.author.voice.channel
        if not str(channel) == str(last_ch):
            await play_embed(ctx, '', ":x: Non puoi eseguire questo comando fuori dal canale vocale: `" + str(last_ch) + "`", discord.Colour.red())
            return
        else:
            if voice.is_connected():
                voice.pause()
                await voice.disconnect()
                await play_embed(ctx, '', ':person_running: Quitto dalla stanza vocale!', discord.Colour.red())
            else:
                await play_embed(ctx, '', ':x: Non sono connesso a nessun canale vocale!', discord.Colour.red())
    except:
        await play_embed(ctx, '', ':x: Per eseguire questo comando unisciti al canale vocale del bot!', discord.Colour.red())
        return
    

@client.command()
async def pause(ctx):
    if isinstance(ctx.channel, discord.channel.DMChannel):
        await ctx.send("Non mi scrivere!")
        return
    
    global last_ch
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    
    try:
        channel = ctx.author.voice.channel
        if not str(channel) == str(last_ch):
            await play_embed(ctx, '', ":x: Non puoi eseguire questo comando fuori dal canale vocale: `" + str(last_ch) + "`", discord.Colour.red())
            return
        else:
            if is_connected(ctx):
                if voice.is_playing():
                    voice.pause()
                    await play_embed(ctx, '', ':pause_button: Traccia messa in pausa!', discord.Colour.red())
                else:
                    await play_embed(ctx, '', ':x: Nessuna traccia è in esecuzione', discord.Colour.red())
            else:
                await play_embed(ctx, '', ':x: Non sono connesso a nessuna stanza!', discord.Colour.red())
    except:
        await play_embed(ctx, '', ':x: Per eseguire questo comando unisciti al canale vocale del bot!', discord.Colour.red())
        return
    

@client.command()
async def resume(ctx):
    if isinstance(ctx.channel, discord.channel.DMChannel):
        await ctx.send("Non mi scrivere!")
        return
    
    global last_ch
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    
    try:
        channel = ctx.author.voice.channel
        if not str(channel) == str(last_ch):
            await play_embed(ctx, '', ":x: Non puoi eseguire questo comando fuori dal canale vocale: `" + str(last_ch) + "`", discord.Colour.red())
            return
        else:
            if is_connected(ctx):
                if voice.is_paused():
                    voice.resume()
                    await play_embed(ctx, '', ':arrow_forward: Ripresa la traccia!', discord.Colour.red())
                else: 
                    await play_embed(ctx, '', ':x: Prima ci deve essere un brano messo in pausa!', discord.Colour.red())
            else:
                await play_embed(ctx, '', ':x: Non sono connesso a nessuna stanza!', discord.Colour.red())
    except:
        await play_embed(ctx, '', ':x: Per eseguire questo comando unisciti al canale vocale del bot!', discord.Colour.red())
        return


@client.command()
async def replay(ctx):
    if isinstance(ctx.channel, discord.channel.DMChannel):
        await ctx.send("Non mi scrivere!")
        return
    
    global last_ch
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    
    try:
        channel = ctx.author.voice.channel
        if not str(channel) == str(last_ch):
            await play_embed(ctx, '', ":x: Non puoi eseguire questo comando fuori dal canale vocale: `" + str(last_ch) + "`", discord.Colour.red())
            return
        else:
            if not is_connected(ctx):
                voiceChannel = discord.utils.get(ctx.guild.voice_channels, name='ch')
                await voiceChannel.connect()
                voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
                await play_embed(ctx, '', ':repeat_one: Faccio ripartire da capo la canzone.', discord.Colour.red())
                voice.play(discord.FFmpegPCMAudio("song.mp3"))
            else:
                voice.stop()
                await play_embed(ctx, '', ':repeat_one: Faccio ripartire da capo la canzone.', discord.Colour.red())
                voice.play(discord.FFmpegPCMAudio("song.mp3"))
    except:
        await play_embed(ctx, '', ':x: Per eseguire questo comando unisciti al canale vocale del bot!', discord.Colour.red())
        return


@client.command()
async def stop(ctx):
    if isinstance(ctx.channel, discord.channel.DMChannel):
        await ctx.send("Non mi scrivere!")
        return
    
    global last_ch
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    
    try:
        channel = ctx.author.voice.channel
        if not str(channel) == str(last_ch):
            await play_embed(ctx, '', ":x: Non puoi eseguire questo comando fuori dal canale vocale: `" + str(last_ch) + "`", discord.Colour.red())
            return
        else:
            if is_connected(ctx):
                if not voice.is_playing():
                    await play_embed(ctx, '', ":x: Non c'è nessun brano da fermare", discord.Colour.red())
                else:
                    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
                    voice.pause()
                    voice.stop()
                    await play_embed(ctx, '', ':stop_button: Fermo del tutto la riproduzione!', discord.Colour.red())
            else:
                await play_embed(ctx, '', ':x: Non sono connesso a nessuna stanza!', discord.Colour.red())

    except:
        await play_embed(ctx, '', ':x: Per eseguire questo comando unisciti al canale vocale del bot!', discord.Colour.red())
        return


@client.command()
async def help(ctx):
    if isinstance(ctx.channel, discord.channel.DMChannel):
        await ctx.send("Non mi scrivere!")
        return
    
    await play_embed(ctx, '', "Elenco dei comandi che puoi fare: \n`-f play [url]` esegue la canzone dell'url \n`-f pause`      per mettere in pausa il brano in esecuzione \n`-f resume`     per riprendere il brano in esecuzione \n`-f stop`       per fermare del tutto il brano \n`-f replay`     per riascoltare l'ultimo brano \n`-f join` per fare entrare il bot nel canale vocale \n`-f leave` per far quittare il bot \n\n P.S.: Per eseguire i comandi, devi essere nel stesso canale vocale del bot (anti P.)!", discord.Colour.red())
    

async def play_embed(ctx, tit, desc, col):
    embed = discord.Embed(
        title = str(tit),
        description = str(desc),
        colour = col
    )
    await ctx.send(embed = embed)


def is_connected(ctx):
    voice_client = discord.utils.get(client.voice_clients, guild=ctx.guild)
    return voice_client and voice_client.is_connected()
    

@client.event
async def on_ready():
    await client.change_presence(activity = discord.Game("-f help")) 
    print('Il bot è in esecuzione')


client.run('OTQ5Mzc3ODg0ODczNzExNjY2.YiJfDg.vNs-RSI52mTkNn0r5uvOE0QZ2U8') #Use your TOKEN
