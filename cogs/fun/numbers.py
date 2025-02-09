import disnake
from disnake.ext import commands
from disnake import TextInputStyle
from difflib import SequenceMatcher
from disnake.ui import Button, View
import json
import random
import datetime
import time
import config
import sys
sys.path.insert(0, f'{config.CD}')
import main

bot = main.bot

class CodeModal(disnake.ui.Modal):
    def __init__(self):
        comp = [
            disnake.ui.TextInput(
                label="Загадайте код(4 цифри!)",
                placeholder="Напр. 4444",
                style=TextInputStyle.short,
                min_length=4,
                max_length=4,
                custom_id="code"
            )
        ]
        super().__init__(title="Гра <<Вгадай код>>", components=comp)

    async def callback(self, interaction: disnake.ModalInteraction):
        numbers = ["0","1","2","3","4","5","6","7","8","9"]
        if interaction.text_values['code'][0] in numbers and interaction.text_values['code'][1] in numbers and interaction.text_values['code'][2] in numbers and interaction.text_values['code'][3] in numbers:
            with open('data/games/numbers.json', 'r') as f:
                data = json.load(f)

            author = None
            for author_id in data:
                try:
                    if data[f'{author_id}']['friend_id'] == interaction.user.id:
                        author=author_id
                except:
                    pass

            data[f'{author_id}']['code_friend']['1'] = f"{interaction.text_values['code'][0]}"
            data[f'{author_id}']['code_friend']['2'] = f"{interaction.text_values['code'][1]}"
            data[f'{author_id}']['code_friend']['3'] = f"{interaction.text_values['code'][2]}"
            data[f'{author_id}']['code_friend']['4'] = f"{interaction.text_values['code'][3]}"

            with open('data/games/numbers.json', 'w') as w:
                json.dump(data, w, indent=4)

            emb = disnake.Embed(title="🔢Вгадай код🔢", description=f"{interaction.author.mention}, Ви успішно прийняли виклик та загадали код!\n\n{bot.get_user(int(author_id)).mention}, {interaction.author.mention},  у Вас є по 10 спроб, щоб вгадати коди друг друга. Щасти!", colour=disnake.Color.blue(), timestamp=interaction.created_at)
            emb.set_footer(text = f"{config.BY_LINE}", icon_url = bot.user.display_avatar.url)
            await interaction.response.send_message(embed=emb)

            await interaction.send("Код успішно загадано!")

class MyView_challenge(disnake.ui.View):
    def __init__(self):
        super().__init__(timeout=120)

    @disnake.ui.button(label="Прийняти виклик та загадати код", disabled=False, style=disnake.ButtonStyle.success)
    async def button_callback_1(self, button, interaction:disnake.AppCmdInter):
        if interaction.user.id != code_log.friend_id:
            await interaction.response.send_message("Ви не можете прийняти виклик, оскільки ця кнопка не для вас!", ephemeral=True)
        else:
            await interaction.response.send_modal(modal=CodeModal())

class code_log():
    friend_id = None
    numbers = {
            "0":"zero",
            "1":"one",
            "2":"two",
            "3":"three",
            "4":"four",
            "5":"five",
            "6":"six",
            "7":"seven",
            "8":"eight",
            "9":"nine"
        }

def similarity(a,b):
    return SequenceMatcher(None, a, b).ratio()

class numbers(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(name="numbers", description="Гра - Вгадай код")
    @commands.guild_only()
    async def numbers_game(self, ctx):
        with open('data/economy/banking_system.json', 'r', encoding='utf-8') as f1:
            data_economy = json.load(f1)

        async def no_guild_data():
            data_economy[f'{ctx.guild.id}'] = {}
            with open('data/economy/banking_system.json', 'w') as w:
                json.dump(data_economy, w, indent=4)

        async def no_data():
            numbers = "0123456789"
            first = "".join(random.sample(numbers, 4))
            second = "".join(random.sample(numbers, 4))
            third = "".join(random.sample(numbers, 4))
            fourth = "".join(random.sample(numbers, 4))
            data_economy[f'{ctx.guild.id}'][f'{ctx.author.id}'] = {}
            data_economy[f'{ctx.guild.id}'][f'{ctx.author.id}']['cash'] =  0
            data_economy[f'{ctx.guild.id}'][f'{ctx.author.id}']['bank'] = 0
            data_economy[f'{ctx.guild.id}'][f'{ctx.author.id}']['date'] = datetime.datetime.today().strftime('%m/%d')
            data_economy[f'{ctx.guild.id}'][f'{ctx.author.id}']['number'] = f"{first} {second} {third} {fourth}"
            with open('data/economy/banking_system.json', 'w') as w:
                json.dump(data_economy, w, indent=4)

        serverlist = []
        for ids in data_economy:
            serverlist.append(ids)
        if f"{ctx.guild.id}" not in serverlist:
            await no_guild_data()

        idmb = []
        for idm in data_economy[f'{ctx.guild.id}']:
            idmb.append(idm)
        if f"{ctx.author.id}" not in idmb:
            await no_data()

    @numbers_game.sub_command(description="Пограй в гру <<Відгадай код>> самостійно")
    @commands.guild_only()
    async def alone(self, ctx):
        with open('data/others/emojies.json', 'r') as f:
            data_emoji = json.load(f)
        with open('data/games/numbers.json', 'r') as f2:
            data = json.load(f2)

        data[f'{ctx.author.id}'] = {}
        data[f'{ctx.author.id}']['start_time'] = time.time()
        data[f'{ctx.author.id}']['status'] = 0
        data[f'{ctx.author.id}']['author_tries'] = 0
        data[f'{ctx.author.id}']['code'] = {}
        data[f'{ctx.author.id}']['code']['1'] = f"{random.randint(0,9)}"
        data[f'{ctx.author.id}']['code']['2'] = f"{random.randint(0,9)}"
        data[f'{ctx.author.id}']['code']['3'] = f"{random.randint(0,9)}"
        data[f'{ctx.author.id}']['code']['4'] = f"{random.randint(0,9)}"

        with open('data/games/numbers.json', 'w', ) as w1:
            json.dump(data, w1, indent=4)

        emb = disnake.Embed(title="🔢Вгадай код🔢", description="Код задано! Спробуйте його вгадати🫣\n\nВам дається по 40 секунд на відповідь! У вас є 10 спроб, щоб розгадати код! Щасти!", colour=disnake.Color.blue(), timestamp=ctx.created_at)
        emb.set_footer(text = f"{config.BY_LINE}", icon_url = bot.user.display_avatar.url)
        await ctx.send(embed=emb) 
        
        print(data[f'{ctx.author.id}']['code'])
        while data[f'{ctx.author.id}']['author_tries']<10 or data[f'{ctx.author.id}']['status'] == 0:
            def check_answer(msg):
                return msg.author == ctx.author and msg.channel == ctx.channel

            try:
                msg = await bot.wait_for("message", timeout=40.0, check=check_answer)
            except:
                emb = disnake.Embed(title="Час вийшов😢", description=f"Відповідь не надіслано :(", colour=disnake.Color.blue(), timestamp=ctx.created_at)
                emb.set_footer(text = f"{config.BY_LINE}", icon_url=bot.user.display_avatar)
                await ctx.send(embed=emb)
                return
            
            if len(msg.content) == 4:
                numbers = ["0","1","2","3","4","5","6","7","8","9"]

                if msg.content[0] in numbers and msg.content[1] in numbers and msg.content[2] in numbers and msg.content[3] in numbers:
                    simil = {
                        0:"",
                        1:"",
                        2:"",
                        3:""
                    }

                    for m_c in [0,1,2,3]:
                        for n in code_log.numbers:
                            if msg.content[m_c] == n:
                                simil[m_c] = code_log.numbers[f'{n}']

                    answer = ""
                    if msg.content[0]==data[f'{ctx.author.id}']['code']['1']:
                        answer += f"<:number_{simil[0]}_green:{data_emoji[f'number_{simil[0]}_green']['ID']}>"
                    elif msg.content[0]==data[f'{ctx.author.id}']['code']['2'] or msg.content[0]==data[f'{ctx.author.id}']['code']['3'] or msg.content[0]==data[f'{ctx.author.id}']['code']['4']:
                        answer += f"<:number_{simil[0]}_yellow:{data_emoji[f'number_{simil[0]}_yellow']['ID']}>"
                    else:
                        answer += f"<:number_{simil[0]}_red:{data_emoji[f'number_{simil[0]}_red']['ID']}>"
                    if msg.content[1]==data[f'{ctx.author.id}']['code']['2']:
                        answer += f"<:number_{simil[1]}_green:{data_emoji[f'number_{simil[1]}_green']['ID']}>"
                    elif msg.content[1]==data[f'{ctx.author.id}']['code']['1'] or msg.content[1]==data[f'{ctx.author.id}']['code']['3'] or msg.content[1]==data[f'{ctx.author.id}']['code']['4']:
                        answer += f"<:number_{simil[1]}_yellow:{data_emoji[f'number_{simil[1]}_yellow']['ID']}>"
                    else:
                        answer += f"<:number_{simil[1]}_red:{data_emoji[f'number_{simil[1]}_red']['ID']}>"
                    if msg.content[2]==data[f'{ctx.author.id}']['code']['3']:
                        answer += f"<:number_{simil[2]}_green:{data_emoji[f'number_{simil[2]}_green']['ID']}>"
                    elif msg.content[2]==data[f'{ctx.author.id}']['code']['2'] or msg.content[2]==data[f'{ctx.author.id}']['code']['1'] or msg.content[2]==data[f'{ctx.author.id}']['code']['4']:
                        answer += f"<:number_{simil[2]}_yellow:{data_emoji[f'number_{simil[2]}_yellow']['ID']}>"
                    else:
                        answer += f"<:number_{simil[2]}_red:{data_emoji[f'number_{simil[2]}_red']['ID']}>"
                    if msg.content[3]==data[f'{ctx.author.id}']['code']['4']:
                        answer += f"<:number_{simil[3]}_green:{data_emoji[f'number_{simil[3]}_green']['ID']}>"
                    elif msg.content[3]==data[f'{ctx.author.id}']['code']['2'] or msg.content[3]==data[f'{ctx.author.id}']['code']['3'] or msg.content[3]==data[f'{ctx.author.id}']['code']['1']:
                        answer += f"<:number_{simil[3]}_yellow:{data_emoji[f'number_{simil[3]}_yellow']['ID']}>"
                    else:
                        answer += f"<:number_{simil[3]}_red:{data_emoji[f'number_{simil[3]}_red']['ID']}>"

                    emb = disnake.Embed(title="🔢Вгадай код🔢", description=f"{answer}", colour=disnake.Color.blue(), timestamp=ctx.created_at)
                    emb.set_footer(text = f"{config.BY_LINE}", icon_url = bot.user.display_avatar.url)
                    await ctx.send(embed=emb)

                    data[f'{ctx.author.id}']['author_tries']+=1

                    with open('data/games/numbers.json', 'w', ) as w1:
                        json.dump(data, w1, indent=4)

                    if msg.content[0]==data[f'{ctx.author.id}']['code']['1'] and msg.content[1]==data[f'{ctx.author.id}']['code']['2'] and msg.content[2]==data[f'{ctx.author.id}']['code']['3'] and msg.content[3]==data[f'{ctx.author.id}']['code']['4']:
                        with open('data/economy/banking_system.json', 'r', encoding='utf-8') as f1:
                            data_economy = json.load(f1)

                        mn = 0
                        if data_economy[f'{ctx.guild.id}'][f'{ctx.author.id}']['cash']+1000<=100000000:
                            if data[f'{ctx.author.id}']['author_tries']<=2:
                                data_economy[f'{ctx.guild.id}'][f'{ctx.author.id}'][f'cash'] += 1000
                                mn+=1000
                            elif data[f'{ctx.author.id}']['author_tries']>2 and data[f'{ctx.author.id}']['author_tries']<=4:
                                data_economy[f'{ctx.guild.id}'][f'{ctx.author.id}'][f'cash'] += 800
                                mn+=800
                            elif data[f'{ctx.author.id}']['author_tries']>4 and data[f'{ctx.author.id}']['author_tries']<=6:
                                data_economy[f'{ctx.guild.id}'][f'{ctx.author.id}'][f'cash'] += 600
                                mn+=600
                            elif data[f'{ctx.author.id}']['author_tries']>6 and data[f'{ctx.author.id}']['author_tries']<=8:
                                data_economy[f'{ctx.guild.id}'][f'{ctx.author.id}'][f'cash'] += 400
                                mn+=400
                            elif data[f'{ctx.author.id}']['author_tries']>8 and data[f'{ctx.author.id}']['author_tries']<10:
                                data_economy[f'{ctx.guild.id}'][f'{ctx.author.id}'][f'cash'] += 200
                                mn+=200

                        with open('data/economy/banking_system.json', 'w') as w:
                            json.dump(data_economy, w, indent=4)
                        
                        emb = disnake.Embed(title="🔢Вгадай код🔢", description=f"**Вітаю! Ви вгадали код!**", colour=disnake.Color.blue(), timestamp=ctx.created_at)
                        emb.add_field(name="Код:", value=f"{answer}", inline=False)
                        emb.add_field(name="Ваша нагорода:", value=f"**{mn}₴**", inline=False)
                        emb.set_footer(text = f"{config.BY_LINE}", icon_url = bot.user.display_avatar.url)
                        await ctx.send(embed=emb)

                        data[f'{ctx.author.id}']['author_tries']=11
                        data[f'{ctx.author.id}']['status']=1

                        with open('data/games/numbers.json', 'w', ) as w1:
                            json.dump(data, w1, indent=4)
                else:
                    await ctx.send("У відповіді повинні міститися лише 4 цифри!", ephemeral=True)
            else:
                await ctx.send("Ваша відповідь повинна складатися з 4 цифр! Не більше і не менше!", ephemeral=True)

        if data[f'{ctx.author.id}']['author_tries']==10:
            emb = disnake.Embed(title="🔢Вгадай код🔢", description=f"На жаль, ви не відгадали код :(\nСпробуйте ще раз!", colour=disnake.Color.blue(), timestamp=ctx.created_at)
            emb.set_footer(text = f"{config.BY_LINE}", icon_url = bot.user.display_avatar.url)
            await ctx.send(embed=emb)

            data[f'{ctx.author.id}']['status']=1
            with open('data/games/numbers.json', 'w', ) as w1:
                json.dump(data, w1, indent=4)

        if data[f'{ctx.author.id}']['status']==1:
            data.pop(f'{ctx.author.id}')
            with open('data/games/numbers.json', 'w', ) as w1:
                json.dump(data, w1, indent=4)
    
    @numbers_game.sub_command(description="Запроси друга пограти в гру <<Відгадай код>>")
    @commands.guild_only()
    async def friend(self, inter, member:disnake.Member=commands.Param(description="Вкажіть користувача, якого хочете запросити до гри!"), code:str=commands.Param(description="Загадайте код користувачу(4 цифри!)", min_length=4, max_length=4)):
        if member.id == inter.author.id:
            await inter.response.send_message("Ви не можете надіслати запит на гру самому собі!", ephemeral=True)
        elif member.bot == True:
            await inter.response.send_message("Ви не можете запропонувати пограти в гру ботові!", ephemeral=True)
        else:
            if len(code) == 4:
                numbers = ["0","1","2","3","4","5","6","7","8","9"]
                if code[0] in numbers and code[1] in numbers and code[2] in numbers and code[3] in numbers:
                    with open('data/games/numbers.json', 'r') as f2:
                        data = json.load(f2)

                    code_log.friend_id = member.id
                    
                    data[f'{inter.author.id}'] = {}
                    data[f'{inter.author.id}']['start_time'] = f"{time.time()}"
                    data[f'{inter.author.id}']['author_tries'] = 0
                    data[f'{inter.author.id}']['friend_tries'] = 0
                    data[f'{inter.author.id}']['friend_id'] = member.id
                    data[f'{inter.author.id}']['code'] = {}
                    data[f'{inter.author.id}']['code']['1'] = code[0]
                    data[f'{inter.author.id}']['code']['2'] = code[1]
                    data[f'{inter.author.id}']['code']['3'] = code[2]
                    data[f'{inter.author.id}']['code']['4'] = code[3]
                    data[f'{inter.author.id}']['code_friend'] = {}

                    with open('data/games/numbers.json', 'w') as w1:
                        json.dump(data, w1, indent=4)

                    emb = disnake.Embed(title="🔢Вгадай код🔢", description=f"{member.mention}, тебе запросив {inter.author.mention} пограти в гру **<<Вгадай код>>**!\nУ вас є 2 хвилини, щоб прийняти виклик!", colour=disnake.Color.blue(), timestamp=inter.created_at)
                    emb.set_footer(text = f"{config.BY_LINE}", icon_url = bot.user.display_avatar.url)
                    await inter.response.send_message(f"{member.mention}",embed=emb, view=MyView_challenge())

                    try:
                        emb = disnake.Embed(title="🔢Вгадай код🔢", description=f"Привіт ***{member.name}***! Тебе запросив ***{inter.author.name}*** пограти в гру **<<Вгадай код>>** на сервері ***{inter.guild.name}***!\nПрийми виклик!(Щоб прийняти виклик у вас є 2 хвилини!)", colour=disnake.Color.blue(), timestamp=inter.created_at)
                        emb.set_footer(text = f"{config.BY_LINE}", icon_url = bot.user.display_avatar.url)
                        await member.send(embed=emb)

                        await inter.send(f"Користувачу {member.mention} було надіслано запрошення! Протягом двох хвилин, запрошення буде дійсним!", ephemeral=True)
                    except disnake.Forbidden:
                        await inter.response.send_message(f"Користувачу {member.mention} було надіслано запрошення в приватні повідомлення:(, оскільки в користувача закриті приватні повідомлення!", ephemeral=True)
                else:
                    await inter.response.send_message("Код повинен містити лише цифри! Використайте команду знову й вкажіть правильний код!", ephemeral=True)
            else:
                await inter.response.send_message("Код повинен містити 4 цифри!", ephemeral=True)

def setup(bot):
    bot.add_cog(numbers(bot))