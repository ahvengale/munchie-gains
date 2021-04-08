import os
import sys
import pymongo
from pymongo import MongoClient

from discord.ext import commands

cluster = MongoClient('mongodb://localhost:27017')
db = cluster['munchie-gains']

def setup(bot):
    bot.add_cog(AdminCommands(bot))

def isUserEnrolled(user):
    collection = db['members']
    results = collection.find({'discord_id':user})
    for x in results:
        if results:
            return True
        else:
            return False


class AdminCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command()
    async def drop(self, ctx):
        for x in cluster.database_names():
            cluster.drop_database(x)

    @commands.command()
    async def enroll(self, ctx):
        if not isUserEnrolled(ctx.message.author.id):
            collection = db['members']
            post = {'discord_id':ctx.message.author.id}
            collection.insert_one(post)
        else:
            await ctx.send('You are already enrolled.')
    
    @commands.command()
    async def unenroll(self, ctx):
        if isUserEnrolled(ctx.message.author.id):
            collection = db['members']
            post = {'discord_id':ctx.message.author.id}
            collections.remove_one(post)
        else:
            await ctx.send('You were not enrolled anyways.')

