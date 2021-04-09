import os
import re
import sys
import pymongo
from pymongo import MongoClient

from discord.ext import commands

# [a-zA-Z ]*[0-9]*x[0-9]* @ [0-9]*:.*

cluster = MongoClient('mongodb://localhost:27017')
db = cluster['munchie-gains']

val_pattern = '[a-zA-Z ]*[0-9]*x[0-9]* @ [0-9]*:.*'

patterns = ['^[a-zA-Z ]*', '(?<= )[0-9]*(?=x)', '(?<=x)[0-9]*(?= )', '(?<=@ )[0-9]*(?=:)', '(?<=: ).*$']
pat_keys = ['workout', 'sets', 'reps', 'weight', 'comments']

log_temp = {}

def setup(bot):
    bot.add_cog(AdminCommands(bot))

def isUserEnrolled(user):
    collection = db['members']
    results = collection.find({'discord_id':user})
    if results:
        return True
    else:
        return False

def regex_parse(text):
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
    async def log(self, ctx, *, text=''):
        if re.findall(val_pattern, text) and str(ctx.message.author.id) in log_temp.keys():
            post = dict(zip(pat_keys, regex_parse(text)))
            log_temp[str(ctx.message.author.id)]['workouts'].append(post)
        else:
            await ctx.send('You did not begin logging a workout.')

    @commands.command()
    async def start(self, ctx, *, text='unspecified'):
        if str(ctx.message.author.id) in log_temp.keys() and isUserEnrolled(ctx.message.author.id):
            await ctx.send('You are already logging a workout.')
        else:
            log_temp[str(ctx.message.author.id)] = {'discord_id': ctx.message.author.id, 'workout_day_type': text, 'workouts': []}

    @commands.command()
    async def stop(self, ctx):
        if str(ctx.message.author.id) in log_temp.keys() and isUserEnrolled(ctx.message.author.id):
            print(log_temp.pop(str(ctx.message.author.id)))
        else:
            await ctx.send('You were not logging a workout.')

