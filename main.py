
from quart import Quart, redirect, url_for,render_template,request
from quart_discord import DiscordOAuth2Session, requires_authorization
import aiohttp
import string
import os
import asyncio
import random
from discord import Webhook, AsyncWebhookAdapter
from quart_rate_limiter import RateLimiter,RateLimit,timedelta,rate_limit
#client=commands.Bot(command_prefix="!")
app = Quart(__name__)
rate_limiter = RateLimiter(app, default_limits=[RateLimit(1, timedelta(seconds=2))])
app.secret_key = b"%\xe0'\x01\xdeH\x8e\x85m|\xb3\xffCN\xc9g"
os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "false"    # !! Only in development environment.
class my_dictionary(dict):
  
    # __init__ function
    def __init__(self):
        self = dict()
          
    # Function to add key:value
    def add(self, key, value):
        self[key] = value
app.config["DISCORD_CLIENT_ID"] = 805030662183845919
app.config["DISCORD_CLIENT_SECRET"] = os.getenv("DISCORD_CLIENT_SECRET")
app.config["DISCORD_BOT_TOKEN"] = os.getenv("DISCORD_BOT_TOKEN")
app.config["DISCORD_REDIRECT_URI"] = "https://TestBOT.thejavaprogramm.repl.co/callback"
token=os.environ.get("DISCORD_BOT_TOKEN")
discordo = DiscordOAuth2Session(app)
dict_obj = my_dictionary()

HYPERLINK = '<a href="{}">{}</a>'
listOfAuth=[]
def genrandomstr(N):
  res = ''.join(random.choices(string.ascii_uppercase +
                              string.digits, k = N))
  return res
async def sendwebhook(text,userprovided,hookurl=None):
        hookurl="https://discord.com/api/webhooks/869804616529899561/FnxwbUPwZuYgjVZQk1OWEOyWHm1D_X1c4VN_dMY_y96o5YwM_rLanWyQWp9b7OGIpDcI"
        async with aiohttp.ClientSession() as session:
            webhook = Webhook.from_url(hookurl,
                                       adapter=AsyncWebhookAdapter(session))
            await webhook.send(text,
                               username=userprovided)

@app.errorhandler(404)
async def page_not_found(e):
    return await render_template("error.html",errordata= "Sorry but the page you are looking for has been removed or is temporarily unavailable.",url="https://TestBOT.thejavaprogramm.repl.co/dashboard")

@app.errorhandler(500)
async def internal_server_error(e):
    return await render_template("error.html",errordata= "Oops the page you were accessing has encountered an unexpected error. Try refreshing the page.",url="https://TestBOT.thejavaprogramm.repl.co/dashboard")
@app.errorhandler(403)
async def page_forbidden(e):
    return await render_template("error.html",errordata= "Seems like the page you were missing access to the page you were looking for.",url="https://TestBOT.thejavaprogramm.repl.co/dashboard")
@app.route("/info")
async def info():
  return redirect(url_for("index"))
@app.route("/")
async def index():
      botAuth=request.args.get('validateAuth')
      if not botAuth==None:
        if botAuth==token:
          print(" Handling a request : "+str((request.args)))
          reqId=request.args.get('requestId')
          print(" Request id : "+str(reqId))
          if not reqId=="Voithos":
            reqOutput=request.args.get('requestOut')
            dict_obj[reqId]=reqOutput
            if reqOutput==None:
              reqError=request.args.get('requestErr')
              reqError=str(reqError).replace("+"," ")
              print(" Request error : "+str(reqError))
              dict_obj[reqId]=reqError
            else:
              print(" Request output : '"+str(reqOutput)+"'")
          else:
            reqError=request.args.get('requestErr')
            reqError=str(reqError).replace("+"," ")
            for key, value in dict_obj.items():
              dict_obj[key]="voithosStart"
      
      return await render_template("index.html", authorized = await discordo.authorized)

@app.route("/dashboard/<int:guild_id>/music")
async def music(guild_id):
  theGuild=None
  user_guilds = await discordo.fetch_guilds()
  for guild in user_guilds:
    if guild.id==guild_id:
      theGuild=guild
  if theGuild==None:
    return await render_template("error.html",errordata= "This guild is not in your guild list.",url="https://TestBOT.thejavaprogramm.repl.co/dashboard")
  return await render_template("music.html",guild=theGuild)
@app.route("/dashboard/<int:guild_id>/moderation")
async def moderation(guild_id):
  theGuild=None
  user_guilds = await discordo.fetch_guilds()
  for guild in user_guilds:
    if guild.id==guild_id:
      theGuild=guild
  if theGuild==None:
    return await render_template("error.html",errordata= "This guild is not in your guild list.",url="https://TestBOT.thejavaprogramm.repl.co/dashboard")
  return await render_template("moderation.html",guild=theGuild)
@app.route("/dashboard/<int:guild_id>/commands")
async def command(guild_id):
  theGuild=None
  user_guilds = await discordo.fetch_guilds()
  for guild in user_guilds:
    if guild.id==guild_id:
      theGuild=guild
  if theGuild==None:
    return await render_template("error.html",errordata= "This guild is not in your guild list.",url="https://TestBOT.thejavaprogramm.repl.co/dashboard")
  return await render_template("commands.html",guild=theGuild)

@app.route("/mute/<int:guild_id>/<string:member>/<string:reason>")
async def mute(guild_id,member,reason):
  theGuild=None
  user_guilds = await discordo.fetch_guilds()
  for guild in user_guilds:
    if guild.id==guild_id:
      theGuild=guild
  if theGuild==None:
    return await render_template("error.html",errordata= "This guild is not in your guild list.",url="https://TestBOT.thejavaprogramm.repl.co/dashboard")
  if not theGuild.permissions.manage_roles:
    return await render_template("error.html",errordata= "You do not have manage role permissions to mute members in this guild.",url=f"https://TestBOT.thejavaprogramm.repl.co/dashboard/{guild_id}")
  author=await discordo.fetch_user()
  timenum=request.args.get('timenum')
  link="https://discord.com/api/webhooks/865629070825750538/RuVdXxNapkUImOILx6O9gna_xhEWdLTUuHCcpAIxW7Z92VczLWnX53sa1JdNBKmK6Lp5"
  getGuilds=f""" 
async def mute_member(guildid,member,author,timenum,reason):
  theGuild=client.get_guild(guildid)
  if theGuild==None:
    raise commands.CommandError(f"The guild with id "+str(guildid)+" was not found .")
    return
  memberobj=None
  if member.isdecimal():
    memberobj=await theGuild.query_members(user_ids=int(member))
    if memberobj==None:
      raise commands.CommandError(f"The member of id "+str(member)+" was not found in "+str(theGuild))
      return
    memberobj=memberobj[0]
  else:
    memberobj=await theGuild.query_members(query=member)
    if memberobj==None:
      raise commands.CommandError(f"The member of name "+str(member)+" was not found in "+str(theGuild))
      return
  print(memberobj)
  await mutemember(theGuild,author,memberobj,timenum,reason)

client.loop.create_task(mute_member({guild_id},'{member}','{author}','{timenum}','{reason}'))
"""
  randomisedStr=genrandomstr(20)
  while randomisedStr in listOfAuth:
    randomisedStr=genrandomstr(20)
  listOfAuth.append(randomisedStr)
  await sendwebhook(getGuilds,randomisedStr,link)
  dict_obj.add(randomisedStr,"waiting")
  while dict_obj[randomisedStr]=="waiting":
    await asyncio.sleep(0.005)
  if dict_obj[randomisedStr]=="voithosStart":
    return await render_template("error.html",url=f"https://TestBOT.thejavaprogramm.repl.co/dashboard",errordata="Bot was offline while requesting data , kindly reload the page.")

  url="https://TestBOT.thejavaprogramm.repl.co/dashboard/"+str(guild_id)+"/moderation"
  if dict_obj[randomisedStr]==None or dict_obj[randomisedStr]=="None" or dict_obj[randomisedStr]=="":
    return redirect(url)
  else:
    return await render_template("error.html",url=f"https://TestBOT.thejavaprogramm.repl.co/dashboard/{guild_id}/moderation",errordata=dict_obj[randomisedStr])

@app.route("/dashboard/<int:guild_id>/prefixes")
async def prefix(guild_id):
  theGuild=None
  user_guilds = await discordo.fetch_guilds()
  for guild in user_guilds:
    if guild.id==guild_id:
      theGuild=guild
  if theGuild==None:
    return await render_template("error.html",errordata= "This guild is not in your guild list.",url="https://TestBOT.thejavaprogramm.repl.co/dashboard")
  link="https://discord.com/api/webhooks/865629070825750538/RuVdXxNapkUImOILx6O9gna_xhEWdLTUuHCcpAIxW7Z92VczLWnX53sa1JdNBKmK6Lp5"
  getGuilds=f""" 
def get_prefix(guildid):
  try:
    return prefixlist[prefixlist.index(guildid) + 1]
  except:
    prefixlist.append(guildid)
    prefixlist.append("vo!")
    return prefixlist[prefixlist.index(guildid) + 1]
print(get_prefix({theGuild.id}))
"""
  randomisedStr=genrandomstr(20)
  while randomisedStr in listOfAuth:
    randomisedStr=genrandomstr(20)
  listOfAuth.append(randomisedStr)
  await sendwebhook(getGuilds,randomisedStr,link)
  dict_obj.add(randomisedStr,"waiting")
  while dict_obj[randomisedStr]=="waiting":
    await asyncio.sleep(0.005)
  if dict_obj[randomisedStr]=="voithosStart":
    return await render_template("error.html",url=f"https://TestBOT.thejavaprogramm.repl.co/dashboard",errordata="Bot was offline while requesting data , kindly reload the page.")
  return await render_template("prefixes.html",guild=theGuild,prefix=str(dict_obj[randomisedStr]))
@app.route("/login")
async def login():
    return await discordo.create_session()

@app.route("/callback")
async def callback():
    errorOcc=request.args.get('error_description')
    if not errorOcc==None:
      errorOcc=errorOcc.replace('+',' ')
      return await render_template("error.html",errordata=errorOcc+".",url="https://TestBOT.thejavaprogramm.repl.co/")
    try:
      data = await discordo.callback()
    except Exception as ex:
      pass
    redirect_to = data.get("redirect", "/")
    return redirect(redirect_to)
@app.route("/playsong/<int:guild_id>/<string:songname>")
@rate_limit(1, timedelta(seconds=1))
async def playsong(guild_id,songname):
  theGuild=None
  user_guilds = await discordo.fetch_guilds()
  for guild in user_guilds:
    if guild.id==guild_id:
      theGuild=guild
  if theGuild==None:
    return await render_template("error.html",errordata="This guild is not in your guild list.",url="https://TestBOT.thejavaprogramm.repl.co/dashboard")
  user=await discordo.fetch_user()
  link="https://discord.com/api/webhooks/865629070825750538/RuVdXxNapkUImOILx6O9gna_xhEWdLTUuHCcpAIxW7Z92VczLWnX53sa1JdNBKmK6Lp5"
  songname=songname.replace("%20"," ")
  getGuilds=f""" 
async def runCode():
    theGuild=client.get_guild({guild_id})
    theMember=theGuild.get_member({user.id})
    songname="{songname}"
    try:
        await theMember.voice.channel.connect()
    except:
      print (" You are not in a voice channel .")
      return
    if validurl(songname):
      videosSearch = VideosSearch(songname,limit=1)
      data = videosSearch.result()
      boolvideoexist=False
    else:
        videosSearch = VideosSearch(songname, limit=1)
        #print(videosSearch.result())
        data = videosSearch.result()
        videoexist = data['result']
        boolvideoexist = not len(videoexist) == 0
    if boolvideoexist:
        vidtitle = data['result'][0]['title']
        try:
            viddes = data['result'][0]['descriptionSnippet'][0]['text']
        except:
            viddes = "No description"
        vidviews = data['result'][0]['viewCount']['text']
        vidpublished = data['result'][0]['publishedTime']
        url = data['result'][0]['link']
    else:
        vidtitle = ""
        viddes = ""
        vidviews = ""
        vidpublished = ""
        url = songname
    player = await YTDLSource.from_url(url,
                                        loop=client.loop,
                                        stream=True)
    try:
        theGuild.voice_client.play(player,
                        after=lambda e: print('Player error: %s' % e)
                        if e else None)
    except:
      print ("Something went wrong while playing song.")
      return
client.loop.create_task(runCode())
"""
  randomisedStr=genrandomstr(20)
  while randomisedStr in listOfAuth:
    randomisedStr=genrandomstr(20)
  listOfAuth.append(randomisedStr)
  await sendwebhook(getGuilds,randomisedStr,link)
  dict_obj.add(randomisedStr,"waiting")
  while dict_obj[randomisedStr]=="waiting":
    await asyncio.sleep(0.005)
  if dict_obj[randomisedStr]=="voithosStart":
    return await render_template("error.html",url=f"https://TestBOT.thejavaprogramm.repl.co/dashboard",errordata="Bot was offline while requesting data , kindly reload the page.")
  url="https://TestBOT.thejavaprogramm.repl.co/dashboard/"+str(guild_id)+"/music"
  if dict_obj[randomisedStr]==None or dict_obj[randomisedStr]=="None" or dict_obj[randomisedStr]=="":
    return redirect(url)
  else:
    return await render_template("error.html",url=f"https://TestBOT.thejavaprogramm.repl.co/dashboard/{guild_id}/music",errordata=dict_obj[randomisedStr])
@app.route("/pausesong/<int:guild_id>/<string:songname>")
@rate_limit(1, timedelta(seconds=1))
async def pausesong(guild_id,songname):
  theGuild=None
  user_guilds = await discordo.fetch_guilds()
  for guild in user_guilds:
    if guild.id==guild_id:
      theGuild=guild
  if theGuild==None:
    return await render_template("error.html",errordata="This guild is not in your guild list.",url="https://TestBOT.thejavaprogramm.repl.co/dashboard")
  user=await discordo.fetch_user()
  link="https://discord.com/api/webhooks/865629070825750538/RuVdXxNapkUImOILx6O9gna_xhEWdLTUuHCcpAIxW7Z92VczLWnX53sa1JdNBKmK6Lp5"
  songname=songname.replace("%20"," ")
  user=await discordo.fetch_user()
  getGuilds=f""" 
async def runCode():
        theGuild=client.get_guild({guild_id})
        theMember=theGuild.get_member({user.id})
        voice=theGuild.voice_client
        try:
            if voice.is_playing():
                voice.pause()
                print(" The voice has been paused successfully.")
                return
            elif voice.is_paused():
                voice.resume()
                print("The voice has been resumed successfully.")
                return
        except:
            print("I cannot find any voice channels.")
            return
client.loop.create_task(runCode())
"""
  randomisedStr=genrandomstr(20)
  while randomisedStr in listOfAuth:
    randomisedStr=genrandomstr(20)
  listOfAuth.append(randomisedStr)
  await sendwebhook(getGuilds,randomisedStr,link)
  dict_obj.add(randomisedStr,"waiting")
  while dict_obj[randomisedStr]=="waiting":
    await asyncio.sleep(0.005)
  if dict_obj[randomisedStr]=="voithosStart":
    return await render_template("error.html",url=f"https://TestBOT.thejavaprogramm.repl.co/dashboard",errordata="Bot was offline while requesting data , kindly reload the page.")
  url="https://TestBOT.thejavaprogramm.repl.co/dashboard/"+str(guild_id)+"/music"
  if dict_obj[randomisedStr]==None or dict_obj[randomisedStr]=="None" or dict_obj[randomisedStr]=="":
    return redirect(url)
  else:
    return await render_template("error.html",url=f"https://TestBOT.thejavaprogramm.repl.co/dashboard/{guild_id}/music",errordata=dict_obj[randomisedStr])
@app.route("/loopsong/<int:guild_id>/<string:songname>")
async def loopsong(guild_id,songname):
  theGuild=None
  user_guilds = await discordo.fetch_guilds()
  for guild in user_guilds:
    if guild.id==guild_id:
      theGuild=guild
  if theGuild==None:
    return await render_template("error.html",errordata="This guild is not in your guild list.",url="https://TestBOT.thejavaprogramm.repl.co/dashboard")
  user=await discordo.fetch_user()
  link="https://discord.com/api/webhooks/865629070825750538/RuVdXxNapkUImOILx6O9gna_xhEWdLTUuHCcpAIxW7Z92VczLWnX53sa1JdNBKmK6Lp5"
  songname=songname.replace("%20"," ")
  getGuilds=f""" 
guildid={guild_id}
userid={user.id}
client.loop.create_task(loopSong('{songname}',guildid,userid))
        
"""
  randomisedStr=genrandomstr(20)
  while randomisedStr in listOfAuth:
    randomisedStr=genrandomstr(20)
  listOfAuth.append(randomisedStr)
  await sendwebhook(getGuilds,randomisedStr,link)
  dict_obj.add(randomisedStr,"waiting")
  while dict_obj[randomisedStr]=="waiting":
    await asyncio.sleep(0.005)
  if dict_obj[randomisedStr]=="voithosStart":
    return await render_template("error.html",url=f"https://TestBOT.thejavaprogramm.repl.co/dashboard",errordata="Bot was offline while requesting data , kindly reload the page.")
  url="https://TestBOT.thejavaprogramm.repl.co/dashboard/"+str(guild_id)+"/music"
  if dict_obj[randomisedStr]==None or dict_obj[randomisedStr]=="None" or dict_obj[randomisedStr]=="":
    return redirect(url)
  else:
    return await render_template("error.html",url=f"https://TestBOT.thejavaprogramm.repl.co/dashboard/{guild_id}/music",errordata=dict_obj[randomisedStr])
@app.route("/stopsong/<int:guild_id>/<string:songname>")
@rate_limit(1, timedelta(seconds=1))
async def stopsong(guild_id,songname):
  theGuild=None
  user_guilds = await discordo.fetch_guilds()
  for guild in user_guilds:
    if guild.id==guild_id:
      theGuild=guild
  if theGuild==None:
    return await render_template("error.html",errordata="This guild is not in your guild list.",url="https://TestBOT.thejavaprogramm.repl.co/dashboard")
  user=await discordo.fetch_user()
  link="https://discord.com/api/webhooks/865629070825750538/RuVdXxNapkUImOILx6O9gna_xhEWdLTUuHCcpAIxW7Z92VczLWnX53sa1JdNBKmK6Lp5"
  songname=songname.replace("%20"," ")
  getGuilds=f""" 
async def runCode():
    theGuild=client.get_guild({guild_id})
    theMember=theGuild.get_member({user.id})
    try:
        await theGuild.voice_client.disconnect()
    except:
        pass
client.loop.create_task(runCode())
        
"""
  randomisedStr=genrandomstr(20)
  while randomisedStr in listOfAuth:
    randomisedStr=genrandomstr(20)
  listOfAuth.append(randomisedStr)
  await sendwebhook(getGuilds,randomisedStr,link)
  dict_obj.add(randomisedStr,"waiting")
  while dict_obj[randomisedStr]=="waiting":
    await asyncio.sleep(0.005)
  if dict_obj[randomisedStr]=="voithosStart":
    return await render_template("error.html",url=f"https://TestBOT.thejavaprogramm.repl.co/dashboard",errordata="Bot was offline while requesting data , kindly reload the page.")
  url="https://TestBOT.thejavaprogramm.repl.co/dashboard/"+str(guild_id)+"/music"
  if dict_obj[randomisedStr]==None or dict_obj[randomisedStr]=="None" or dict_obj[randomisedStr]=="":
    return redirect(url)
  else:
    return await render_template("error.html",url=f"https://TestBOT.thejavaprogramm.repl.co/dashboard/{guild_id}/music",errordata=dict_obj[randomisedStr])
@app.route("/dashboard")
async def user_guilds():
  global listOfAuth
  user_guilds = await discordo.fetch_guilds()
  guild_count=len(user_guilds)
  authguilds=[]
  for guild in user_guilds:
    if guild.permissions.manage_guild:			
      guild.class_color = "green-border" 
    else:
      guild.class_color = "red-border"
    authguilds.append(guild)
  
  authguilds.sort(key = lambda x: x.class_color == "red-border")
  user=await discordo.fetch_user()
  name = user.name
  return await render_template("guilds.html", guild_count = guild_count, guilds = authguilds, username=name,user=user)

@app.route("/changeprefix/<int:guild_id>/<string:prefix>")
@rate_limit(1, timedelta(seconds=1))
async def changeprefix(guild_id,prefix):
  theGuild=None
  user_guilds = await discordo.fetch_guilds()
  for guild in user_guilds:
    if guild.id==guild_id:
      theGuild=guild
  if theGuild==None:
    return await render_template("error.html",errordata= "This guild is not in your guild list.",url="https://TestBOT.thejavaprogramm.repl.co/dashboard")
  if not theGuild.permissions.manage_guild:
    return await render_template("error.html",errordata= "You do not have manage guild permissions to change prefixes in this guild.",url=f"https://TestBOT.thejavaprogramm.repl.co/dashboard/{guild_id}")
  link="https://discord.com/api/webhooks/865629070825750538/RuVdXxNapkUImOILx6O9gna_xhEWdLTUuHCcpAIxW7Z92VczLWnX53sa1JdNBKmK6Lp5"
  getGuilds=f""" 
def set_prefix(guildid,prefix):
  try:
    prefixlist[prefixlist.index(guildid) + 1]=prefix
  except:
    prefixlist.append(guildid)
    prefixlist.append("vo!")
    prefixlist[prefixlist.index(guildid) + 1]=prefix
print(set_prefix({guild_id},'{prefix}'))
"""
  randomisedStr=genrandomstr(20)
  while randomisedStr in listOfAuth:
    randomisedStr=genrandomstr(20)
  listOfAuth.append(randomisedStr)
  await sendwebhook(getGuilds,randomisedStr,link)
  dict_obj.add(randomisedStr,"waiting")
  while dict_obj[randomisedStr]=="waiting":
    await asyncio.sleep(0.005)
  if dict_obj[randomisedStr]=="voithosStart":
    return await render_template("error.html",url=f"https://TestBOT.thejavaprogramm.repl.co/dashboard",errordata="Bot was offline while requesting data , kindly reload the page.")
  url="https://TestBOT.thejavaprogramm.repl.co/dashboard/"+str(guild_id)
  return redirect(url)

@app.route("/dashboard/<int:guild_id>")
async def dashboard_server(guild_id):
  if not await discordo.authorized:
    return redirect(url_for("login"))
  user_guilds=await discordo.fetch_guilds()
  user_guildids=[]
  for guild in user_guilds:
    user_guildids.append(guild.id)
  if not guild_id in user_guildids:
    return await render_template("error.html",errordata= "You do not have permissions to access this guild.",url="https://TestBOT.thejavaprogramm.repl.co/dashboard")
  theGuild=None
  for g in user_guilds:
    if g.id==guild_id:
      theGuild=g
  link="https://discord.com/api/webhooks/865629070825750538/RuVdXxNapkUImOILx6O9gna_xhEWdLTUuHCcpAIxW7Z92VczLWnX53sa1JdNBKmK6Lp5"
  getGuilds=f""" 
def get_guilds():
  listOfGuilds=[]
  for guild in client.guilds:
    listOfGuilds.append(guild.id)
  return listOfGuilds
print(get_guilds())
"""
  randomisedStr=genrandomstr(20)
  while randomisedStr in listOfAuth:
    randomisedStr=genrandomstr(20)
  listOfAuth.append(randomisedStr)
  await sendwebhook(getGuilds,randomisedStr,link)
  dict_obj.add(randomisedStr,"waiting")
  while dict_obj[randomisedStr]=="waiting":
    await asyncio.sleep(0.005)
  if dict_obj[randomisedStr]=="voithosStart":
    return await render_template("error.html",url=f"https://TestBOT.thejavaprogramm.repl.co/dashboard",errordata="Bot was offline while requesting data , kindly reload the page.")
  voithosguilds=list(eval(str(dict_obj[randomisedStr])))
  if not guild_id in voithosguilds:
    if theGuild.permissions.manage_guild:
      return (redirect(f"https://discord.com/api/oauth2/authorize?client_id=805030662183845919&permissions=2419453014&scope=bot&guild_id={guild_id}"))
    else:
      return await render_template("error.html",errordata= "You do not have permissions to invite this bot to that guild.",url="https://TestBOT.thejavaprogramm.repl.co/dashboard")
  return await render_template("guild.html",guild=theGuild)



@app.route("/logout/")
async def logout():
    discordo.revoke()
    return redirect(url_for(".index"))

if __name__ == "__main__":
  app.run(host='0.0.0.0')

#client.run(token=token)