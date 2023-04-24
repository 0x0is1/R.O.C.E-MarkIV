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
    
    def error_embed(self, message:str):
        embed = discord.Embed(title="Error", color=0xf15f46)
        embed.add_field(name="Exception occured", value=f"```css\n{message}\n```", inline=False)
        return embed

    def help_embed(self, help_module:str):
        embed = discord.Embed(title="Help", color=self.default_color)
        if help_module == "default":
            embed.add_field(name="Commands", 
            value="`set` : sets parameters to get data\n`get` : gets data\n`search`: search module\ntype `help <module type>` to get help for specific command",
            inline=False)
            return embed
        if help_module == 'set':
            embed.add_field(name="set help", value="module available for set command.")
            embed.add_field(
                name='Description:', value="use for setting item id and item type.")
            embed.add_field(name='Example: ', value='`set id 1798174254` and `set type nuccore`')
            embed.add_field(name='Options for item type:', value="Nucleotide (`nuccore`)\nGenes (`gene`)\nProtein (`protein`)\nProbe (`probe`)\nPopset(`popset`)")
            embed.add_field(name='Options for item id:', value="use `search <item type> <item name>` to get ids.")
            return embed

        if help_module == 'get':
            embed.add_field(
                name="get help", value="module available for get command.")
            embed.add_field(
                name='Description:', value="use for getting data for saved item id and item type.")
            embed.add_field(
                name='Example: ', value='`get gene`, `get cds` etc.')
            embed.add_field(name='Accessible fields:', value='''"LOCUS",
        DEFINITION, ACCESSION, VERSION, KEYWORDS, SOURCE, REFERENCE, COMMENT, REMARK, PRIMARY, FEATURES, ORIGIN''', inline=False)
            return embed

        if help_module == 'search':
            embed.add_field(
                name="search help", value="module available for search command.")
            embed.add_field(
                name='Description:', value="use for searching data for specific detail type.")
            embed.add_field(
                name='Example: ', value='`search nuccore SARS`, `search gene rept` etc.')
            return embed
        else:
            embed=self.error_embed("Info for given module is not available.")
            return embed
    
    def invite_embed(self):
        embed = discord.Embed(title='MarkIV Invite',
                            url='https://discord.com/oauth2/authorize?client_id=798966300448784425&permissions=8&scope=bot',
                            description='Invite MarkIV on your server.')
        return embed


    def source_embed(self):
        source_code = 'https://github.com/0x0is1/R.O.C.E-MarkIV'
        embed = discord.Embed(title='MarkIV Source code',
                            url=source_code,
                            description='Visit MarkIV on github')
        return embed
