import disnake
from disnake.ext import commands
from disnake import TextInputStyle
from disnake.ui import Button, View
import json
import random
import datetime
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO
import math
import time
import config
import sys
sys.path.insert(0, f'{config.CD}')
import main

bot = main.bot

class NoInfoDate():
#Додавання до бази даних користувача
    member = None
    guild = None
    
    async def check_user_data():
        with open('data/economy/banking_system.json', 'r', encoding='utf-8') as f:
            data = json.load(f)

        members = []
        for m in data[f'{NoInfoDate.guild.id}']:
            members.append(f"{m}")
        if f"{NoInfoDate.member.id}" not in members:
            await NoInfoDate.no_data()
        return        

    async def no_data():
        with open('data/economy/banking_system.json', 'r', encoding='utf-8') as f:
            data = json.load(f)

        numbers = "0123456789"

        first = "".join(random.sample(numbers, 4))
        second = "".join(random.sample(numbers, 4))
        third = "".join(random.sample(numbers, 4))
        fourth = "".join(random.sample(numbers, 4))

        data[f'{NoInfoDate.guild.id}'][f'{NoInfoDate.member.id}'] = {}
        data[f'{NoInfoDate.guild.id}'][f'{NoInfoDate.member.id}']['cash'] = 0
        data[f'{NoInfoDate.guild.id}'][f'{NoInfoDate.member.id}']['bank'] = 0 
        data[f'{NoInfoDate.guild.id}'][f'{NoInfoDate.member.id}']['date'] = datetime.datetime.today().strftime('%m/%d')
        data[f'{NoInfoDate.guild.id}'][f'{NoInfoDate.member.id}']['number'] = f"{first} {second} {third} {fourth}"

        with open('data/economy/banking_system.json', 'w', encoding='utf-8') as w:
            json.dump(data, w, indent=4)
        return

class MyView(disnake.ui.View):#основні кнопки керування
    def __init__(self):
        super().__init__(timeout=60)

    @disnake.ui.button(emoji="💳", label="Банківська картка", disabled=False)
    async def button_callback_1_active(self, button, interaction):
        with open('data/economy/banking_system.json', 'r', encoding='utf-8') as f:
            data = json.load(f)

        await interaction.response.defer()

        font_type = 'fonts/AABebasNeue.ttf'
        bank_card = Image.open('images/banking system/template_card.png')
        draw = ImageDraw.Draw(bank_card)

        #card_number
        card_number = f"{data[f'{interaction.guild.id}'][f'{interaction.author.id}']['number']}"
        font = ImageFont.truetype(font_type, 250)
        text_width = draw.textlength(card_number, font)
        x_cd = 1108
        y_cd = 810
        draw.text((x_cd,y_cd), card_number, font=font)

        #all_money
        all_money = f"{data[f'{interaction.guild.id}'][f'{interaction.author.id}']['cash'] + data[f'{interaction.guild.id}'][f'{interaction.author.id}']['bank']}"
        font1 = ImageFont.truetype(font_type, 200)
        text_width = draw.textlength(all_money, font1)
        x_allm=450
        y_allm=1400
        draw.text((x_allm,y_allm), all_money, font=font1)

        #bank
        bank = f"{data[f'{interaction.guild.id}'][f'{interaction.author.id}']['bank']}"
        font2 = ImageFont.truetype(font_type, 200)
        text_width = draw.textlength(all_money, font1)
        x_b=1750
        y_b=1400
        draw.text((x_b,y_b), bank, font=font2)

        #money
        money = f"{data[f'{interaction.guild.id}'][f'{interaction.author.id}']['cash']}"
        font2 = ImageFont.truetype(font_type, 200)
        text_width = draw.textlength(all_money, font1)
        x_m=2600
        y_m=1400
        draw.text((x_m,y_m), money, font=font2)

        #date
        date = f"{data[f'{interaction.guild.id}'][f'{interaction.author.id}']['date']}"
        font3 = ImageFont.truetype(font_type, 200)
        text_width = draw.textlength(all_money, font1)
        x_d=3000
        y_d=1850
        draw.text((x_d,y_d), date, font=font3)

        #user_name
        user_name = f"{interaction.author}"
        font3 = ImageFont.truetype(font_type, 200)
        text_width = draw.textlength(all_money, font1)
        x_name=800
        y_name=1850
        draw.text((x_name,y_name), user_name, font=font3)

        #avatar
        avatar = interaction.author.avatar.with_size(128)
        avt = BytesIO(await avatar.read())
        img = Image.open(avt)
        img = img.resize((420, 420))
        
        mask = Image.new('L', (420, 420), 0)
        radius = min(img.width // 2, img.height // 2)
        center = radius, radius
        draw = ImageDraw.Draw(mask)
        draw.ellipse((0, 0, radius * 2, radius * 2), fill=250)
        img.putalpha(mask)
    
        img.resize((420, 420))
        bank_card.paste(img, (292, 1675), img)
        width, height = bank_card.size
        draw = ImageDraw.Draw(bank_card)
    
        bank_card.save("images/banking system/bank_card.png")
        
        view=View_BankCard()

        emb = disnake.Embed(title=f"💳Банківський рахунок", colour=disnake.Color.blue(), timestamp=interaction.created_at)
        emb.set_image(file=disnake.File('images/banking system/bank_card.png'))
        emb.set_footer(text = f"{config.BY_LINE}", icon_url = bot.user.display_avatar.url)
        await interaction.send(embed=emb, view=view, ephemeral=True)

        with open('data/economy/banking_system.json', 'r', encoding='utf-8') as f:
            data = json.load(f)

        await interaction.response.defer()

        view=View()
        view.remove_item(button)

        emb = disnake.Embed(title="💸Система грошового переказу", colour=disnake.Color.blue(), timestamp=interaction.created_at)
        emb.add_field(name="На вашому рахунку:", value=f"{data[f'{interaction.guild.id}'][f'{interaction.author.id}']['bank']+data[f'{interaction.guild.id}'][f'{interaction.author.id}']['cash']}₴")
        emb.add_field(name="Готівки:", value=f"{data[f'{interaction.guild.id}'][f'{interaction.author.id}']['cash']}₴")
        emb.add_field(name="У банку:", value=f"{data[f'{interaction.guild.id}'][f'{interaction.author.id}']['bank']}₴")
        emb.set_footer(text = f"{config.BY_LINE}", icon_url = bot.user.display_avatar.url)
        await interaction.send(embed=emb, view=view)

    @disnake.ui.button(emoji="💵", label="Депозит", disabled=False)
    async def button_callback_3_active(self, button, interaction):
        with open('data/economy/deposite_system.json', 'r', encoding='utf-8') as f:
            data = json.load(f)

        guilds = []
        for g in data:
            guilds.append(f"{g}")
        if f"{interaction.guild.id}" not in guilds:
            data[f'{interaction.guild.id}'] = {}
            with open('data/economy/deposite_system.json', 'w', encoding='utf-8') as w:
                json.dump(data, w, indent=4)

        members = []
        for m in data[f'{interaction.guild.id}']:
            members.append(f"{m}")

        if f"{interaction.guild.id}" not in members:
            data[f'{interaction.guild.id}'][f'{interaction.author.id}'] = {}
            data[f'{interaction.guild.id}'][f'{interaction.author.id}']['money'] = 0
            data[f'{interaction.guild.id}'][f'{interaction.author.id}']['level'] = 0
            data[f'{interaction.guild.id}'][f'{interaction.author.id}']['date'] = datetime.datetime.today().strftime('%m/%d')

            with open('data/economy/deposite_system.json', 'w', encoding='utf-8') as w:
                json.dump(data, w, indent=4)

        emb = disnake.Embed(title="💸Система депозиту", colour=disnake.Color.blue(), timestamp=interaction.created_at)
        emb.add_field(name="На вашому депозитному рахунку:", value=f"{data[f'{interaction.guild.id}'][f'{interaction.author.id}']['money']}₴")
        emb.set_footer(text = f"{config.BY_LINE}", icon_url = bot.user.display_avatar.url)
        await interaction.send(embed=emb, view=View_Deposite(), ephemeral=True)

class MyView_Disable(disnake.ui.View):#основні неактивні кнопки
    @disnake.ui.button(emoji="💳", label="Банківська картка", disabled=True)
    async def button_callback_1_disabled(self, button, interaction):
        return
    @disnake.ui.button(emoji="💸", label="Переказ", disabled=True)
    async def button_callback_2_disabled(self, button, interaction):
        return
    @disnake.ui.button(emoji="💵", label="Депозит", disabled=True)
    async def button_callback_3_disabled(self, button, interaction):
        return

#-------------------------------------BankCard_button_start----------------------------------------
class View_BankCard(disnake.ui.View):#кнопки в категорії банківський рахунок
    def __init__(self):
        super().__init__()

    @disnake.ui.button(emoji="📤", label="Зняти готівку", disabled=False)
    async def button_callback_bankcard_1(self, button, interaction:disnake.AppCmdInter):
        if interaction.user.id != interaction.author.id:
            await interaction.response.send_message("Ви не можете використовувати цю кнопку, оскільки не ви автор запросу!", ephemeral=True)
        else:
            await interaction.response.send_modal(modal=BankCard_Modal_Take_off_money())
    
    @disnake.ui.button(emoji="📥", label="Покласти готівку", disabled=False)
    async def button_callback_bankcard_2(self, button, inter:disnake.AppCmdInter):
        if inter.user.id != inter.author.id:
            await inter.response.send_message("Ви не можете використовувати цю кнопку, оскільки не ви автор запросу!", ephemeral=True)
        else:
            await inter.response.send_modal(modal=BankCard_Modal_Put_money_down())

class BankCard_Modal_Take_off_money(disnake.ui.Modal):#Модульне вікно зняття готівки
    def __init__(self):
        comp = [
            disnake.ui.TextInput(
                label="Вкажіть суму зняття з банківського рахунку",
                placeholder="сума ₴",
                style=TextInputStyle.short,
                max_length=9,
                min_length=1,
                custom_id="take_off"
            )
        ]
        super().__init__(title="Зняття готівки з банківського рахунка", components=comp)

    async def callback(self, interaction:disnake.ModalInteraction):
        with open('data/economy/banking_system.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        if data[f'{interaction.guild.id}'][f'{interaction.author.id}']['cash']+int(f"{interaction.text_values['take_off']}") <= 100000000:
            if data[f'{interaction.guild.id}'][f'{interaction.author.id}']['bank']-int(f"{interaction.text_values['take_off']}")>=0:
                data[f'{interaction.guild.id}'][f'{interaction.author.id}']['cash'] = data[f'{interaction.guild.id}'][f'{interaction.author.id}']['cash']+int(f"{interaction.text_values['take_off']}")
                data[f'{interaction.guild.id}'][f'{interaction.author.id}']['bank'] = data[f'{interaction.guild.id}'][f'{interaction.author.id}']['bank']-int(f"{interaction.text_values['take_off']}") 

                with open('data/economy/banking_system.json', 'w', encoding='utf-8') as w:
                    json.dump(data, w, indent=4)

                await interaction.response.send_message(f"Операція пройшла успішно! Ви зняли {interaction.text_values['take_off']}₴", ephemeral=True)
            else:
                await interaction.response.send_message(f"На вашому банківському рахунку недостатньо коштів! Ви не можете зняти `{interaction.text_values['take_off']}₴`!\nВи можете зняти не більше, ніж {data[f'{interaction.guild.id}'][f'{interaction.author.id}']['bank']}", ephemeral=True)    
        else:
            await interaction.response.send_message(f"Ви не можете мати більше 100.000.000₴ на руках! Ви можете зняти не більше, аніж {100000000-data[f'{interaction.guild.id}'][f'{interaction.author.id}']['cash']}₴!", ephemeral=True)

class BankCard_Modal_Put_money_down(disnake.ui.Modal):#Модульне вікно внесення готівки
    def __init__(self):
        comp = [
            disnake.ui.TextInput(
                label="Вкажіть суму внесення на банківський рахунок",
                placeholder="сума ₴",
                style=TextInputStyle.short,
                max_length=9,
                min_length=1,
                custom_id="put_down"
            )
        ]
        super().__init__(title="Внесення готівки на банківський рахунок", components=comp)

    async def callback(self, interaction:disnake.ModalInteraction):
        with open('data/economy/banking_system.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        if data[f'{interaction.guild.id}'][f'{interaction.author.id}']['cash']-int(f"{interaction.text_values['put_down']}") >=0:
            if data[f'{interaction.guild.id}'][f'{interaction.author.id}']['bank']+int(f"{interaction.text_values['put_down']}")<=100000000:
                data[f'{interaction.guild.id}'][f'{interaction.author.id}']['cash'] = data[f'{interaction.guild.id}'][f'{interaction.author.id}']['cash']-int(f"{interaction.text_values['put_down']}")
                data[f'{interaction.guild.id}'][f'{interaction.author.id}']['bank'] = data[f'{interaction.guild.id}'][f'{interaction.author.id}']['bank']+int(f"{interaction.text_values['put_down']}") 

                with open('data/economy/banking_system.json', 'w', encoding='utf-8') as w:
                    json.dump(data, w, indent=4)

                await interaction.response.send_message(f"Операція пройшла успішно! Ви поклали {interaction.text_values['put_down']}₴", ephemeral=True)
            else:
                await interaction.response.send_message(f"Ви не можете мати більше 100.000.000₴ на банківському рахунку! Ви можете покласти не більше, аніж {100000000-data[f'{interaction.guild.id}'][f'{interaction.author.id}']['bank']}₴!", ephemeral=True)
        else:
            await interaction.response.send_message(f"У вас недостатньо готівки! Ви не можете покласти `{interaction.text_values['put_down']}₴`!\nВи можете покласти не більше, аніж {data[f'{interaction.guild.id}'][f'{interaction.author.id}']['cash']}", ephemeral=True)  
#-------------------------------------BankCard_button_end------------------------------------------

#-------------------------------------Deposite_button_start----------------------------------------
class View_Deposite(disnake.ui.View):#кнопки в категорії депозит
    def __init__(self):
        super().__init__()

    @disnake.ui.button(emoji="📥", label="Покласти на депозит", disabled=False)
    async def button_callback_deposite_1(self, button, interaction:disnake.AppCmdInter):
        await interaction.response.send_modal(modal=Transaction_Modal_Put_money_down())

    @disnake.ui.button(emoji="📤", label="Зняти з депозиту", disabled=False)
    async def button_callback_deposite_2(self, button, interaction:disnake.AppCmdInter):
        await interaction.response.send_modal(modal=Transaction_Modal_Take_off_money())

class Transaction_Modal_Take_off_money(disnake.ui.Modal):
    def __init__(self):
        comp = [
            disnake.ui.TextInput(
                label="Вкажіть суму зняття з депозитного рахунку",
                placeholder=f"сума ₴",
                style=TextInputStyle.short,
                max_length=9,
                min_length=1,
                custom_id="take_off"
            )
        ]
        super().__init__(title="Зняття готівки з депозитного рахунка", components=comp)

    async def callback(self, interaction:disnake.ModalInteraction):
        with open('data/economy/banking_system.json', 'r', encoding='utf-8') as f:
            data_bank = json.load(f)
        with open('data/economy/deposite_system.json', 'r', encoding='utf-8') as f1:
            data_dep = json.load(f1)
        
        if int(interaction.text_values['take_off']) <= data_dep[f'{interaction.guild.id}'][f'{interaction.author.id}']['money'] and data_dep[f'{interaction.guild.id}'][f'{interaction.author.id}']['money']-int(f"{interaction.text_values['take_off']}")>=0:
            if data_bank[f'{interaction.guild.id}'][f'{interaction.author.id}']['bank']+int(f"{interaction.text_values['take_off']}") <= 100000000:
                data_bank[f'{interaction.guild.id}'][f'{interaction.author.id}']['bank']=data_bank[f'{interaction.guild.id}'][f'{interaction.author.id}']['bank']+int(f"{interaction.text_values['take_off']}")
                data_dep[f'{interaction.guild.id}'][f'{interaction.author.id}']['money']=data_dep[f'{interaction.guild.id}'][f'{interaction.author.id}']['money']-int(f"{interaction.text_values['take_off']}")

                with open('data/economy/banking_system.json', 'w', encoding='utf-8') as w:
                    json.dump(data_bank, w, indent=4)
                with open('data/economy/deposite_system.json', 'w', encoding='utf-8') as w1:
                    json.dump(data_dep, w1, indent=4)
                    
                await interaction.response.send_message(f"Операція пройшла успішно! На ваш банківський рахунок було зачислено `{interaction.text_values['take_off']}₴`.\nЗалишки:\nБанківський рахунок: `{data_bank[f'{interaction.guild.id}'][f'{interaction.author.id}']['bank']}₴`\nДепозитний рахунок: `{data_dep[f'{interaction.guild.id}'][f'{interaction.author.id}']['money']}₴`", ephemeral=True)
            else:
                await interaction.response.send_message(f"Ви не можете перевисити ліміт коштів на банківському рахунку! Ліміт - `100.000.000₴`!\nВи можете зняти не більше, аніж `{100000000-data_bank[f'{interaction.guild.id}'][f'{interaction.author.id}']['bank']}₴`!", ephemeral=True)
        else:
            await interaction.response.send_message(f"Ви не можете зняти більше, аніж `{data_dep[f'{interaction.guild.id}'][f'{interaction.author.id}']['money']}`₴!", ephemeral=True)

class Transaction_Modal_Put_money_down(disnake.ui.Modal):
    def __init__(self):
        comp = [
            disnake.ui.TextInput(
                label="Вкажіть суму внесення на депозитний рахунок",
                placeholder=f"сума ₴",
                style=TextInputStyle.short,
                max_length=9,
                min_length=1,
                custom_id="put_down"
            )
        ]
        super().__init__(title="Внесення готівки на депозитний рахунок", components=comp)

    async def callback(self, interaction:disnake.ModalInteraction):
        with open('data/economy/banking_system.json', 'r', encoding='utf-8') as f:
            data_bank = json.load(f)
        with open('data/economy/deposite_system.json', 'r', encoding='utf-8') as f1:
            data_dep = json.load(f1)
        
        if int(interaction.text_values['put_down']) <= data_bank[f'{interaction.guild.id}'][f'{interaction.author.id}']['bank'] and data_bank[f'{interaction.guild.id}'][f'{interaction.author.id}']['bank']-int(f"{interaction.text_values['put_down']}")>=0:
            if data_dep[f'{interaction.guild.id}'][f'{interaction.author.id}']['money']+int(f"{interaction.text_values['put_down']}") <= 100000000:
                data_bank[f'{interaction.guild.id}'][f'{interaction.author.id}']['bank']=data_bank[f'{interaction.guild.id}'][f'{interaction.author.id}']['bank']-int(f"{interaction.text_values['put_down']}")
                data_dep[f'{interaction.guild.id}'][f'{interaction.author.id}']['money']=data_dep[f'{interaction.guild.id}'][f'{interaction.author.id}']['money']+int(f"{interaction.text_values['put_down']}")

                with open('data/economy/banking_system.json', 'w', encoding='utf-8') as w:
                    json.dump(data_bank, w, indent=4)
                with open('data/economy/deposite_system.json', 'w', encoding='utf-8') as w1:
                    json.dump(data_dep, w1, indent=4)
                    
                await interaction.response.send_message(f"Операція пройшла успішно! На депозитний рахунок було зачислено `{interaction.text_values['put_down']}₴`.\nЗалишки:\nБанківський рахунок: `{data_bank[f'{interaction.guild.id}'][f'{interaction.author.id}']['bank']}₴`\nДепозитний рахунок: `{data_dep[f'{interaction.guild.id}'][f'{interaction.author.id}']['money']}₴`", ephemeral=True)
            else:
                await interaction.response.send_message(f"Ви не можете перевисити ліміт коштів на депозитному рахунку! Ліміт - `100.000.000₴`!\nВи можете внести не більше, аніж `{100000000-data_dep[f'{interaction.guild.id}'][f'{interaction.author.id}']['money']}₴`!", ephemeral=True)
        else:
            await interaction.response.send_message(f"Ви не можете внести більше, аніж `{100000000-data_dep[f'{interaction.guild.id}'][f'{interaction.author.id}']['money']}`₴! На вшому банківському рахунку - `{data_bank[f'{interaction.guild.id}'][f'{interaction.author.id}']['bank']}₴!`", ephemeral=True)

#-------------------------------------Deposite_button_end----------------------------------------

class Bank(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(name = "bank", description="Банк «TarasBot»")
    @commands.guild_only()
    async def bank(self, ctx):
        with open('data/economy/banking_system.json', 'r', encoding='utf-8') as f:
            data = json.load(f)

        NoInfoDate.guild = ctx.guild
        
        async def no_guild_data():
            data[f'{ctx.guild.id}'] = {}

            with open('data/economy/banking_system.json', 'w') as w:
                json.dump(data, w, indent=4)

        guilds = []
        for g in data:
            guilds.append(f"{g}")
        if f"{ctx.guild.id}" not in guilds:
            #додавання до бази даних сервера(якщо відсутний)
            await no_guild_data()


    @bank.sub_command(description="Відкрити головне вікно банку «TarasBot»")
    @commands.guild_only()
    async def app(self, inter):
        NoInfoDate.member = inter.author
        await NoInfoDate.check_user_data()
        
        view = MyView()

        emb = disnake.Embed(title="Банківська система", description="Вітаємо в **Банку «TarasBot»**! Виберіть подальшу операцію для взаємодії з банком ↓↓↓", colour=disnake.Color.blue(), timestamp=inter.created_at)
        emb.set_footer(text=f"{config.BY_LINE}", icon_url=bot.user.display_avatar.url)
        await inter.response.send_message(embed=emb, view=view)

        if await view.wait():
            view=MyView_Disable()
            await inter.edit_original_response(embed=emb, view=view)
        else:
            return

    @bank.sub_command(description="Банківська картка")
    @commands.guild_only()
    async def card(self, ctx):
        NoInfoDate.member = ctx.author

        await NoInfoDate.check_user_data()

        with open('data/economy/banking_system.json', 'r', encoding='utf-8') as f:
            data = json.load(f)

        
        font_type = 'fonts/AABebasNeue.ttf'
        bank_card = Image.open('images/banking system/template_card.png')
        draw = ImageDraw.Draw(bank_card)

        #card_number
        card_number = f"{data[f'{ctx.guild.id}'][f'{ctx.author.id}']['number']}"
        font = ImageFont.truetype(font_type, 250)
        text_width = draw.textlength(card_number, font)
        x_cd = 1108
        y_cd = 810
        draw.text((x_cd,y_cd), card_number, font=font)

        #all_money
        all_money = f"{data[f'{ctx.guild.id}'][f'{ctx.author.id}']['cash'] + data[f'{ctx.guild.id}'][f'{ctx.author.id}']['bank']}"
        font1 = ImageFont.truetype(font_type, 200)
        text_width = draw.textlength(all_money, font1)
        x_allm=450
        y_allm=1400
        draw.text((x_allm,y_allm), all_money, font=font1)

        #bank
        bank = f"{data[f'{ctx.guild.id}'][f'{ctx.author.id}']['bank']}"
        font2 = ImageFont.truetype(font_type, 200)
        text_width = draw.textlength(all_money, font1)
        x_b=1750
        y_b=1400
        draw.text((x_b,y_b), bank, font=font2)

        #money
        money = f"{data[f'{ctx.guild.id}'][f'{ctx.author.id}']['cash']}"
        font2 = ImageFont.truetype(font_type, 200)
        text_width = draw.textlength(all_money, font1)
        x_m=2600
        y_m=1400
        draw.text((x_m,y_m), money, font=font2)

        #date
        date = f"{data[f'{ctx.guild.id}'][f'{ctx.author.id}']['date']}"
        font3 = ImageFont.truetype(font_type, 200)
        text_width = draw.textlength(all_money, font1)
        x_d=3000
        y_d=1850
        draw.text((x_d,y_d), date, font=font3)

        #user_name
        user_name = f"{ctx.author}"
        font3 = ImageFont.truetype(font_type, 200)
        text_width = draw.textlength(all_money, font1)
        x_name=800
        y_name=1850
        draw.text((x_name,y_name), user_name, font=font3)

        #avatar
        avatar = ctx.author.avatar.with_size(128)
        avt = BytesIO(await avatar.read())
        img = Image.open(avt)
        img = img.resize((420, 420))
        
        mask = Image.new('L', (420, 420), 0)
        radius = min(img.width // 2, img.height // 2)
        center = radius, radius
        draw = ImageDraw.Draw(mask)
        draw.ellipse((0, 0, radius * 2, radius * 2), fill=250)
        img.putalpha(mask)
    
        img.resize((420, 420))
        bank_card.paste(img, (292, 1675), img)
        width, height = bank_card.size
        draw = ImageDraw.Draw(bank_card)
    
        bank_card.save("images/banking system/bank_card.png")
        
        emb = disnake.Embed(title=f"💳Банківський рахунок", colour=disnake.Color.blue(), timestamp=ctx.created_at)
        emb.set_image(file=disnake.File('images/banking system/bank_card.png'))
        emb.set_footer(text = f"{config.BY_LINE}", icon_url = bot.user.display_avatar.url)
        await ctx.send(embed=emb)    

    @bank.sub_command(description="Баланс користувача")
    @commands.guild_only()
    async def balance(self, ctx, member:disnake.Member = commands.Param(default=None, description="Вкажіть користувача")):
        if member is None:
            member = ctx.author
        
        NoInfoDate.member = member

        if member.bot:
            await ctx.send("Бот не може мати банківського рахунку!", ephemeral=True)
        else:                
            await NoInfoDate.check_user_data()

            with open('data/economy/banking_system.json', 'r', encoding='utf-8') as f:
                data = json.load(f)

            emb = disnake.Embed(title=f"Баланс користувача {member.name}", colour=disnake.Color.blue(), timestamp=ctx.created_at)
            emb.add_field(name="Всього грошей:", value=f"{data[f'{ctx.guild.id}'][f'{member.id}']['cash'] + data[f'{ctx.guild.id}'][f'{member.id}']['bank']}₴", inline=False)
            emb.add_field(name="Готівка:", value = f"{data[f'{ctx.guild.id}'][f'{member.id}']['cash']}₴")
            emb.add_field(name="У банку:", value = f"{data[f'{ctx.guild.id}'][f'{member.id}']['bank']}₴")
            emb.set_footer(text = f"{config.BY_LINE}", icon_url = bot.user.display_avatar.url)
            await ctx.send(embed=emb)

    @bank.sub_command(description="Переказати кошти на банківський рахунок користувача")
    
    @commands.guild_only()
    async def transfer(self, ctx, member:disnake.Member = commands.Param(description="Вкажіть користувача"), money:int=commands.Param(description="Вкажіть суму для передачі")):
        if member.bot:
            await ctx.send("Бот не може мати банківського рахунку!", ephemeral=True)
        else:
            NoInfoDate.member = ctx.author
            await NoInfoDate.check_user_data()
            NoInfoDate.member = member
            await NoInfoDate.check_user_data()

            with open('data/economy/banking_system.json', 'r', encoding='utf-8') as f:
                data = json.load(f)

            if data[f'{ctx.guild.id}'][f'{ctx.author.id}']['bank'] - money > 0:
                mn_from = data[f'{ctx.guild.id}'][f'{ctx.author.id}']['bank'] - money
                mn_to = data[f'{ctx.guild.id}'][f'{member.id}']['bank'] + money
                if mn_to > 100000000:
                    await ctx.send(f"Користувач {member.mention} не може мати на банківському рахунку більше `100.000.000₴`! На банківсьому рахунку користувача - `{data[f'{ctx.guild.id}'][f'{member.id}']['bank']}₴`! Ви можете надіслати не більше `{100000000-data[f'{ctx.guild.id}'][f'{member.id}']['bank']}₴`", ephemeral=True)
                else:
                    data[f'{ctx.guild.id}'][f'{ctx.author.id}']['bank'] = mn_from
                    data[f'{ctx.guild.id}'][f'{member.id}']['bank'] = mn_to

                    with open('data/economy/banking_system.json', 'w') as w:
                        json.dump(data, w, indent=4)

                    emb = disnake.Embed(title="Транзакція пройшла успішно!", description=f"Користувачу {member.mention} було перераховано `{money}₴`\nНа вашому банківському рахунку залишилося: `{data[f'{ctx.guild.id}'][f'{ctx.author.id}']['bank']}₴`", colour=disnake.Color.blue(), timestamp=ctx.created_at)
                    emb.set_footer(text = f"{config.BY_LINE}", icon_url = bot.user.display_avatar.url)
                    await ctx.send(embed = emb)
            else:
                emb = disnake.Embed(title="Помилка!", description=f"На вашому банківському рахунку не вистачає коштів!\nНа вашому банківському рахунку: `{data[f'{ctx.guild.id}'][f'{ctx.author.id}']['bank']}₴`", colour=disnake.Color.blue(), timestamp=ctx.created_at)
                emb.set_footer(text = f"{config.BY_LINE}", icon_url = bot.user.display_avatar.url)
                await ctx.send(embed = emb, ephemeral=True)
    
    @bank.sub_command(description="Передати гроші користувачу")
    @commands.guild_only()
    async def pay(self, ctx, member:disnake.Member = commands.Param(description="Вкажіть користувача"), money:int=commands.Param(description="Вкажіть суму для передачі")):
        if member.bot:
            await ctx.send("Бот не може мати банківського рахунку!", ephemeral=True)
        else:
            NoInfoDate.member = ctx.author
            await NoInfoDate.check_user_data()
            NoInfoDate.member = member
            await NoInfoDate.check_user_data()

            with open('data/economy/banking_system.json', 'r', encoding='utf-8') as f:
                data = json.load(f)

            if data[f'{ctx.guild.id}'][f'{ctx.author.id}']['cash'] - money > 0:
                mn_from = data[f'{ctx.guild.id}'][f'{ctx.author.id}']['cash'] - money
                mn_to = data[f'{ctx.guild.id}'][f'{member.id}']['cash'] + money
                if mn_to > 100000000:
                    await ctx.send(f"Користувач {member.mention} не може мати на рахунку більше `100.000.000₴`! На рахунку користувача - `{data[f'{ctx.guild.id}'][f'{member.id}']['cash']}₴`! Ви можете надіслати не більше `{100000000-data[f'{ctx.guild.id}'][f'{member.id}']['cash']}₴`", ephemeral=True)
                else:
                    data[f'{ctx.guild.id}'][f'{ctx.author.id}']['cash'] = mn_from
                    data[f'{ctx.guild.id}'][f'{member.id}']['cash'] = mn_to

                    with open('data/economy/banking_system.json', 'w') as w:
                        json.dump(data, w, indent=4)

                    emb = disnake.Embed(title="Передача коштів пройшла успішно!", description=f"Користувачу {member.mention} було перераховано `{money}₴`\nНа вашому рахунку залишилося: `{data[f'{ctx.guild.id}'][f'{ctx.author.id}']['cash']}₴`", colour=disnake.Color.blue(), timestamp=ctx.created_at)
                    emb.set_footer(text = f"{config.BY_LINE}", icon_url = bot.user.display_avatar.url)
                    await ctx.send(embed = emb)
            else:
                emb = disnake.Embed(title="Помилка!", description=f"На вашому рахунку не вистачає коштів!\nНа вашому рахунку: `{data[f'{ctx.guild.id}'][f'{ctx.author.id}']['cash']}₴`", colour=disnake.Color.blue(), timestamp=ctx.created_at)
                emb.set_footer(text = f"{config.BY_LINE}", icon_url = bot.user.display_avatar.url)
                await ctx.send(embed = emb, ephemeral=True)

def setup(bot):
    bot.add_cog(Bank(bot))