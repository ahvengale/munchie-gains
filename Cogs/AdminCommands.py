import os
import sys
import pymongo
from pymongo import MongoClient

from discord.ext import commands

cluster = MongoClient('127.0.0.1', 27017)
db = cluster['test']
collection = db['test']

def setup(bot):
    bot.add_cog(AdminCommands(bot))


class AdminCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
