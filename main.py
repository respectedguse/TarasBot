import disnake
import os
import config
import json
import datetime
import time
import random
import logging
import keep_alive
from disnake.ui import Select, Button, View
from disnake.ext import commands, tasks

bot = commands.Bot(command_prefix = "!", intents=disnake.Intents.all())
bot.remove_slash_command('help')

#logger = logging.getLogger()
#logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s", datefmt="%Y/%m/%d %H:%M:%S", filename="technical/logs.log", encoding='utf-8')

with open('data/technical/settings.json', 'r') as file:
    settings = json.load(file)

@bot.event
async def on_ready():
    with open('data/technical/bot.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    with open('data/technical/settings.json', 'r') as f1:
        datas = json.load(f1)
    
    channel = await bot.fetch_channel(datas['start-work'])

    #logger.info("[+]System start work![+]")
    print("[+]Система рахування часу роботи оновлено![+]")
    print("[+]Статус оновлено![+]")
    print("[!]TaraBot 2024© start work[!]")
    #await channel.send(f"{bot.user.mention} start work\n{datetime.datetime.today().strftime('%D %H:%M')}")

    data['working']['timework'] = 0
    data['working']['days'] = 0
    data['working']['hours'] = 0
    data['working']['minutes'] = 0
    data['working']['seconds'] = 0

    with open('data/technical/bot.json', 'w') as w2:
        json.dump(data, w2, indent=5)

    status.start()
    timework.start()
    count.start()
    bad_words.start()

@tasks.loop(seconds = 20)
async def status():
    with open('data/technical/bot.json', 'r') as f:
        data = json.load(f)
    

    status=[
            "In developing"
        ]
    await bot.change_presence(status=disnake.Status.idle,activity=disnake.Game(name=f"{random.choice(status)}"))

@tasks.loop(seconds = 5)
async def timework():
    with open('data/technical/bot.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    sec = data['working']['seconds'] + 5

    data['working']['seconds'] = sec
    data['working']['timework'] = data['working']['timework'] + 5

    if sec == 60:
        data['working']['seconds'] = 0
        data['working']['minutes'] = data['working']['minutes'] + 1
    elif data['working']['minutes'] == 60:
        data['working']['minutes'] = 0
        data['working']['hours'] = data['working']['hours'] + 1
    elif data['working']['hours'] == 24:
        data['working']['hours'] = 0
        data['working']['days'] = data['working']['days'] + 1
    
    with open('data/technical/bot.json', 'w', encoding='utf-8') as w:
        json.dump(data, w, indent = 5)
    
@tasks.loop(minutes = 10)
async def count():
    with open('data/technical/bot.json', 'r') as f:
        data = json.load(f)
    
    memberlist = []
    for g in bot.guilds:
        for m in g.members:
            if m.bot is not True:
                memberlist.append(m)

    data['bot']['guilds'] = len(bot.guilds)
    data['bot']['members'] = len(memberlist)

    with open('data/technical/bot.json', 'w', encoding='utf-8') as w:
        json.dump(data, w, indent = 5)

@tasks.loop(minutes=5)
async def bad_words():
    with open('data/bad words/words.json', 'r') as f1:
        words = json.load(f1)
    with open('data/bad words/guilds.json', 'r') as f2:
        guilds = json.load(f2)
    
    
    gwords = []
    for guild in words:
        gwords.append(f"{guild}")
    guilds['guilds'] = gwords
    
    with open('data/bad words/guilds.json', 'w') as w:
        json.dump(guilds, w, indent=2)

@bot.slash_command(name = "load", guild_ids=settings['guilds'])
async def load(ctx, extension):
    if ctx.author.id in settings['members']:
        extension = extension.lower()
        bot.load_extension(f'cogs.{extension}')
        await ctx.send(f'***{extension}*** завантажено!')
        print(f"[+]Ког {extension} завантажено[+]")
    else:
        await ctx.send("У вас немає можливості використовувати цю команду!", ephemeral=True)

@bot.slash_command(name = "unload", guild_ids=settings['guilds'])
async def unload(ctx, extension):
    if ctx.author.id in settings['members']:
        extension = extension.lower()
        bot.unload_extension(f'cogs.{extension}')
        await ctx.send(f'***{extension}*** вивантажано!')
        print(f"[-]Ког {extension} вивантажено[-]")
    else:
        await ctx.send("У вас немає можливості використовувати цю команду!", ephemeral=True)

@bot.slash_command(name = "reload", guild_ids=settings['guilds'])
async def reload(ctx, extension):
    if ctx.author.id in settings['members']:
        extension = extension.lower()
        bot.unload_extension(f'cogs.{extension}')
        bot.load_extension(f'cogs.{extension}')
        await ctx.send(f'***{extension}*** перезавантажено!!')
        print(f"[+]Ког {extension} перезавантажено[+]")
    else:
        await ctx.send("У вас немає можливості використовувати цю команду!", ephemeral=True)

@bot.slash_command(name = "reload_all", guild_ids=settings['guilds'])
async def reloadall(ctx):
    if ctx.author.id in settings['members']:
        for folder in os.listdir("./cogs"):
            for filename in os.listdir(f"./cogs/{folder}"):
                if filename.endswith(".py") and not filename.startswith("_"):
                    bot.unload_extension(f"cogs.{folder}.{filename[:-3]}") 
                    bot.load_extension(f"cogs.{folder}.{filename[:-3]}") 
        await ctx.send("Файли були перезавантажені!")
        print(f"[+]Когі були перезавантажені![+]")
    else:
        await ctx.send("У вас немає можливості використовувати цю команду!", ephemeral=True)

@bot.slash_command(name = "cogs", guild_ids=settings['guilds'])
async def cogs(ctx):
    if ctx.author.id in settings['members']:
        files = ""
        text = ""
        for folder in os.listdir("./cogs"):
            for filename in os.listdir(f"./cogs/{folder}"):
                if filename.endswith(".py") and not filename.startswith("_"):
                    files += f"{filename}, "

            text += f"**{folder}**:\n{files}\n\n"
            files = ""

        option = []
        for folder in os.listdir("./cogs"):
            option.append(disnake.SelectOption(label=f"{folder}"))

        select_all_cogs = Select(
            placeholder="Choose tha category",
            options=option
        )

        view = View()
        view.add_item(select_all_cogs)

        emb = disnake.Embed(title = "All cogs", description=f"{text}", color=disnake.Color.random())
        await ctx.send(embed = emb, view=view)
    else:
        await ctx.send("У вас немає можливості використовувати цю команду!", ephemeral=True)

for folder in os.listdir("./cogs"):
    for filename in os.listdir(f"./cogs/{folder}"):
        if filename.endswith(".py") and not filename.startswith("_"):
            bot.load_extension(f"cogs.{folder}.{filename[:-3]}")
            #time.sleep(0.1) 

print("[+]Когі завантажено![+]")

#keep_alive.keep_alive()

bot.run(config.TOKEN)