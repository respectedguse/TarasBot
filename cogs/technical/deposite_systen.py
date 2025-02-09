import disnake
from disnake.ext import commands
import json
import config
import sys
sys.path.insert(0, f'{config.CD}')
import main

bot = main.bot


class deposite_system(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

def setup(bot):
    bot.add_cog(deposite_system(bot))