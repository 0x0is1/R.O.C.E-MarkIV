import discord
from discord.ext import commands
import embed_generator
import libluci2
import os
from webserver import start_server
import json

active_sessions = {}
parser = libluci2.Parser()
embedder = embed_generator.Embedder()
intents = discord.Intents.all()
bot = commands.Bot(command_prefix=';;', intents=intents)

bot.remove_command('help')

@bot.event
async def on_ready():
    print('Bot status: Online')

@bot.command()
async def search(ctx, db:str, name:str):
    data = parser.parseSearch(name, db)
    embed = embedder.search_embed(name, data[:15])
    await ctx.send(embed=embed)

@bot.command()
async def set(ctx, key:str, value:str):
    channel_id = ctx.message.channel.id
    if channel_id not in active_sessions.keys():
        active_sessions[channel_id] = dict()
    
    try:
        active_sessions[channel_id][key] = value
        await ctx.message.add_reaction('✅')

    except KeyError:
        await ctx.message.add_reaction('❌')

@bot.command()
async def get(ctx, module_name:str):
    channel_id = ctx.message.channel.id
    sesssion = active_sessions[channel_id]
    item_id = None
    db_type = None
    try:
        item_id = sesssion["id"]
    except KeyError:
        await ctx.send("❎ id is not defined")
        return

    try:
        db_type = sesssion["type"]
    except KeyError:
        await ctx.send("❎ type is not defined")
        return
    data = parser.parseGenbank(item_id, db_type)
    try:
        data = data[module_name.upper()]
        await ctx.send(f"```css\n{data}\n```")
    except KeyError:
        await ctx.send(f"❎ Module with '{module_name}' key is not defined")
        return


token = os.environ.get('BOT_TOKEN')
start_server()
bot.run(token)