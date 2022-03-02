import time

import discord
from discord.ext import commands
from discord.ext.commands import CommandNotFound

bot = commands.Bot(command_prefix='')
myToken = open("token.txt", "r").read()


@bot.command(pass_context=True, aliases=['ChangeStatus', 'changestatus', 'Status'])
async def status(ctx, *, message: str):
    await bot.change_presence(activity=discord.Game(name=message))


@status.error
async def status_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.channel.send("You must give an argument")
        return


@bot.command(pass_context=True)
async def join(ctx, *args):
    if ctx.author.voice:
        channel = ctx.author.voice.channel
        voice = await channel.connect()
        return voice
    else:
        await ctx.channel.send("You aren't in a voice channel")


@bot.command(pass_context=True)
async def play(ctx, *, args):
    voice = await join(ctx, args)
    if voice is None:
        return
    voice.play(discord.FFmpegPCMAudio(executable="ffmpeg.exe", source="Dancing Queen.m4a"))
    await ctx.send('**Now playing:** {}'.format(args))


@play.error
async def play_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.channel.send("You must name a song to play")
        return


@bot.command(pass_context=True)
async def pause(ctx, *args):
    voice = ctx.voice_client
    if voice is None:
        await ctx.channel.send("Not in a voice channel")
        return
    voice.pause()
    await ctx.send('**Paused**')


@bot.command(pass_context=True)
async def resume(ctx, *args):
    voice = ctx.voice_client
    if voice is None:
        await ctx.channel.send("Not in a voice channel")
        return
    voice.resume()
    await ctx.send('**Resumed**')


@bot.command()
async def leave(ctx, *args):
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
