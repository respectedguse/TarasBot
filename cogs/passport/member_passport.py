import disnake
from disnake.ext import commands
from disnake import TextInputStyle
from disnake.ui import Button, View
import json
import config
from PIL import Image, ImageDraw, ImageFont, ImageOps
from io import BytesIO
import math
import datetime
import sys
sys.path.insert(0, f'{config.CD}')
import main

bot = main.bot

class OpisModal(disnake.ui.Modal):
    def __init__(self):
        comp = [
            disnake.ui.TextInput(
                label="Розкажіть трохи про себе", 
                placeholder="Напишіть про себе",
                style=TextInputStyle.paragraph,
                max_length=150,
                custom_id="opis"
            )
        ]
        super().__init__(title="Доповнення до паспортних даних", components=comp)

    async def callback(self, interaction: disnake.ModalInteraction):
        with open('data/members/passport.json', 'r', encoding='utf-8') as f:
            data = json.load(f)

        data[f"{interaction.author.id}"]["opis"] = f"{interaction.text_values['opis']}"

        with open('data/members/passport.json', 'w') as w:
            json.dump(data, w, indent=4)
        
        await interaction.response.send_message("Вся інформація була успішно додана!",  ephemeral=True)
        

class Modal(disnake.ui.Modal):
    def __init__(self):
        components = [
            disnake.ui.TextInput(
                label="Як вас звати?",
                placeholder="Напишіть ваше ім'я",
                custom_id = "name",
                style=TextInputStyle.short,
                max_length=30           
            ),
            disnake.ui.TextInput(
                label="Скільки вам років?",
                placeholder="Вкажіть ваш вік",
                custom_id = "age",
                style=TextInputStyle.short,
                min_length = 1,
                max_length = 2
            ),
            disnake.ui.TextInput(
                label="Вкажіть вашу дату народження(ДД.ММ.РРРР)",
                placeholder="ДД.ММ.РРРР",
                custom_id = "date",
                style=TextInputStyle.short,
                max_length = 10,
                min_length = 10
            ),
            disnake.ui.TextInput(
                label="Вкажіть вашу стать(Впишіть одну літеру)",
                placeholder="ч - чоловік | ж - жінка",
                custom_id = "sex",
                style=TextInputStyle.short,
                min_length = 1,
                max_length = 1
            )
        ]
        super().__init__(title="Редагувати інформацію", components=components)

    async def callback(self, interaction: disnake.ModalInteraction):
        with open('data/members/passport.json', 'r', encoding='utf-8') as f:
            data = json.load(f)

        if f"{interaction.text_values['sex']}" == "ч" or f"{interaction.text_values['sex']}" == "ж" or f"{interaction.text_values['sex']}" == "Ч" or f"{interaction.text_values['sex']}" == "Ж":
            numbers = ["0","1","2","3","4","5","6","7","8","9"]

            if f"{(interaction.text_values['age'])[0]}" in numbers and f"{(interaction.text_values['age'])[1]}" in numbers:
                if f"{interaction.text_values['sex']}" == "ч" or f"{interaction.text_values['sex']}" == "Ч":
                    sex = "Чоловік"
                elif f"{interaction.text_values['sex']}" == "ж" or f"{interaction.text_values['sex']}" == "Ж":
                    sex = "Жінка"

                data[f"{interaction.author.id}"] = {}
                data[f"{interaction.author.id}"]["name"] = f"{interaction.text_values['name']}" 
                data[f"{interaction.author.id}"]["age"] = int(interaction.text_values['age'])
                data[f"{interaction.author.id}"]["birth"] = f"{interaction.text_values['date']}"
                data[f"{interaction.author.id}"]["date"] = datetime.datetime.today().strftime('%d.%m.%Y')
                data[f"{interaction.author.id}"]["sex"] = f"{sex}"
                data[f"{interaction.author.id}"]["opis"] = ""

                with open('data/members/passport.json', 'w') as w:
                    json.dump(data, w, indent=4)

                async def call_back(inter:disnake.AppCmdInter):
                    await inter.response.send_modal(modal=OpisModal())
                
                button = Button(label="Додати опис про себе", style=disnake.ButtonStyle.green)
                view = View()
                view.add_item(button)
                button.callback = call_back
                
                await interaction.response.send_message("Ви змінили інформацію про себе!", view=view, ephemeral=True)
            else:
                await interaction.response.send_message("Ви допустили помилку в інформації про ваш вік! Спробуйте ще раз! (Використовуйте виключно числа!)", ephemeral=True)
        else:
           await interaction.response.send_message("Ви допустили помилку в інформації про вашу стать! Спробуйте ще раз!", ephemeral=True)

class passport(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.slash_command(name = "passport", description="Паспорт користувача")
    async def passport(self, ctx):
        pass

    @passport.sub_command(description="Показати паспорт користувача")
    async def show(self, ctx, member:disnake.Member = commands.Param(description="Вкажіть користувача", default=None)):
        if member is None:
            member = ctx.author

        with open('data/members/passport.json', 'r', encoding='utf-8') as f:
            data = json.load(f)

        idlist = []
        for id in data:
            idlist.append(id)

        if f"{member.id}" in idlist:
            font_type = 'fonts/AA-Pussycat-Italic.ttf'

            passport = Image.open('images/passport/passport_maket.png')
            draw = ImageDraw.Draw(passport)
        
            #passport_name
            passport_name = f"{data[f'{member.id}']['name']}"
            font = ImageFont.truetype(font_type, 261.89)
            text_width = draw.textlength(passport_name, font)
            x_n = 820
            y_n = 1272
            draw.text((x_n, y_n), passport_name, font=font)

            #sex
            passport_sex = f"{data[f'{member.id}']['sex']}"
            font = ImageFont.truetype(font_type, 261.89)
            text_width = draw.textlength(passport_sex, font)
            x_s = 950
            y_s = 1567
            draw.text((x_s, y_s), passport_sex, font=font)

            #age
            passport_age = f"{data[f'{member.id}']['age']}"
            font = ImageFont.truetype(font_type, 261.89)
            text_width = draw.textlength(passport_age, font)
            x_a = 760
            y_a = 1840
            draw.text((x_a, y_a), passport_age, font=font)

            #nation
            passport_nation = f"Українець"
            font = ImageFont.truetype(font_type, 261.89)
            text_width = draw.textlength(passport_nation, font)
            x_na = 1705
            y_na = 2143
            draw.text((x_na, y_na), passport_nation, font=font)

            #birth_date
            passport_birth = f"{data[f'{member.id}']['birth']}"
            font = ImageFont.truetype(font_type, 261.89)
            text_width = draw.textlength(passport_birth, font)
            x_b = 1925
            y_b = 2445
            draw.text((x_b, y_b), passport_birth, font=font)

            #date_of_given
            passport_date = f"{data[f'{member.id}']['date']}"
            font = ImageFont.truetype(font_type, 261.89)
            text_width = draw.textlength(passport_date, font)
            x_d = 1450
            y_d = 2752
            draw.text((x_d, y_d), passport_date, font=font)

            #avatar
            avatar = member.avatar.with_format('png').with_size(128)
            avt = BytesIO(await avatar.read())
            img = Image.open(avt)
            img = img.resize((680, 680))
            
            mask = Image.new('L', (680, 680), 0)
            radius = min(img.width // 2, img.height // 2)
            center = radius, radius
            draw = ImageDraw.Draw(mask)
            draw.ellipse((0, 0, radius * 2, radius * 2), fill=250)
            img.putalpha(mask)
        
            img.resize((680, 680))
            passport.paste(img, (310, 470), img)
            width, height = passport.size
            draw = ImageDraw.Draw(passport)

            passport.save("images/passport/passport_user.png")

            emb = disnake.Embed(title = f"Паспорт користувача {member.name}", colour=disnake.Color.blue(), description=f"{data[f'{member.id}']['opis']}", timestamp=ctx.created_at) 
            emb.set_image(file=disnake.File('images/passport/passport_user.png'))
            emb.set_footer(text = f"{config.BY_LINE}", icon_url = bot.user.display_avatar.url)
            await ctx.send(embed = emb)
        else:
            emb = disnake.Embed(title=f"Паспорт користувача {member.name} не знайдено!", description="Прохання ввести дані в паспорт за допомогою команди ```/passport edit```", colour=disnake.Color.blue(), timestamp=ctx.created_at)
            emb.set_footer(text = f"{config.BY_LINE}", icon_url = bot.user.display_avatar.url)
            await ctx.send(embed = emb, ephemeral=True)

    @passport.sub_command(description="Редагувати пасортні дані користувача")
    async def edit(self, inter:disnake.AppCmdInter):
        await inter.response.send_modal(modal=Modal())

def setup(bot):
    bot.add_cog(passport(bot))