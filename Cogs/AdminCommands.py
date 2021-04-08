import os
import sys
import pymongo
from pymongo import MongoClient

from discord.ext import commands

def setup(bot):
    bot.add_cog(AdminCommands(bot))


class AdminCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command()
    async def insert(self, ctx):
        cluster = MongoClient('mongodb://localhost:27017')
        db = cluster['test']
        collection = db['test']

        post = {'_id': 0, 'name': 'Quinn'}
        collection.insert_one(post)

    @commands.command()
    async def find(self, ctx):
        cluster = MongoClient('mongodb://localhost:27017')
        db = cluster['test']
        collection = db['test']

        results = collection.find({'name':'Quinn'})
        for x in results:
            await ctx.send(f'{x}')

