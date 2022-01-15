
from quart import Quart, redirect, url_for,render_template,request
from quart_discord import DiscordOAuth2Session,requires_authorization, Unauthorized
import aiohttp
import string
import os
import asyncio
import random
from discord import Webhook, AsyncWebhookAdapter
from quart_rate_limiter import RateLimiter,RateLimit,timedelta,rate_limit
#client=commands.Bot(command_prefix="!")
#, default_limits=[RateLimit(1, timedelta(seconds=2))]
app = Quart(__name__)
rate_limiter = RateLimiter(app)
app.secret_key = b"%\xe0'\x01\xdeH\x8e\x85m|\xb3\xffCN\xc9g"
os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "false"    # !! Only in development environment.
timeoutmessage="Try reloading this page , the bot is unresponsive/offline ."

async def waitRequests(randomisedStr):
  print(" Sent a request : "+randomisedStr)
  dict_obj.add(randomisedStr,"waiting")
  while dict_obj[randomisedStr]=="waiting":
    await asyncio.sleep(0.1)
    
  
class my_dictionary(dict):
  
    # __init__ function
    def __init__(self):
        self = dict()
          
    # Function to add key:value
    def add(self, key, value):
        self[key] = value
app.config["DISCORD_CLIENT_ID"] = 884635575032897537
app.config["DISCORD_CLIENT_SECRET"] = os.getenv("DISCORD_CLIENT_SECRET")
app.config["DISCORD_BOT_TOKEN"] = os.getenv("DISCORD_BOT_TOKEN")
app.config["DISCORD_REDIRECT_URI"] = "https://vithron.webdashboard.repl.co/callback"
token=os.environ.get("DISCORD_BOT_TOKEN")
dashtoken=os.environ.get("DASH_SECRET")
discordo = DiscordOAuth2Session(app)
dict_obj = my_dictionary()
hooksecret=os.environ.get("WEBHOOK_SECRET")
HYPERLINK = '<a href="{}">{}</a>'
listOfAuth=[]
def genrandomstr(N):
  res = ''.join(random.choices(string.ascii_uppercase +
                              string.digits, k = N))
  return res
async def sendwebhook(text,userprovided):
        async with aiohttp.ClientSession() as session:
            webhook = Webhook.from_url(hooksecret,
                                       adapter=AsyncWebhookAdapter(session))
            await webhook.send(text,
                               username=f"vi-{userprovided}")

@app.errorhandler(429)
async def rate_limit_exceeded(e):
    return await render_template("429.html",errordata= "You exceeded an allotted request count. Try again later.",url="https://vithron.webdashboard.repl.co/dashboard")
@app.errorhandler(404)
async def page_not_found(e):
    return await render_template("404.html",errordata= "Sorry but the page you are looking for has been removed or is temporarily unavailable.",url="https://vithron.webdashboard.repl.co/dashboard")
@app.errorhandler(500)
async def internal_server_error(e):
    return await render_template("500.html",errordata= "Oops the page you were accessing has encountered an unexpected error. Try refreshing the page.",url="https://vithron.webdashboard.repl.co/dashboard")
@app.errorhandler(403)
async def page_forbidden(e):
    return await render_template("403.html",errordata= "Seems like the page you were missing access to the page you were looking for.",url="https://vithron.webdashboard.repl.co/dashboard")
@app.errorhandler(Unauthorized)
async def redirect_unauthorized(e):
    return redirect(url_for("login"))
@app.route("/info")
async def info():
  return redirect(url_for("index"))
@app.route("/")
async def index():
      botAuth=request.args.get('validateAuth')
      if not botAuth==None:
        if botAuth==dashtoken:
          reqId=request.args.get('requestId')
          print(" Request id : "+str(reqId))
          if not reqId=="vithron":
            reqOutput=request.args.get('requestOut')
            dict_obj[reqId]=reqOutput
            if reqOutput==None:
              reqError=request.args.get('requestErr')
              reqError=str(reqError).replace("+"," ")
              print(" Request error : "+str(reqError))
              dict_obj[reqId]=reqError
            else:
              reqOutput=reqOutput.replace("+"," ")
              try:
                reqOutput = eval(reqOutput)
                reqOutput = reqOutput.decode()
              except Exception:
                  pass
              print(f" Request output : {reqOutput}")
          else:
            reqError=request.args.get('requestErr')
            for key, value in dict_obj.items():
              dict_obj[key]="vithronStart"
      
      return await render_template("index.html", authorized = await discordo.authorized)
@app.route("/riot.txt")
@rate_limit(1, timedelta(seconds=5))
async def riot():
  return await render_template("riot.txt")
@app.route("/dashboard/<int:guild_id>/music")
@rate_limit(1, timedelta(seconds=5))
async def music(guild_id):
  theGuild=None
  user_guilds = await discordo.fetch_guilds()
  for guild in user_guilds:
    if guild.id==guild_id:
      theGuild=guild
  if theGuild==None:
    return await render_template("error.html",errordata= "This guild is not in your guild list.",url="https://vithron.webdashboard.repl.co/dashboard")
  author=await discordo.fetch_user()
  getGuilds=f""" 
print(dashgetchannelsname({theGuild.id},{author.id}))
"""
  randomisedStr=genrandomstr(20)
  while randomisedStr in listOfAuth:
    randomisedStr=genrandomstr(20)
  listOfAuth.append(randomisedStr)
  await sendwebhook(getGuilds,randomisedStr)
  try:
    await asyncio.wait_for(waitRequests(randomisedStr),60)
  except Exception as ex:
    print(ex)
    return await render_template("error.html",url=f"https://vithron.webdashboard.repl.co/dashboard",errordata=timeoutmessage)
  if dict_obj[randomisedStr]=="vithronStart":
    return await render_template("error.html",url=f"https://vithron.webdashboard.repl.co/dashboard",errordata="Bot was offline while requesting data , kindly reload the page.")

  if dict_obj[randomisedStr]==None or dict_obj[randomisedStr]=="None" or dict_obj[randomisedStr]=="":
    return redirect(f"https://vithron.webdashboard.repl.co/dashboard")
  theGuildChannelnames=str(dict_obj[randomisedStr])
  getGuilds=f""" 
print(dashgetchannelsid({theGuild.id},{author.id}))
"""
  randomisedStr=genrandomstr(20)
  while randomisedStr in listOfAuth:
    randomisedStr=genrandomstr(20)
  listOfAuth.append(randomisedStr)
  await sendwebhook(getGuilds,randomisedStr)
  try:
    await asyncio.wait_for(waitRequests(randomisedStr),60)
  except Exception as ex:
    print(ex)
    return await render_template("error.html",url=f"https://vithron.webdashboard.repl.co/dashboard",errordata=timeoutmessage)
  if dict_obj[randomisedStr]=="vithronStart":
    return await render_template("error.html",url=f"https://vithron.webdashboard.repl.co/dashboard",errordata="Bot was offline while requesting data , kindly reload the page.")

  if dict_obj[randomisedStr]==None or dict_obj[randomisedStr]=="None" or dict_obj[randomisedStr]=="":
    return redirect(f"https://vithron.webdashboard.repl.co/dashboard")
  theGuildChannelids=str(dict_obj[randomisedStr])
  getGuilds=f""" 
print(dashgetvcname({theGuild.id},{author.id}))
"""
  randomisedStr=genrandomstr(20)
  while randomisedStr in listOfAuth:
    randomisedStr=genrandomstr(20)
  listOfAuth.append(randomisedStr)
  await sendwebhook(getGuilds,randomisedStr)
  try:
    await asyncio.wait_for(waitRequests(randomisedStr),60)
  except Exception as ex:
    print(ex)
    return await render_template("error.html",url=f"https://vithron.webdashboard.repl.co/dashboard",errordata=timeoutmessage)
  if dict_obj[randomisedStr]=="vithronStart":
    return await render_template("error.html",url=f"https://vithron.webdashboard.repl.co/dashboard",errordata="Bot was offline while requesting data , kindly reload the page.")
  theGuildMembervc=str(dict_obj[randomisedStr])
  return await render_template("music.html",guild=theGuild,guildchannelids=theGuildChannelids,guildchannelnames=theGuildChannelnames,vcinfo=theGuildMembervc)
@app.route("/dashboard/<int:guild_id>/moderation")
async def moderation(guild_id):
  theGuild=None
  user_guilds = await discordo.fetch_guilds()
  for guild in user_guilds:
    if guild.id==guild_id:
      theGuild=guild
  if theGuild==None:
    return await render_template("error.html",errordata= "This guild is not in your guild list.",url="https://vithron.webdashboard.repl.co/dashboard")
  getGuilds=f""" 
print(dashgetmembersname({theGuild.id}))
"""
  randomisedStr=genrandomstr(20)
  while randomisedStr in listOfAuth:
    randomisedStr=genrandomstr(20)
  listOfAuth.append(randomisedStr)
  await sendwebhook(getGuilds,randomisedStr)
  try:
    await asyncio.wait_for(waitRequests(randomisedStr),60)
  except Exception as ex:
    print(ex)
    return await render_template("error.html",url=f"https://vithron.webdashboard.repl.co/dashboard",errordata=timeoutmessage)
  if dict_obj[randomisedStr]=="vithronStart":
    return await render_template("error.html",url=f"https://vithron.webdashboard.repl.co/dashboard",errordata="Bot was offline while requesting data , kindly reload the page.")

  if dict_obj[randomisedStr]==None or dict_obj[randomisedStr]=="None" or dict_obj[randomisedStr]=="":
    return redirect(f"https://vithron.webdashboard.repl.co/dashboard")
  theGuildMembernames=str(dict_obj[randomisedStr])
  getGuilds=f""" 
print(dashgetmembersid({theGuild.id}))
"""
  randomisedStr=genrandomstr(20)
  while randomisedStr in listOfAuth:
    randomisedStr=genrandomstr(20)
  listOfAuth.append(randomisedStr)
  await sendwebhook(getGuilds,randomisedStr)
  try:
    await asyncio.wait_for(waitRequests(randomisedStr),60)
  except Exception as ex:
    print(ex)
    return await render_template("error.html",url=f"https://vithron.webdashboard.repl.co/dashboard",errordata=timeoutmessage)
  if dict_obj[randomisedStr]=="vithronStart":
    return await render_template("error.html",url=f"https://vithron.webdashboard.repl.co/dashboard",errordata="Bot was offline while requesting data , kindly reload the page.")

  if dict_obj[randomisedStr]==None or dict_obj[randomisedStr]=="None" or dict_obj[randomisedStr]=="":
    return redirect(f"https://vithron.webdashboard.repl.co/dashboard")
  theGuildMemberids=str(dict_obj[randomisedStr])
  return await render_template("moderation.html",guild=theGuild,guildmemberids=theGuildMemberids,guildmembernames=theGuildMembernames)
@app.route("/dashboard/<int:guild_id>/commands")
@rate_limit(1, timedelta(seconds=2))
async def command(guild_id):
  theGuild=None
  user_guilds = await discordo.fetch_guilds()
  for guild in user_guilds:
    if guild.id==guild_id:
      theGuild=guild
  if theGuild==None:
    return await render_template("error.html",errordata= "This guild is not in your guild list.",url="https://vithron.webdashboard.repl.co/dashboard")
  return await render_template("commands.html",guild=theGuild)
@app.route("/kick/<int:guild_id>/<string:member>/<string:reason>")
@rate_limit(1, timedelta(seconds=2))
async def kick(guild_id,member,reason):
  theGuild=None
  user_guilds = await discordo.fetch_guilds()
  for guild in user_guilds:
    if guild.id==guild_id:
      theGuild=guild
  if theGuild==None:
    return await render_template("error.html",errordata= "This guild is not in your guild list.",url="https://vithron.webdashboard.repl.co/dashboard")
  if not theGuild.permissions.kick_members:
    return await render_template("error.html",errordata= "You do not have kick member permissions to kick members in this guild.",url=f"https://vithron.webdashboard.repl.co/dashboard/{guild_id}")
  author=await discordo.fetch_user()
  authorid=author.id
  
  getGuilds=f""" 
member='{member}'
if member.isdigit():
  member=int(member)
  guild=client.get_guild({guild_id})
  memberobj=await guild.fetch_member(int(member))
  if memberobj is None:
    print(f"The member with id {member} was invalid.")
    return
else:
  guild=client.get_guild({guild_id})
  memberobj=discord.utils.get(guild.members, name=member)
  if memberobj is None:
    print(f"The member with name {member} was invalid.")
    return
author=await guild.fetch_member({authorid})
await dashkick(guild,author,memberobj,'{reason}')
"""
  randomisedStr=genrandomstr(20)
  while randomisedStr in listOfAuth:
    randomisedStr=genrandomstr(20)
  listOfAuth.append(randomisedStr)
  await sendwebhook(getGuilds,randomisedStr)
  try:
    await asyncio.wait_for(waitRequests(randomisedStr),60)
  except Exception as ex:
    print(ex)
    return await render_template("error.html",url=f"https://vithron.webdashboard.repl.co/dashboard",errordata=timeoutmessage)
  if dict_obj[randomisedStr]=="vithronStart":
    return await render_template("error.html",url=f"https://vithron.webdashboard.repl.co/dashboard",errordata="Bot was offline while requesting data , kindly reload the page.")

  if dict_obj[randomisedStr]==None or dict_obj[randomisedStr]=="None" or dict_obj[randomisedStr]=="":
    return redirect(f"https://vithron.webdashboard.repl.co/dashboard/{guild_id}/moderation")
  return redirect(f"https://vithron.webdashboard.repl.co/dashboard/{guild_id}/moderation")
@app.route("/ban/<int:guild_id>/<string:member>/<string:reason>")
@rate_limit(1, timedelta(seconds=2))
async def ban(guild_id,member,reason):
  theGuild=None
  user_guilds = await discordo.fetch_guilds()
  for guild in user_guilds:
    if guild.id==guild_id:
      theGuild=guild
  if theGuild==None:
    return await render_template("error.html",errordata= "This guild is not in your guild list.",url="https://vithron.webdashboard.repl.co/dashboard")
  if not theGuild.permissions.ban_members:
    return await render_template("error.html",errordata= "You do not have ban member permissions to ban members in this guild.",url=f"https://vithron.webdashboard.repl.co/dashboard/{guild_id}")
  author=await discordo.fetch_user()
  authorid=author.id
  timenum=request.args.get('timenum')
  
  getGuilds=f""" 
member='{member}'
if member.isdigit():
  member=int(member)
  guild=client.get_guild({guild_id})
  memberobj=await guild.fetch_member(int(member))
  if memberobj is None:
    print(f"The member with id {member} was invalid.")
    return
else:
  guild=client.get_guild({guild_id})
  memberobj=discord.utils.get(guild.members, name=member)
  if memberobj is None:
    print(f"The member with name {member} was invalid.")
    return
author=await guild.fetch_member({authorid})
await dashban(guild,author,memberobj,'{reason}',{timenum})
"""
  randomisedStr=genrandomstr(20)
  while randomisedStr in listOfAuth:
    randomisedStr=genrandomstr(20)
  listOfAuth.append(randomisedStr)
  await sendwebhook(getGuilds,randomisedStr)
  try:
    await asyncio.wait_for(waitRequests(randomisedStr),60)
  except Exception as ex:
    print(ex)
    return await render_template("error.html",url=f"https://vithron.webdashboard.repl.co/dashboard",errordata=timeoutmessage)
  if dict_obj[randomisedStr]=="vithronStart":
    return await render_template("error.html",url=f"https://vithron.webdashboard.repl.co/dashboard",errordata="Bot was offline while requesting data , kindly reload the page.")

  if dict_obj[randomisedStr]==None or dict_obj[randomisedStr]=="None" or dict_obj[randomisedStr]=="":
    return redirect(f"https://vithron.webdashboard.repl.co/dashboard/{guild_id}/moderation")
  return redirect(f"https://vithron.webdashboard.repl.co/dashboard/{guild_id}/moderation")
@app.route("/unban/<int:guild_id>/<string:member>/<string:reason>")
@rate_limit(1, timedelta(seconds=2))
async def unban(guild_id,member,reason):
  theGuild=None
  user_guilds = await discordo.fetch_guilds()
  for guild in user_guilds:
    if guild.id==guild_id:
      theGuild=guild
  if theGuild==None:
    return await render_template("error.html",errordata= "This guild is not in your guild list.",url="https://vithron.webdashboard.repl.co/dashboard")
  if not theGuild.permissions.ban_members:
    return await render_template("error.html",errordata= "You do not have ban member permissions to unban members in this guild.",url=f"https://vithron.webdashboard.repl.co/dashboard/{guild_id}")
  author=await discordo.fetch_user()
  authorid=author.id
  
  getGuilds=f""" 
member='{member}'
if member.isdigit():
  member=int(member)
  guild=client.get_guild({guild_id})
  memberobj=await guild.fetch_member(int(member))
  if memberobj is None:
    print(f"The member with id {member} was invalid.")
    return
else:
  guild=client.get_guild({guild_id})
  memberobj=discord.utils.get(guild.members, name=member)
  if memberobj is None:
    print(f"The member with name {member} was invalid.")
    return
author=await guild.fetch_member({authorid})
await dashunban(guild,author,memberobj,'{reason}')
"""
  randomisedStr=genrandomstr(20)
  while randomisedStr in listOfAuth:
    randomisedStr=genrandomstr(20)
  listOfAuth.append(randomisedStr)
  await sendwebhook(getGuilds,randomisedStr)
  try:
    await asyncio.wait_for(waitRequests(randomisedStr),60)
  except Exception as ex:
    print(ex)
    return await render_template("error.html",url=f"https://vithron.webdashboard.repl.co/dashboard",errordata=timeoutmessage)
  if dict_obj[randomisedStr]=="vithronStart":
    return await render_template("error.html",url=f"https://vithron.webdashboard.repl.co/dashboard",errordata="Bot was offline while requesting data , kindly reload the page.")

  if dict_obj[randomisedStr]==None or dict_obj[randomisedStr]=="None" or dict_obj[randomisedStr]=="":
    return redirect(f"https://vithron.webdashboard.repl.co/dashboard/{guild_id}/moderation")
  return redirect(f"https://vithron.webdashboard.repl.co/dashboard/{guild_id}/moderation")
@app.route("/blacklist/<int:guild_id>/<string:member>/<string:reason>")
@rate_limit(1, timedelta(seconds=2))
async def blacklist(guild_id,member,reason):
  theGuild=None
  user_guilds = await discordo.fetch_guilds()
  for guild in user_guilds:
    if guild.id==guild_id:
      theGuild=guild
  if theGuild==None:
    return await render_template("error.html",errordata= "This guild is not in your guild list.",url="https://vithron.webdashboard.repl.co/dashboard")
  if not theGuild.permissions.manage_roles:
    return await render_template("error.html",errordata= "You do not have manage role permissions to blacklist members in this guild.",url=f"https://vithron.webdashboard.repl.co/dashboard/{guild_id}")
  author=await discordo.fetch_user()
  authorid=author.id
  timenum=request.args.get('timenum')
  
  getGuilds=f""" 
member='{member}'
if member.isdigit():
  member=int(member)
  guild=client.get_guild({guild_id})
  memberobj=await guild.fetch_member(int(member))
  if memberobj is None:
    print(f"The member with id {member} was invalid.")
    return
else:
  guild=client.get_guild({guild_id})
  memberobj=discord.utils.get(guild.members, name=member)
  if memberobj is None:
    print(f"The member with name {member} was invalid.")
    return
author=await guild.fetch_member({authorid})
await dashblacklist(guild,author,memberobj,'{reason}','{timenum}')
"""
  randomisedStr=genrandomstr(20)
  while randomisedStr in listOfAuth:
    randomisedStr=genrandomstr(20)
  listOfAuth.append(randomisedStr)
  await sendwebhook(getGuilds,randomisedStr)
  try:
    await asyncio.wait_for(waitRequests(randomisedStr),60)
  except Exception as ex:
    print(ex)
    return await render_template("error.html",url=f"https://vithron.webdashboard.repl.co/dashboard",errordata=timeoutmessage)
  if dict_obj[randomisedStr]=="vithronStart":
    return await render_template("error.html",url=f"https://vithron.webdashboard.repl.co/dashboard",errordata="Bot was offline while requesting data , kindly reload the page.")

  if dict_obj[randomisedStr]==None or dict_obj[randomisedStr]=="None" or dict_obj[randomisedStr]=="":
    return redirect(f"https://vithron.webdashboard.repl.co/dashboard/{guild_id}/moderation")
  return redirect(f"https://vithron.webdashboard.repl.co/dashboard/{guild_id}/moderation")
@app.route("/unblacklist/<int:guild_id>/<string:member>/<string:reason>")
@rate_limit(1, timedelta(seconds=2))
async def unblacklist(guild_id,member,reason):
  theGuild=None
  user_guilds = await discordo.fetch_guilds()
  for guild in user_guilds:
    if guild.id==guild_id:
      theGuild=guild
  if theGuild==None:
    return await render_template("error.html",errordata= "This guild is not in your guild list.",url="https://vithron.webdashboard.repl.co/dashboard")
  if not theGuild.permissions.manage_roles:
    return await render_template("error.html",errordata= "You do not have manage role permissions to unblacklist members in this guild.",url=f"https://vithron.webdashboard.repl.co/dashboard/{guild_id}")
  author=await discordo.fetch_user()
  authorid=author.id
  
  getGuilds=f""" 
member='{member}'
if member.isdigit():
  member=int(member)
  guild=client.get_guild({guild_id})
  memberobj=await guild.fetch_member(int(member))
  if memberobj is None:
    print(f"The member with id {member} was invalid.")
    return
else:
  guild=client.get_guild({guild_id})
  memberobj=discord.utils.get(guild.members, name=member)
  if memberobj is None:
    print(f"The member with name {member} was invalid.")
    return
author=await guild.fetch_member({authorid})
await dashunblacklist(guild,author,memberobj,'{reason}')
"""
  randomisedStr=genrandomstr(20)
  while randomisedStr in listOfAuth:
    randomisedStr=genrandomstr(20)
  listOfAuth.append(randomisedStr)
  await sendwebhook(getGuilds,randomisedStr)
  try:
    await asyncio.wait_for(waitRequests(randomisedStr),60)
  except Exception as ex:
    print(ex)
    return await render_template("error.html",url=f"https://vithron.webdashboard.repl.co/dashboard",errordata=timeoutmessage)
  if dict_obj[randomisedStr]=="vithronStart":
    return await render_template("error.html",url=f"https://vithron.webdashboard.repl.co/dashboard",errordata="Bot was offline while requesting data , kindly reload the page.")

  if dict_obj[randomisedStr]==None or dict_obj[randomisedStr]=="None" or dict_obj[randomisedStr]=="":
    return redirect(f"https://vithron.webdashboard.repl.co/dashboard/{guild_id}/moderation")
  return redirect(f"https://vithron.webdashboard.repl.co/dashboard/{guild_id}/moderation")
@app.route("/unmute/<int:guild_id>/<string:member>/<string:reason>")
@rate_limit(1, timedelta(seconds=2))
async def unmute(guild_id,member,reason):
  theGuild=None
  user_guilds = await discordo.fetch_guilds()
  for guild in user_guilds:
    if guild.id==guild_id:
      theGuild=guild
  if theGuild==None:
    return await render_template("error.html",errordata= "This guild is not in your guild list.",url="https://vithron.webdashboard.repl.co/dashboard")
  if not theGuild.permissions.manage_roles:
    return await render_template("error.html",errordata= "You do not have manage role permissions to unmute members in this guild.",url=f"https://vithron.webdashboard.repl.co/dashboard/{guild_id}")
  author=await discordo.fetch_user()
  authorid=author.id
  
  getGuilds=f""" 
member='{member}'
if member.isdigit():
  member=int(member)
  guild=client.get_guild({guild_id})
  memberobj=await guild.fetch_member(int(member))
  if memberobj is None:
    print(f"The member with id {member} was invalid.")
    return
else:
  guild=client.get_guild({guild_id})
  memberobj=discord.utils.get(guild.members, name=member)
  if memberobj is None:
    print(f"The member with name {member} was invalid.")
    return
author=await guild.fetch_member({authorid})
await dashunmute(guild,author,memberobj,'{reason}')
"""
  randomisedStr=genrandomstr(20)
  while randomisedStr in listOfAuth:
    randomisedStr=genrandomstr(20)
  listOfAuth.append(randomisedStr)
  await sendwebhook(getGuilds,randomisedStr)
  try:
    await asyncio.wait_for(waitRequests(randomisedStr),60)
  except Exception as ex:
    print(ex)
    return await render_template("error.html",url=f"https://vithron.webdashboard.repl.co/dashboard",errordata=timeoutmessage)
  if dict_obj[randomisedStr]=="vithronStart":
    return await render_template("error.html",url=f"https://vithron.webdashboard.repl.co/dashboard",errordata="Bot was offline while requesting data , kindly reload the page.")

  if dict_obj[randomisedStr]==None or dict_obj[randomisedStr]=="None" or dict_obj[randomisedStr]=="":
    return redirect(f"https://vithron.webdashboard.repl.co/dashboard/{guild_id}/moderation")
  return redirect(f"https://vithron.webdashboard.repl.co/dashboard/{guild_id}/moderation")
@app.route("/mute/<int:guild_id>/<string:member>/<string:reason>")
@rate_limit(1, timedelta(seconds=2))
async def mute(guild_id,member,reason):
  theGuild=None
  user_guilds = await discordo.fetch_guilds()
  for guild in user_guilds:
    if guild.id==guild_id:
      theGuild=guild
  if theGuild==None:
    return await render_template("error.html",errordata= "This guild is not in your guild list.",url="https://vithron.webdashboard.repl.co/dashboard")
  if not theGuild.permissions.manage_roles:
    return await render_template("error.html",errordata= "You do not have manage role permissions to mute members in this guild.",url=f"https://vithron.webdashboard.repl.co/dashboard/{guild_id}")
  author=await discordo.fetch_user()
  authorid=author.id
  timenum=request.args.get('timenum')
  
  getGuilds=f""" 
member='{member}'
if member.isdigit():
  member=int(member)
  guild=client.get_guild({guild_id})
  memberobj=await guild.fetch_member(int(member))
  if memberobj is None:
    print(f"The member with id {member} was invalid.")
    return
else:
  guild=client.get_guild({guild_id})
  memberobj=discord.utils.get(guild.members, name=member)
  if memberobj is None:
    print(f"The member with name {member} was invalid.")
    return
author=await guild.fetch_member({authorid})
await dashmute(guild,author,memberobj,'{reason}','{timenum}')
"""
  randomisedStr=genrandomstr(20)
  while randomisedStr in listOfAuth:
    randomisedStr=genrandomstr(20)
  listOfAuth.append(randomisedStr)
  await sendwebhook(getGuilds,randomisedStr)
  try:
    await asyncio.wait_for(waitRequests(randomisedStr),60)
  except Exception as ex:
    print(ex)
    return await render_template("error.html",url=f"https://vithron.webdashboard.repl.co/dashboard",errordata=timeoutmessage)
  if dict_obj[randomisedStr]=="vithronStart":
    return await render_template("error.html",url=f"https://vithron.webdashboard.repl.co/dashboard",errordata="Bot was offline while requesting data , kindly reload the page.")

  if dict_obj[randomisedStr]==None or dict_obj[randomisedStr]=="None" or dict_obj[randomisedStr]=="":
    return redirect(f"https://vithron.webdashboard.repl.co/dashboard/{guild_id}/moderation")
  return redirect(f"https://vithron.webdashboard.repl.co/dashboard/{guild_id}/moderation")

@app.route("/dashboard/<int:guild_id>/prefixes")
@rate_limit(1, timedelta(seconds=5))
async def prefix(guild_id):
  theGuild=None
  user_guilds = await discordo.fetch_guilds()
  for guild in user_guilds:
    if guild.id==guild_id:
      theGuild=guild
  if theGuild==None:
    return await render_template("error.html",errordata= "This guild is not in your guild list.",url="https://vithron.webdashboard.repl.co/dashboard")
  
  getGuilds=f""" 
prefix = await get_guild_prefixid({theGuild.id})
print(prefix)
"""
  randomisedStr=genrandomstr(20)
  while randomisedStr in listOfAuth:
    randomisedStr=genrandomstr(20)
  listOfAuth.append(randomisedStr)
  await sendwebhook(getGuilds,randomisedStr)
  try:
    await asyncio.wait_for(waitRequests(randomisedStr),60)
  except:
    return await render_template("error.html",url=f"https://vithron.webdashboard.repl.co/dashboard",errordata=timeoutmessage)
  if dict_obj[randomisedStr]=="vithronStart":
    return await render_template("error.html",url=f"https://vithron.webdashboard.repl.co/dashboard",errordata="Bot was offline while requesting data , kindly reload the page.")
  return await render_template("prefixes.html",guild=theGuild,prefix=str(dict_obj[randomisedStr]))
@app.route("/login")
async def login():
    return await discordo.create_session()

@app.route("/callback")
async def callback():
    errorOcc=request.args.get('error_description')
    if not errorOcc==None:
      errorOcc=errorOcc.replace('+',' ')
      return await render_template("error.html",errordata=errorOcc+".",url="https://vithron.webdashboard.repl.co/")
    try:
      data = await discordo.callback()
      redirect_to = data.get("redirect", "/")
    except Exception as ex:
      print(f" An unknown error occured : {type(ex)}{ex} ")
      return await render_template("error.html",errordata=" An unknown error occured ",url="https://vithron.webdashboard.repl.co/")
    return redirect(redirect_to)

@app.route("/playsong/<int:guild_id>/<string:songname>/<string:channelid>")
@rate_limit(1, timedelta(seconds=30))
async def playsong(guild_id,songname,channelid):
  theGuild=None
  user_guilds = await discordo.fetch_guilds()
  for guild in user_guilds:
    if guild.id==guild_id:
      theGuild=guild
  if theGuild==None:
    return await render_template("error.html",errordata="This guild is not in your guild list.",url="https://vithron.webdashboard.repl.co/dashboard")
  user=await discordo.fetch_user()
  
  songname=songname.replace("%20"," ")
  getGuilds=f""" 
  await dashplay({guild_id}, {user.id}, {channelid},'{songname}')
"""
  randomisedStr=genrandomstr(20)
  while randomisedStr in listOfAuth:
    randomisedStr=genrandomstr(20)
  listOfAuth.append(randomisedStr)
  await sendwebhook(getGuilds,randomisedStr)
  try:
    await asyncio.wait_for(waitRequests(randomisedStr),60)
  except:
    return await render_template("error.html",url=f"https://vithron.webdashboard.repl.co/dashboard",errordata=timeoutmessage)
  if dict_obj[randomisedStr]=="vithronStart":
    return await render_template("error.html",url=f"https://vithron.webdashboard.repl.co/dashboard",errordata="Bot was offline while requesting data , kindly reload the page.")

  if dict_obj[randomisedStr]==None or dict_obj[randomisedStr]=="None" or dict_obj[randomisedStr]=="":
    return redirect(f"https://vithron.webdashboard.repl.co/dashboard/{guild_id}/music")
  return redirect(f"https://vithron.webdashboard.repl.co/dashboard/{guild_id}/music")
@app.route("/pausesong/<int:guild_id>/<string:songname>/<string:channelid>")
@rate_limit(1, timedelta(seconds=2))
async def pausesong(guild_id,songname,channelid):
  theGuild=None
  user_guilds = await discordo.fetch_guilds()
  for guild in user_guilds:
    if guild.id==guild_id:
      theGuild=guild
  if theGuild==None:
    return await render_template("error.html",errordata="This guild is not in your guild list.",url="https://vithron.webdashboard.repl.co/dashboard")
  user=await discordo.fetch_user()
  
  songname=songname.replace("%20"," ")
  user=await discordo.fetch_user()
  getGuilds=f""" 
  await dashpause({guild_id}, {user.id}, {channelid})
"""
  randomisedStr=genrandomstr(20)
  while randomisedStr in listOfAuth:
    randomisedStr=genrandomstr(20)
  listOfAuth.append(randomisedStr)
  await sendwebhook(getGuilds,randomisedStr)
  try:
    await asyncio.wait_for(waitRequests(randomisedStr),60)
  except:
    return await render_template("error.html",url=f"https://vithron.webdashboard.repl.co/dashboard",errordata=timeoutmessage)
  if dict_obj[randomisedStr]=="vithronStart":
    return await render_template("error.html",url=f"https://vithron.webdashboard.repl.co/dashboard",errordata="Bot was offline while requesting data , kindly reload the page.")

  if dict_obj[randomisedStr]==None or dict_obj[randomisedStr]=="None" or dict_obj[randomisedStr]=="":
    return redirect(f"https://vithron.webdashboard.repl.co/dashboard/{guild_id}/music")
  return redirect(f"https://vithron.webdashboard.repl.co/dashboard/{guild_id}/music")
@app.route("/loopsong/<int:guild_id>/<string:songname>/<string:channelid>")
@rate_limit(1, timedelta(seconds=4))
async def loopsong(guild_id,songname,channelid):
  theGuild=None
  user_guilds = await discordo.fetch_guilds()
  for guild in user_guilds:
    if guild.id==guild_id:
      theGuild=guild
  if theGuild==None:
    return await render_template("error.html",errordata="This guild is not in your guild list.",url="https://vithron.webdashboard.repl.co/dashboard")
  user=await discordo.fetch_user()
  userid=user.id
  
  songname=songname.replace("%20"," ")
  getGuilds=f""" 
 await dashloop({guild_id}, {userid}, {channelid},'{songname}')
"""
  randomisedStr=genrandomstr(20)
  while randomisedStr in listOfAuth:
    randomisedStr=genrandomstr(20)
  listOfAuth.append(randomisedStr)
  await sendwebhook(getGuilds,randomisedStr)
  try:
    await asyncio.wait_for(waitRequests(randomisedStr),60)
  except:
    return await render_template("error.html",url=f"https://vithron.webdashboard.repl.co/dashboard",errordata=timeoutmessage)
  if dict_obj[randomisedStr]=="vithronStart":
    return await render_template("error.html",url=f"https://vithron.webdashboard.repl.co/dashboard",errordata="Bot was offline while requesting data , kindly reload the page.")

  if dict_obj[randomisedStr]==None or dict_obj[randomisedStr]=="None" or dict_obj[randomisedStr]=="":
    return redirect(f"https://vithron.webdashboard.repl.co/dashboard/{guild_id}/music")
  return redirect(f"https://vithron.webdashboard.repl.co/dashboard/{guild_id}/music")
@app.route("/stopsong/<int:guild_id>/<string:songname><string:channelid>")
@rate_limit(1, timedelta(seconds=2))
async def stopsong(guild_id,songname,channelid):
  theGuild=None
  user_guilds = await discordo.fetch_guilds()
  for guild in user_guilds:
    if guild.id==guild_id:
      theGuild=guild
  if theGuild==None:
    return await render_template("error.html",errordata="This guild is not in your guild list.",url="https://vithron.webdashboard.repl.co/dashboard")
  user=await discordo.fetch_user()
  userid=user.id
  
  songname=songname.replace("%20"," ")
  getGuilds=f""" 
await dashstop({guild_id}, {userid}, {channelid})
"""
  randomisedStr=genrandomstr(20)
  while randomisedStr in listOfAuth:
    randomisedStr=genrandomstr(20)
  listOfAuth.append(randomisedStr)
  await sendwebhook(getGuilds,randomisedStr)
  try:
    await asyncio.wait_for(waitRequests(randomisedStr),60)
  except:
    return await render_template("error.html",url=f"https://vithron.webdashboard.repl.co/dashboard",errordata=timeoutmessage)
  if dict_obj[randomisedStr]=="vithronStart":
    return await render_template("error.html",url=f"https://vithron.webdashboard.repl.co/dashboard",errordata="Bot was offline while requesting data , kindly reload the page.")
  
  if dict_obj[randomisedStr]==None or dict_obj[randomisedStr]=="None" or dict_obj[randomisedStr]=="":
    return redirect(f"https://vithron.webdashboard.repl.co/dashboard/{guild_id}/music")
  return redirect(f"https://vithron.webdashboard.repl.co/dashboard/{guild_id}/music")
@app.route("/dashboard")
async def user_guilds():
  global listOfAuth
  user_guilds = await discordo.fetch_guilds()
  guild_count=len(user_guilds)
  authguilds=[]
  for guild in user_guilds:
    if guild.permissions.manage_guild:
      if not guild.id==811864132470571038:			
        guild.class_color = "green-border"
      else:
        guild.class_color = "golden-border"
    else:
      guild.class_color = "red-border"
    authguilds.append(guild)
  
  authguilds.sort(key = lambda x: x.class_color == "red-border")
  user=await discordo.fetch_user()
  name = user.name
  return await render_template("guilds.html", guild_count = guild_count, guilds = authguilds, username=name,user=user)
@app.route("/changeprefix/<int:guild_id>/<string:prefix>")
@rate_limit(1, timedelta(seconds=3))
async def changeprefix(guild_id,prefix):
  theGuild=None
  user_guilds = await discordo.fetch_guilds()
  for guild in user_guilds:
    if guild.id==guild_id:
      theGuild=guild
  if theGuild==None:
    return await render_template("error.html",errordata= "This guild is not in your guild list.",url="https://vithron.webdashboard.repl.co/dashboard")
  if not theGuild.permissions.manage_guild:
    return await render_template("error.html",errordata= "You do not have manage guild permissions to change prefixes in this guild.",url=f"https://vithron.webdashboard.repl.co/dashboard/{guild_id}")
  user=await discordo.fetch_user()
  
  getGuilds=f"""
await dashsetprefix({guild_id},{user.id},'{prefix}')
"""
  randomisedStr=genrandomstr(20)
  while randomisedStr in listOfAuth:
    randomisedStr=genrandomstr(20)
  listOfAuth.append(randomisedStr)
  await sendwebhook(getGuilds,randomisedStr)
  try:
    await asyncio.wait_for(waitRequests(randomisedStr),60)
  except:
    return await render_template("error.html",url=f"https://vithron.webdashboard.repl.co/dashboard",errordata=timeoutmessage)
  if dict_obj[randomisedStr]=="vithronStart":
    return await render_template("error.html",url=f"https://vithron.webdashboard.repl.co/dashboard",errordata="Bot was offline while requesting data , kindly reload the page.")
  return redirect(f"https://vithron.webdashboard.repl.co/dashboard/{guild_id}")

@app.route("/dashboard/<int:guild_id>")
@rate_limit(1, timedelta(seconds=1))
async def dashboard_server(guild_id):
  if not await discordo.authorized:
    return redirect(url_for("login"))
  user_guilds=await discordo.fetch_guilds()
  user_guildids=[]
  for guild in user_guilds:
    user_guildids.append(guild.id)
  if not guild_id in user_guildids:
    return await render_template("error.html",errordata= "You do not have permissions to access this guild.",url="https://vithron.webdashboard.repl.co/dashboard")
  theGuild=None
  for g in user_guilds:
    if g.id==guild_id:
      theGuild=g
  
  getGuilds=f""" 
print(get_guilds())
"""
  randomisedStr=genrandomstr(20)
  while randomisedStr in listOfAuth:
    randomisedStr=genrandomstr(20)
  listOfAuth.append(randomisedStr)
  await sendwebhook(getGuilds,randomisedStr)
  try:
    await asyncio.wait_for(waitRequests(randomisedStr),60)
  except Exception as ex:
    print(ex)
    return await render_template("error.html",url=f"https://vithron.webdashboard.repl.co/dashboard",errordata=timeoutmessage)
  if dict_obj[randomisedStr]=="vithronStart":
    return await render_template("error.html",url=f"https://vithron.webdashboard.repl.co/dashboard",errordata="Bot was offline while requesting data , kindly reload the page.")
  voithosguilds=list(eval(str(dict_obj[randomisedStr])))
  if not guild_id in voithosguilds:
    if theGuild.permissions.manage_guild:
      return (redirect(f"https://discord.com/oauth2/authorize?client_id=884635575032897537&permissions=2416012310&scope=bot&guild_id={guild_id}"))
    else:
      return await render_template("error.html",errordata= "You do not have permissions to invite this bot to that guild.",url="https://vithron.webdashboard.repl.co/dashboard")
  return await render_template("guild.html",guild=theGuild)

@app.route("/logout/")
async def logout():
    discordo.revoke()
    return redirect(url_for(".index"))

if __name__ == "__main__":
  app.run(host='0.0.0.0')

#client.run(token=token)