import os
import discord
from keepalive import keep_alive
from discord.ext import commands
import music
import txtcommands
import json
from discord.ext.commands import has_permissions

cogs = [music, txtcommands]

my_secret = os.environ['TOKEN']
client = commands.Bot(command_prefix="^",intents = discord.Intents.all(), case_insensitive=True)

for i in range(len(cogs)):
  cogs[i].setup(client)

@client.event
async def on_ready():
  print(f"Logged in as {client.user}")

import discord
from discord.ext import commands

#Class for reaction roles
class reactrole(commands.Cog):
  def __init__(self,client):
    self.client = client

  @client.command()
  @has_permissions(administrator=True)
  async def reactorole(ctx, emoji, role: discord.Role,*,message):
    emb = discord.Embed(description=message)
    msg = await ctx.channel.send(embed=emb)
    await msg.add_reaction(emoji)

    with open('reactroles.json') as json_file:
      data = json.load(json_file)
      new_react_role= {
        'role_name':role.name,
        'role_id':role.id,
        'emoji':emoji,
        'message_id':msg.id
      }
      
      data.append(new_react_role)

    with open('reactroles.json','w') as j:
      json.dump(data,j,indent=4)

def setup(client):
  client.add_cog(reactrole(client))



keep_alive()
client.run(my_secret)