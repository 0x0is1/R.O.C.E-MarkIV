import discord
from discord.ext import commands
import embed_generator
import libluci2
import os
from webserver import start_server
import json
from discord.ext.commands.errors import (MissingRequiredArgument, CommandNotFound)

active_sessions = {}
parser = libluci2.Parser()
embedder = embed_generator.Embedder()
intents = discord.Intents.all()
bot = commands.Bot(command_prefix=';;', intents=intents)

bot.remove_command('help')

@bot.event
async def on_ready():
    print('Bot status: Online')

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, CommandNotFound):
        await ctx.send(embed=embedder.error_embed(error))
    if isinstance(error, MissingRequiredArgument):
        await ctx.send(embed=embedder.error_embed(error))        
    else:raise error


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
        embed = embedder.error_embed("❎ id is not defined")
        await ctx.send(embed=embed)
        return

    try:
        db_type = sesssion["type"]
    except KeyError:
        embed = embedder.error_embed("❎ type is not defined")
        await ctx.send(embed=embed)
        return
    
    data = parser.parseGenbank(item_id, db_type)
    try:
        embed = embedder.getFunction_embed(data, module_name)
        await ctx.send(embed=embed)
    except KeyError:
        embed = embedder.error_embed(f"❎ Module with '{module_name}' key is not defined")
        await ctx.send(embed=embed)
        return

@bot.command()
async def help(ctx, module='default'):
    await ctx.send(embed=embedder.help_embed(module))

@bot.command()
async def source(ctx):
    await ctx.send(embed=embedder.source_embed())

@bot.command()
async def invite(ctx):
    await ctx.send(embed=embedder.invite_embed())

token = os.environ.get('BOT_TOKEN')
start_server()
bot.run(token)