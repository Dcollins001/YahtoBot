import discord
from discord.ext import commands
from discord.ext.commands import has_permissions
import random
import requests
import json

class txtcommands(commands.Cog):
  def __init__(self,client):
    self.client = client

  @commands.command()
  async def listcommands(self,ctx):
    cmds = {1: ["listcommands", "Lists commands"],
    2: ["rng x y", "Gives random number between x and y"],
    3: ["flipacoin", "Flips a coin"],
    4: ["peensize", "Shows everyone your dick size"],
    5: ["inspire", "Generates a random inspirational quote"],
    6: ["insult", "Generates a random insult"],
    7: ["yt [youtube url]", "Plays youtube video"], 
    8: ["disconnect", "Removes the bot from the voice channel"],
    9: ["pause", "Pauses youtube video"], 
    10: ["resume", "Resumes youtube video"],
    11: ["stop", "Stops playing youtube video"]}
    returner = "{:<15}---------{:25}".format('Command', 'Use(remember ^prefix)') + "\n"
    for i, j in cmds.items():
        command, use = j
        returner += "{:<15}---------{:25}".format(command, use) + "\n"
    returner += "\n\nAdmin only commands below\n"
    returner += "{:<15}---------{:25}".format('Command', 'Use(remember ^prefix)') + "\n"
    admincmds = {1: ["purge x", "Deletes x amount of messages"],
    2: ["createrolereactor [emote] [role] [message]", "Creates a message that allows for role reactions. Does not work with server emotes, only global ones"],
    3: ["addrolereaction [emote] [role] [message]", "Adds a role reaction to a previously created role reactor"],
    4: ["removerolereaction [emote] [role]", "Removes role reaction from a previously created role reactor"],
    5: ["removerolereactor", "Deletes a previously created role reactor (PLEASE USE THIS. DO NOT MANUALLY DELETE A ROLE REACTOR)"]
    }

    for k, l in admincmds.items():
        command, use = l
        returner += "{:<15}---------{:25}".format(command, use) + "\n"
    emb = discord.Embed(description=returner)
    await ctx.channel.send(embed=emb)
  
  

  @commands.command()
  async def flipacoin(self,ctx):
    face = random.randint(1,2)
    if(face == 1):
      await ctx.channel.send('HEADS!!')
    else:
      await ctx.channel.send('TAILS!!')

  @commands.command()
  async def peensize(self,ctx):
      length = random.uniform(0, 12)
      girth = random.uniform(0, 4)
      printer = 'You have a dick size of ' + str("%.2f" % length) + ' inches long and ' + str("%.2f" % girth) + ' inches thick. '
      if(length > 6 and girth > 2):
        printer += 'Nice cock.'
      await ctx.channel.send(printer)

  @commands.command()
  async def insult(self,ctx):
    try:
      response = requests.get("https://evilinsult.com/generate_insult.php?lang=en&type=json")
      json_data = json.loads(response.text)
      quote = json_data['insult']
      await ctx.channel.send(quote)
    except Exception:
      await ctx.channel.send("Could not find insult!")
      pass
  
  @commands.command()
  async def inspire(self, ctx):
    response = requests.get("https://zenquotes.io/api/random")
    json_data = json.loads(response.text)
    quote = json_data[0]['q'] + " -" + json_data[0]['a']
    await ctx.channel.send(quote)
  
  @commands.command()
  async def rng(self, ctx, arg, arg2):
    if arg.isdigit() == False or arg2.isdigit() == False:
      await ctx.channel.send("Please use 2 whole numbers.")
    else:
      bottom = int(arg)
      top = int(arg2)
      await ctx.channel.send('Your random number is ' + str(random.randint(bottom, top)) + "!")
  
  @commands.command()
  @has_permissions(administrator=True)
  async def purge(self, ctx, arg):
    num = int(arg)
    await ctx.channel.purge(limit=num)

def setup(client):
  client.add_cog(txtcommands(client))

  