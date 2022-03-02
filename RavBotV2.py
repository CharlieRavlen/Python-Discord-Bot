from discord.ext import commands
import shlex

bot = commands.Bot(command_prefix='?')
myToken = ""

@bot.command()
async def join(ctx, *args):
    if args:
        await ctx.channel.send("Invalid use of this command")
        return
    if ctx.author.voice:
        channel = ctx.author.voice.channel
        await channel.connect()
    else:
        await ctx.channel.send("You aren't in a voice channel")

@bot.command()
async def leave(ctx, *args):
    if args:
        await ctx.channel.send("Invalid use of this command")
        return
    if ctx.author.voice:
        if ctx.voice_client.channel == ctx.author.voice.channel:
            await ctx.guild.voice_client.disconnect()
        else:
            await ctx.channel.send("You must be in the same voice channel as me")
    else:
        await ctx.channel.send("You aren't in a voice channel")

@bot.command()
async def play(ctx, *args):
    await join(ctx)


@bot.event
async def on_ready():
    print('Logged on as {0}!'.format(bot.user))

@bot.event
async def on_message(message):
    print('Message from {0.author}: {0.content}'.format(message))


bot.run(myToken)
