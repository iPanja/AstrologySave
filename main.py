import discord
from discord.ext import commands
import config
import MySQLdb

#Discord API
discordToken = config.discord["key"]
bot = discord.Client()
bot = commands.Bot(command_prefix=commands.when_mentioned_or('!'), description='Saves a user\'s astrology information')

#Variables
conn = MySQLdb.connect(user="root", passwd="root", db="astrology", host="localhost", port=3306)
cursor = conn.cursor()

def insert(user, sun, ascendent, moon):
    cursor.execute("""INSERT INTO saves (user, sun, ascendent, moon) VALUES (%s, %s, %s, %s)""", (user, sun, ascendent, moon,))
    conn.commit()
def update(user, sun, ascendent, moon):
    cursor.execute("""UPDATE saves SET sun = %s, ascendent = %s, moon = %s WHERE user = %s""", (sun, ascendent, moon, user,))
    conn.commit()
def fetchone(user):
    cursor.execute("""SELECT sun, ascendent, moon FROM saves WHERE user = %s""", (user,))
    conn.commit()
    results = cursor.fetchall()
    if len(results) == 1:
        return results[0]
    return None

@bot.event
async def on_ready():
    print('Logged in as:\n{0} (ID: {0.id})'.format(bot.user))
@bot.event
async def on_command_error(error, ctx):
    if isinstance(error, commands.CommandNotFound):
        return
    if isinstance(error, commands.MissingRequiredArgument):
        await bot.send_message(ctx.message.channel, "You are missing a parameter.")
    raise error;


@bot.command(pass_context = True)
async def setinfo(ctx, sun:str, ascendent:str, moon:str):
    author = ctx.message.author.name
    if fetchone(author) == None:
        insert(author, sun, ascendent, moon)
    else:
        update(author, sun, ascendent, moon)
    await bot.send_message(ctx.message.channel, "Your astral map has been saved!")

@bot.command(pass_context = True)
async def showmap(ctx, target:discord.Member = None):
    if target == None:
        target = ctx.message.author.name
    else:
        target = target.name
    result = fetchone(target)
    if result == None:
        await bot.send_message(ctx.message.channel, "That user has not created a map yet!")
        return
    await bot.send_message(ctx.message.channel, "**" + target + "'s**" + " astral map: **Sun** " + result[0] + " - **Ascendent** " + result[1] + " - **Moon** " + result[2] + "!")
    return


bot.run(discordToken)