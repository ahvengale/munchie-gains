import os
import re
import sys
import pymongo
from pymongo import MongoClient

from discord.ext import commands

# [a-zA-Z ]*[0-9]*x[0-9]* @ [0-9]*:.*

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

def regex_parse(patterns, text):
    ret = []
    for p in patterns:
        ret.append(re.findall(p, text)[0].strip())
    return ret


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

    @commands.command()
    async def log(self, ctx, *, text):
        val_pattern = '[a-zA-Z ]*[0-9]*x[0-9]* @ [0-9]*:.*'
        if re.findall(val_pattern, text):
            workout = '^[a-zA-Z ]*'
            sets = '(?<= )[0-9]*(?=x)'
            reps = '(?<=x)[0-9]*(?= )'
            weight = '(?<=@ )[0-9]*(?=:)'
            comment = '(?<=: ).*$'
            print(regex_parse([workout, sets, reps, weight, comment], text))

