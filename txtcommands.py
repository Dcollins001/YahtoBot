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
    cmds = {'listcommands\tLists commands', 'rng x y\tGives random number between x and y', 'flipacoin\tFlips a coin', 'peensize\tshows everyone your dick size', 'inspire\tGenerates a Random inspirational quote', 'insult\tGenerates a Random insult', 'yt [youtube url]\tPlays youtube video', 'disconnect\tleaves voice channel', 'pause\tPauses audio', 'resume\tResumes audio', 'purge x\t[Admin only] Deletes x amount of messages', 'stop\tStops playing audio'}
    printer = "```\nCommand list: (Be sure to add ^ before all)\n"
    for command in cmds:
      printer += command + "\n"
    printer += "```"
    await ctx.channel.send(printer)

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

  