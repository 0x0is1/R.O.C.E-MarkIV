import discord

class Embedder:
    def __init__(self):
        self.default_color = 0x61afef

    def search_embed(self, term:str, data:list):
        embed = discord.Embed(title=f"Search result for term: '{term}'", color=self.default_color)
        for i, j in enumerate(data):
            embed.add_field(name=f"{i+1}. {j[0]}", value=f"Description: {j[1]}\n{j[2]}", inline=False)
        return embed
    
    def getFunction_embed(self, data:dict, module_name:str):
        embed = discord.Embed(title=f"{data['LOCUS']}", color=self.default_color)
        if module_name != "all":
            res = {
                key: val for key, val in data.items()
                if key.startswith(module_name.upper())
            }
        else:
            res = data
        if len(res) != 0:
            for i in res.keys():
                embed.add_field(name=i, value=f"```css\n{res[i][:999]}\n```", inline=False)
            return embed
        return self.error_embed(f"No result found for key '{module_name}'")
    
    def error_embed(this, message:str):
        embed = discord.Embed(title="Error", color=0xf15f46)
        embed.add_field(name="Exception occured", value=f"```css\n{message}\n```", inline=False)
        return embed
