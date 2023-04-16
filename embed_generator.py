#     embed = discord.Embed(title="Rational Operative Communication Entity - Mark II", color=0x03f8fc)
# embed.add_field(name="Description:", value="This bot is designed for genetic engineering research purpose.", inline=False)

import discord

class Embedder:
    def __init__(self):
        self.default_color = 0x61afef

    def search_embed(self, term:str, data:list):
        embed = discord.Embed(title=f"Search result for term: '{term}'", color=self.default_color)
        for i, j in enumerate(data):
            embed.add_field(name=f"{i+1}. {j[0]}", value=f"Description: {j[1]}\n{j[2]}", inline=False)
        return embed
    
    def setFunction_embed(self):
        _
    
    def getFunction_embed(self):
        _