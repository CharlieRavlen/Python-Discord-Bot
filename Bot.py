import discord
from discord.ext import commands
from discord.ext.commands import CommandNotFound

bot = commands.Bot(command_prefix='?')
myToken = open("token.txt", "r").read()


@bot.command(aliases=['ChangeStatus', 'changestatus', 'Status'])
async def status(ctx, *, message: str):
    await bot.change_presence(activity=discord.Game(name=message))


@status.error
async def status_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.channel.send("You must give an argument")
        return


@bot.command()
async def join(ctx):
    if ctx.author.voice:
        channel = ctx.author.voice.channel
        voice = await channel.connect()
        return voice
    else:
        await ctx.channel.send("You aren't in a voice channel")


@bot.command()
async def play(ctx, *, args):
    voice = await join(ctx)
    if voice is None:
        return
    song = "test.mp3"
    voice.play(discord.FFmpegPCMAudio(executable="ffmpeg.exe", source=song))
    await ctx.send('**Now playing:** {}'.format(args))


@play.error
async def play_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.channel.send("You must name a song to play")
        return


@bot.command()
async def pause(ctx, *args):
    voice = ctx.voice_client
    if voice is None:
        await ctx.channel.send("Not in a voice channel")
        return
    voice.pause()
    await ctx.send('**Paused**')


@bot.command()
async def resume(ctx):
    voice = ctx.voice_client
    if voice is None:
        await ctx.channel.send("Not in a voice channel")
        return
    voice.resume()
    await ctx.send('**Resumed**')


@bot.command()
async def leave(ctx):
    if ctx.author.voice:
        if ctx.voice_client.channel == ctx.author.voice.channel:
            voice = ctx.voice_client
            if voice:
                voice.stop()
            await ctx.guild.voice_client.disconnect()
        else:
            await ctx.channel.send("You must be in the same voice channel as me")
    else:
        await ctx.channel.send("You aren't in a voice channel")


@bot.command()
async def add(ctx, a: int, b: int):
    await ctx.channel.send(a + b)


def toUpper(value):
    return value.upper()


@bot.command()
async def test(ctx, a: toUpper):
    await ctx.channel.send(a)


@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, CommandNotFound):
        return
    raise error


@bot.event
async def on_ready():
    print('Logged on as {0}'.format(bot.user))


@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    print('Message from {0.author}: {0.content} from {0.channel.guild}'.format(message))
    await bot.process_commands(message)


bot.run(myToken)
