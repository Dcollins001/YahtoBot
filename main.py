import os
import discord
from keepalive import keep_alive
from discord.ext import commands
import music
import txtcommands
import time
import json
from discord import Embed
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

#Nested Class for reaction roles
class reactrole(commands.Cog):
  def __init__(self,client):
    self.client = client

  #^createrolereactor command in a discord server. Creates a prompt in a channel that allows users to react to a message for a role.
  @client.command()
  @has_permissions(administrator=True)
  async def createrolereactor(ctx, emoji, role: discord.Role,*,message):

    await ctx.channel.purge(limit=1)
    msg = await ctx.channel.send(message)
    await msg.add_reaction(emoji)

    #Saves the data about the message id and which emote to react to for a role
    with open('reactroles.json') as json_file:
      data = json.load(json_file)
      new_react_role= {
        'role_name':role.name,
        'role_id':role.id,
        'emote':emoji,
        'msgid':msg.id,
        'isreactor':'yes',
        'serverid':ctx.message.guild.id,
        'channelid':ctx.message.channel.id,
      }
      data.append(new_react_role)
    with open('reactroles.json','w') as j:
      json.dump(data,j,indent=4)
  
  #^removerolereactor command that removes the role reactor and any records in the .json file with the same server id and channel id
  
  
  #upon callin this command, have the bot add another reaction to the initial message witht that emote, add to .json file, and make it actionable
  @client.command()
  @has_permissions(administrator=True)
  async def addrolereaction(ctx, emoji, role: discord.Role,*,message):
    with open('reactroles.json') as react_file:
      data = json.load(react_file)
      reactormade = False
      for x in data:
        if x['isreactor'] == 'yes' and x['serverid'] == ctx.message.guild.id and x['channelid'] == ctx.message.channel.id:
          messageid = x['msgid']
          if(await ctx.channel.fetch_message(messageid)):
            reactormade = True
            break
          else:
            pass
      if reactormade == False:
        #if no role reactor is already made
        await ctx.channel.send("Error! You may not have created a role reactor in this channel yet!")
        time.sleep(2)
        await ctx.channel.purge(limit=2)
        return
      try:
        #find the message and attach reaction
        origmessage = await ctx.channel.fetch_message(messageid)
        await ctx.channel.send("Reaction role added!")
        time.sleep(2)
        await ctx.channel.purge(limit=2)
        await origmessage.add_reaction(emoji)
        await origmessage.edit(content=origmessage.content + "\n" + message)
        #attach data to the .json file of all the reaction data and all
        with open('reactroles.json') as json_file:
          data = json.load(json_file)
          new_react_role= {
          'role_name':role.name,
          'role_id':role.id,
          'emote':emoji,
          'msgid':messageid,
          'isreactor':'no',
          'serverid':ctx.message.guild.id,
          'channelid':ctx.message.channel.id
          }
          data.append(new_react_role)

          with open('reactroles.json', 'w') as j:
            json.dump(data,j,indent=4)
          #exception if reactor has not been made
      except Exception as e:
          print(e)
          await ctx.channel.send("Error! You may not have created a role reactor in this channel yet!")
          time.sleep(2)
          await ctx.channel.purge(limit=2)
          return

  #Will delete the role reactor and all its records in reactroles.json
  @client.command()
  @has_permissions(administrator = True)
  async def removerolereactor(ctx):
    reactormade = False
    with open('reactroles.json') as react_file:
      data = json.load(react_file)
      #first, check if reactor has been made
      for x in data:
        if x['isreactor'] == 'yes' and x['serverid'] == ctx.message.guild.id and x['channelid'] == ctx.message.channel.id:
          messageid = x['msgid']
          if(await ctx.channel.fetch_message(messageid)):
            reactormade = True
            reactor = await ctx.channel.fetch_message(messageid)
            await reactor.delete()
    
    if reactormade == False:
      #if no role reactor is already made
      await ctx.channel.send("Error! You may not have created a role reactor in this channel yet!")
      time.sleep(2)
      await ctx.channel.purge(limit=2)
      return
    else:
    #delete all records in reactroles.json with the same channel and serverid by writing all back records except the found ones
      with open('reactroles.json') as json_file:
        data = json.load(json_file)
        replacer = []
        for i in range(len(replacer)):
          if(str(data[i]['serverid']) != ctx.message.guild.id and str(data[i]['channelid']) != ctx.message.channel.id):
            replacer.append(data[i])
      with open('reactroles.json', 'w') as j:
        json.dump(replacer,j,indent=4)
    await ctx.channel.purge(limit=1)
    
      
  #upon calling this command, remove a role reaction both from the interface and from the .json file
  @client.command()
  @has_permissions(administrator=True)
  async def removerolereaction(ctx, emoji, role: discord.Role):
    index = 0
    with open('reactroles.json') as react_file:
      data = json.load(react_file)
      reactormade = False
      for x in data:
        #TODO: first, must check if reactor has been made and if there is already a reaction for that role
        if x['isreactor'] == 'yes' and x['serverid'] == ctx.message.guild.id and x['channelid'] == ctx.message.channel.id:
          messageid = x['msgid']
          if(await ctx.channel.fetch_message(messageid)):
            reactormade = True
            break
          else:
            pass
      if reactormade == False:
        #if no role reactor is already made
        await ctx.channel.send("Error! You may not have created a role reactor in this channel yet!")
        time.sleep(2)
        await ctx.channel.purge(limit=2)
        return
      try:
        #find the message and remove the reaction
        origmessage = await ctx.channel.fetch_message(messageid)
        await ctx.channel.send("Reaction role removed!")
        time.sleep(2)
        await ctx.channel.purge(limit=2)
        await origmessage.clear_reaction(emoji)
        #remove that reaction role data from the .json file by writing back all records except the found one
        with open('reactroles.json') as json_file:
          data = json.load(json_file)
          print(role.id)
          for i in range(len(data)):
            if str(data[i]['role_id']) == str(role.id):
              index = i
              break
        replacer = data
        replacer.pop(index)
        with open('reactroles.json', 'w') as j:
          json.dump(replacer,j,indent=4)
      #catch exception if a role reactor is not already made
      except Exception as e:
          print(e)
          await ctx.channel.send("Error! You may not have created a role reactor in this channel yet!")
          time.sleep(2)
          await ctx.channel.purge(limit=2)
          return


  #Adds role to a user when they react to the role
  @client.event
  async def on_raw_reaction_add(payload):
    if payload.member.bot:
      pass
    else:
      with open('reactroles.json') as react_file:
        data = json.load(react_file)
        for x in data:
          if x['emote'] == payload.emoji.name and x['msgid'] == payload.message_id:
            role = discord.utils.get(client.get_guild(payload.guild_id).roles, id=x['role_id'])
            await payload.member.add_roles(role)
  
  #Removes role from a user when they remove their reaction. Similar function as before, but without the need to check if the reactor is a bot and also has slightly different logic since payload.member.remove_roles doesnt exist.
  @client.event
  async def on_raw_reaction_remove(payload):
    with open('reactroles.json') as react_file:
      data = json.load(react_file)
      for x in data:
        if x['emote'] == payload.emoji.name and x['msgid'] == payload.message_id:
          role = discord.utils.get(client.get_guild(payload.guild_id).roles, id=x['role_id'])
          await client.get_guild(payload.guild_id).get_member(payload.user_id).remove_roles(role)
        


keep_alive()
client.run(my_secret)