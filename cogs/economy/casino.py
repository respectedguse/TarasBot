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

class casino(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(name = "casino", description="Зіграти в казіно")
    @commands.guild_only()
    async def casinos(self, ctx, money:int=commands.Param(description="Поставте ставку!(Мінімальна 50₴)")):
        with open('data/economy/banking_system.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
        with open('data/logs/logs.json', 'r') as f1:
            logs = json.load(f1)

        idl = []
        for id in logs:
            idl.append(f"{id}")
        if f"{ctx.guild.id}" not in idl:
            logs[f'{ctx.guild.id}'] = {}
            logs[f'{ctx.guild.id}']['member_update'] = "None"
            logs[f'{ctx.guild.id}']['message_update'] = "None"
            logs[f'{ctx.guild.id}']['moderations'] = "None"
            logs[f'{ctx.guild.id}']['role_update'] = "None"
            logs[f'{ctx.guild.id}']['guild_update'] = "None"
            logs[f'{ctx.guild.id}']['channel_update'] = "None"
            logs[f'{ctx.guild.id}']['economy_updates'] = "None"

            with open('data/logs/logs.json', 'w') as wl:
                json.dump(logs, wl, indent=4)
                        
        serverlist = []
        for ids in data:
            serverlist.append(ids)

        if f"{ctx.guild.id}" not in serverlist:
            data[f'{ctx.guild.id}'] = {}
                
        idmb = []
        for idm in data[f'{ctx.guild.id}']:
            idmb.append(idm)

        if f"{ctx.author.id}" not in idmb:
            numbers = "0123456789"

            first = "".join(random.sample(numbers, 4))
            second = "".join(random.sample(numbers, 4))
            third = "".join(random.sample(numbers, 4))
            fourth = "".join(random.sample(numbers, 4))

            data[f'{ctx.guild.id}'][f'{ctx.author.id}'] = {}
            data[f'{ctx.guild.id}'][f'{ctx.author.id}']['cash'] =  0
            data[f'{ctx.guild.id}'][f'{ctx.author.id}']['bank'] = 0
            data[f'{ctx.guild.id}'][f'{ctx.author.id}']['date'] = datetime.datetime.today().strftime('%D %H:%M')
            data[f'{ctx.guild.id}'][f'{ctx.author.id}']['number'] = f"{first} {second} {third} {fourth}"
        
        if money < 50:
            await ctx.send("Мінімальна ставка 50₴!", ephemeral=True)
        else:
            if data[f'{ctx.guild.id}'][f'{ctx.author.id}']['cash'] - money >= 0:
                var1 = [
                    "💵💮🎲\n🪙🪙🪙\n🃏🎴🧲",
                    "💵🧲🃏\n🎲🎲🎲\n💰🎲💎"
                ]

                var2 = [
                    "🃏🃏💮\n🧲💮🎴\n💵💮💎",
                    "🧲💵🪙\n🪙💎💎\n💎🎴🎴",
                    "🎲🎲🪙\n🃏🃏💵\n💮💎🃏",
                    "💰🎲💎\n🧲🧲💰\n🪙💵🧲",
                    "🧲🃏💮\n🃏🪙🪙\n🪙💎🎴"
                ]

                var3=[
                    "🪙💵💵\n🃏🃏💮\n💎🎴🎴",
                    "💵🪙💵\n🧲🧲💰\n🃏💮🎲",
                    "🪙🧲🃏\n🧲💮🎴\n🃏💮🎲",
                    "💮🎲🧲\n🧲🃏💮\n🪙🪙💵",
                    "🪙💮🎲\n🪙💵🧲\n🃏💮🎲"
                ]

                valall = random.randint(1, 3)

                if valall == 1:
                    cas1 = random.choice(var1)
                    cash1 = 5

                    money1 = money * cash1

                    emb = disnake.Embed(title="Автомат", description=f"{cas1}\n**Ви заробили {money1}₴!**", colour=disnake.Color.blue(), timestamp=ctx.created_at)
                    emb.set_footer(text = f"{config.BY_LINE}", icon_url = bot.user.display_avatar.url)
                    await ctx.send(embed=emb)

                    data[f'{ctx.guild.id}'][f'{ctx.author.id}']['cash'] = data[f'{ctx.guild.id}'][f'{ctx.author.id}']['cash'] + money1

                    if logs[f'{ctx.guild.id}']['economy_updates'] != "None":
                        channel = await bot.fetch_channel(logs[f'{ctx.guild.id}']['economy_updates'])
                        emb1 = disnake.Embed(title="Зміна балансу", description=f"Користувачу було видано `{money1}₴`", colour=disnake.Color.blue(), timestamp=ctx.created_at)
                        emb1.add_field(name="Видано:", value=f"Система казино", inline=False)
                        emb1.add_field(name="Причина:", value="Виграш", inline=False)
                        emb1.set_footer(text = f"{config.BY_LINE}", icon_url = ctx.guild.icon.url)
                        await channel.send(embed=emb1)  
                elif valall == 2:
                    cas2 = random.choice(var2)
                    cash2 = 2

                    money1 = money * cash2

                    emb = disnake.Embed(title="Автомат", description=f"{cas2}\n**Ви заробили {money1}₴!**", colour=disnake.Color.blue(), timestamp=ctx.created_at)
                    emb.set_footer(text = f"{config.BY_LINE}", icon_url = bot.user.display_avatar.url)
                    await ctx.send(embed=emb)

                    data[f'{ctx.guild.id}'][f'{ctx.author.id}']['cash'] = data[f'{ctx.guild.id}'][f'{ctx.author.id}']['cash'] + money1

                    if logs[f'{ctx.guild.id}']['economy_updates'] != "None":
                        channel = await bot.fetch_channel(logs[f'{ctx.guild.id}']['economy_updates'])
                        emb1 = disnake.Embed(title="Зміна балансу", description=f"Користувачу було видано `{money1}₴`", colour=disnake.Color.blue(), timestamp=ctx.created_at)
                        emb1.add_field(name="Видаyно:", value=f"Система казино", inline=False)
                        emb1.add_field(name="Причина:", value="Виграш", inline=False)
                        emb1.set_footer(text = f"{config.BY_LINE}", icon_url = ctx.guild.icon.url)
                        await channel.send(embed=emb1)  
                elif valall == 3:
                    cas3 = random.choice(var3)
                    emb = disnake.Embed(title="Автомат", description=f"{cas3}\n**Ви програли {money}₴!**", colour=disnake.Color.blue(), timestamp=ctx.created_at)
                    emb.set_footer(text = f"{config.BY_LINE}", icon_url = bot.user.display_avatar.url)
                    await ctx.send(embed=emb)

                    data[f'{ctx.guild.id}'][f'{ctx.author.id}']['cash'] = data[f'{ctx.guild.id}'][f'{ctx.author.id}']['cash'] - money

                    if logs[f'{ctx.guild.id}']['economy_updates'] != "None":
                        channel = await bot.fetch_channel(logs[f'{ctx.guild.id}']['economy_updates'])
                        emb1 = disnake.Embed(title="Зміна балансу", description=f"Користувачу було знято `{data[f'{ctx.guild.id}'][f'{ctx.author.id}']['cash'] - money}₴`", colour=disnake.Color.blue(), timestamp=ctx.created_at)
                        emb1.add_field(name="Знято:", value=f"Система казино", inline=False)
                        emb1.add_field(name="Причина:", value="Програш", inline=False)
                        emb1.set_footer(text = f"{config.BY_LINE}", icon_url = ctx.guild.icon.url)
                        await channel.send(embed=emb1)  
            else:
                emb = disnake.Embed(title=f"У вас нема стільки грошей!", description=f"На вашому рахунку {data[f'{ctx.guild.id}'][f'{ctx.author.id}']['cash']}₴", colour=disnake.Color.blue(), timestamp=ctx.created_at)
                emb.set_footer(text = f"{config.BY_LINE}", icon_url = bot.user.display_avatar.url)
                await ctx.send(embed = emb)

        with open('data/economy/banking_system.json', 'w') as w:
            json.dump(data, w, indent=4)

def setup(bot):
    bot.add_cog(casino(bot))