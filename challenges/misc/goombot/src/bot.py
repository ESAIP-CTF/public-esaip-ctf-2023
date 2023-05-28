import discord
from discord.ext import commands

from os import getenv
from dotenv import load_dotenv

import random
import time
import sqlite3

conn = sqlite3.connect("data.db")
c = conn.cursor()

load_dotenv()

TOKEN = getenv("TOKEN")

bot = commands.Bot(command_prefix="!", help_command=None, intents=discord.Intents.all())

@bot.event
async def on_command_error(ctx, error):
    # For the account and balance commands
    if isinstance(error, discord.ext.commands.errors.MissingRequiredArgument) and ctx.author.guild_permissions.administrator:
        await ctx.send("*I need an account ID*")
    elif isinstance(error, discord.ext.commands.errors.CommandNotFound):
        pass
    else:
        await ctx.send("An error occured.")

@bot.event
async def on_ready():
    print("Bot is ready !")
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name="   !help"))

@bot.event
async def on_message(message):
    if message.author != bot.user:
        if isinstance(message.channel, discord.channel.DMChannel):
            await message.channel.send("Don't talk to me in private messages like that. why don't you invite me instead ?")
        else:
            await bot.process_commands(message)

@bot.command(name="account")
async def account(ctx, arg):
    if arg:
        if ctx.author.guild_permissions.administrator:
            out = ""
            for row in c.execute("SELECT name FROM Accounts WHERE id=?", (arg,)):
                out += f"The name for account n°{arg} is {row[0]}\n"
            if out == "":
                await ctx.send(f"Account n°{arg} doesn't exist !")
            else:
                await ctx.send(out)
        else:
            await ctx.send('I will only tell that to high privileged people !')

@bot.command(name="balance")
async def balance(ctx, arg):
    if arg:
        if ctx.author.guild_permissions.administrator:
            out = ""
            query = f"SELECT * FROM Balances WHERE id={arg};"
            for row in c.execute(query):
                out += f"ID : {row[0]} -- Balance : {row[1]}:moneybag: -- Overdraft : {row[2]}\n"
            await ctx.send(out)
        else:
            await ctx.send('You are not my boss, I wont tell that to you !')

@bot.command(name="info")
async def info(ctx):
    infos = [
        "I have big teeth, but I don't really use them",
        "I get killed when someone jumps on my head 😰",
        "I am part of the Koppa Troop",
        "Some poeple say I look like a mushroom, I don't see why...",
        "I am inspired of the shiitake mushroom",
        "I don't know how to swim 😥",
        "My name comes from the italian word *compa* which means partner or buddy.",
        "Sometimes, I can jump, bite or even fly !",
        "I don't like heavy things, I prefer to work with light things."
    ]
    await ctx.send(random.choice(infos))
    

@bot.command(name='help')
async def help(ctx):
    await ctx.send("""**Hello I am the accountant goomba, you can use :**```
-   help : displays this menu
-   info : gives a random information about me
-   account [id] : gives the name for the account [id]
-   balance [id] : gives the total balance of account [id]```""")

bot.run(TOKEN)
