import disnake
from disnake.ext import commands
import json
import random
import datetime
import config
import sys
sys.path.insert(0, f'{config.CD}')
import main

bot = main.bot

class addmoney(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(name = "add_money", description="Видати гроші користувачу")
    @commands.guild_only()
    async def addmoneys(self, ctx, member:disnake.Member = commands.Param(description="Вкажіть користувача"), type: str = commands.Param(description="Виберіть куди додати гроші", choices=["bank", "cash"]), money:int=commands.Param(description="Вкажіть кількість грошей для видачі")):
        if ctx.author.guild_permissions.administrator:
            if member.bot:
                await ctx.send("Бот не може мати банківського рахунку!", ephemeral=True)
            else:
                with open('data/economy/banking_system.json', 'r', encoding='utf-8') as f:
                    data = json.load(f)

                async def no_guild_data():
                    data[f'{ctx.guild.id}'] = {}

                    with open('data/economy/banking_system.json', 'w') as w:
                        json.dump(data, w, indent=4)
            
                async def no_data():
                    numbers = "0123456789"

                    first = "".join(random.sample(numbers, 4))
                    second = "".join(random.sample(numbers, 4))
                    third = "".join(random.sample(numbers, 4))
                    fourth = "".join(random.sample(numbers, 4))

                    data[f'{ctx.guild.id}'][f'{member.id}'] = {}
                    data[f'{ctx.guild.id}'][f'{member.id}']['cash'] =  0
                    data[f'{ctx.guild.id}'][f'{member.id}']['bank'] = 0
                    data[f'{ctx.guild.id}'][f'{member.id}']['date'] = datetime.datetime.today().strftime('%m/%d')
                    data[f'{ctx.guild.id}'][f'{member.id}']['number'] = f"{first} {second} {third} {fourth}"

                    with open('data/economy/banking_system.json', 'w') as w:
                        json.dump(data, w, indent=4)
                        
                serverlist = []
                for ids in data:
                    serverlist.append(ids)
                if f"{ctx.guild.id}" not in serverlist:
                    await no_guild_data()
                
                idmb = []
                for idm in data[f'{ctx.guild.id}']:
                    idmb.append(idm)
                if f"{member.id}" not in idmb:
                    await no_data()

                if type == "cash":
                    mn = data[f'{ctx.guild.id}'][f'{member.id}']['cash'] + money
                    if mn > 100000000:
                        await ctx.send(f"Ліміт на руках не може перевищувати 100.000.000₴. Користувач {member.name} має {data[f'{ctx.guild.id}'][f'{member.id}']['cash']}₴.\nВидайте ту кількість грошей, щоб не перевищувало ліміт!", ephemeral=True)
                    else:
                        data[f'{ctx.guild.id}'][f'{member.id}']['cash'] = mn
                                    
                        emb = disnake.Embed(title=f"Видача грошей",description=f"Користувачу {member.mention} було видано `{money}₴`", colour=disnake.Color.blue(), timestamp=ctx.created_at)
                        emb.set_footer(text = f"{config.BY_LINE}", icon_url = bot.user.display_avatar.url)
                        await ctx.send(embed=emb)

                        with open('data/economy/banking_system.json', 'w') as w:
                            json.dump(data, w, indent=4)
                elif type == "bank":
                    mn = data[f'{ctx.guild.id}'][f'{member.id}']['bank'] + money
                    if mn > 100000000:
                        await ctx.send(f"Ліміт на банківському рахунку не може перевищувати 100.000.000₴. Користувач {member.name} має {data[f'{ctx.guild.id}'][f'{member.id}']['bank']}₴.\nВидайте ту кількість грошей, щоб не перевищувало ліміт!", ephemeral=True)
                    else:
                        data[f'{ctx.guild.id}'][f'{member.id}']['bank'] = mn
                                
                        emb = disnake.Embed(title=f"Видача грошей",description=f"Користувачу {member.mention} було видано {money}₴ на банківський рахунок.", colour=disnake.Color.blue(), timestamp=ctx.created_at)
                        emb.set_footer(text = f"{config.BY_LINE}", icon_url = bot.user.display_avatar.url)
                        await ctx.send(embed=emb) 
                    
                        with open('data/economy/banking_system.json', 'w') as w:
                            json.dump(data, w, indent=4)
                
        else:
            await ctx.send("Ви маєте дозволи нижче, аніж потрібні або ви не є модератором!", ephemeral=True)

def setup(bot):
    bot.add_cog(addmoney(bot))