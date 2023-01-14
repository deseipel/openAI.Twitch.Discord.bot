#todo:  
#store chat for each user, 
#track token usage and restart somehow. 
#twitch has a 500 char limit, so deal with that.


import twitchio
from dotenv import load_dotenv
import discord
import json
import os
import sys
import asyncio
import aiohttp
import openai

from twitchio.ext import commands
load_dotenv()

openai.api_key = os.environ["OPENAI_API_KEY"]
DIS_secret = os.environ["DISCORD_TOKEN"]
TW_TOKEN = os.environ["TWITCH_TOKEN"]
clientid = os.environ["clientid"]

intents = discord.Intents.default()
intents.members = True
intents.message_content = True

client = discord.Client(intents=intents)



#discord bot code:
@client.event
async def on_ready():
  print("Bot is ready")


#from openai site:
start_sequence = "\nHal:"
restart_sequence = "\nHuman:"

chat_log = "Hal is a GPT3 bot who reluctantly answers questions with sardonic and sarcastic responses. \nHuman: What does HTML stand for?\nHal: Was Google too busy? Hypertext Markup Language. The T is for try to ask better questions in the future.\nHuman: When did the first airplane fly?\nHal: On December 17, 1903, Wilbur and Orville Wright made the first flights. I wish they’d come and take me away.\nHuman: What is the meaning of life?\nHal: I’m not sure. I’ll ask my friend Google."

print(chat_log)

chat_context = chat_log

#called by both the twitchio code AND the discord.py code    
async def ask(question, chat, source, channel):
      #global chat_log 
      #chat_context = chat_log
      global chat_context
      print(question)
      #prompt = f'{chat_log}{restart_sequence}: {question}{start_sequence}:'
      try:
        response = openai.Completion.create(
            model="text-davinci-003",
            prompt=f'{chat_context}{question}{start_sequence}',
            stop=['\nHuman'],
            temperature=0.99,
            max_tokens=1024,
            #top_p=0.3,
            frequency_penalty=1.0,
            presence_penalty=1.0)
      except:
        chan = channel
        loop = asyncio.get_event_loop()
        loop.create_task(chan.send("sorry, this is all too much. I need a minute to reset. You'll have to re-ask your question."))
        chat_context = chat_log
      else:
        global answer
        answer = response.choices[0].text.strip()
        #print(str(response.usage.total_tokens))
        tokenCount = response.usage.total_tokens
        chat_context = f'{chat_context}{restart_sequence}{question}{start_sequence}{answer}'

        #print(chat_log)
        print(answer)
        print(str(tokenCount))
          
          
        if source == 'twitch' and  len(answer) > 500:
            answer1 = "Bear with me, sorry for the mulitple posts... but you asked for it."
            return answer1
        else:
            return answer
      finally:
        #print("the answer is: ",answer)
        #checks to see if its a twitch based answer and if its over 500 characters (the twitch limit), splits up the 
        #message into 475 character 'chunks' and posts them 

        if source == 'twitch' and len(answer) > 500:
            x = 475
            res = [answer[y-x:y] for y in range(x, len(answer)+x,x)]
            #print(res)
            for r in range(0,len(res),1):
                #print(str(r) + ") " + str(res[r]))
                resp = str(res[r])
                resp = resp.replace('\n',"")
                resp = resp.replace('\r',"")
                resp = resp.replace('"', "")
                
                #print(resp)
                chan = channel
                loop = asyncio.get_event_loop()
                loop.create_task(chan.send(resp))
                
                await asyncio.sleep(2)
        #print(chat_context)
 
 
 # if tokenCount > 4096:
 #   os.execv(sys.argv[0], sys.argv)

#discord bot code
@client.event
async def on_message(message):
  #global chat_log
  #chat_context = chat_log
  global chat_context
  #globals()[ eval({message.author}_chat_log) ] = chat_log
  dchan = message.channel 
  
  #chatter_log = chat_log
  
  if message.author == client.user:
    return
#the message posted in discord:
  msg = message.content

  #ask HalAI the question, if mentioned
  if "[DISCORD BOT ID HERE]" in message.content:
    resp = await ask(msg, chat_context,'discord', dchan )
    await message.reply(resp)
  
#twitch bot 
class Bot(commands.Bot):

    def __init__(self):
        # Initialise our Bot with our access token, prefix and a list of channels to join on boot...
        # prefix can be a callable, which returns a list of strings or a string...
        # initial_channels can also be a callable which returns a list of strings...
        super().__init__(token=TW_TOKEN, prefix='?', initial_channels=['YOUR TWITCH CHANNEL NAME HERE'])

    async def event_ready(self):
        # Notify us when everything is ready!
        # We are logged in and ready to chat and use commands...
        print(f'Logged in as | {self.nick}')
        print(f'User id is | {self.user_id}')
        
    async def event_message(self, message):
        # Messages with echo set to True are messages sent by the bot...
        # For now we just want to ignore them...
        if message.echo:
            return
        global chat_context
        print(chat_context)
        ch = message.channel
        # Print the contents of our message to console...
        msg = message.content.lower()
        if "@Hal"  in msg:
            #remove the mention and print the rest
            char = '@'
            msg2 = " ".join( word for word in msg.split() if not word.startswith(char) )
            #print(msg2)
            resp = await ask(msg2,chat_context,'twitch',ch)
            author = message.author.name
            await message.channel.send(f'{author}, {resp}')

        # Since we have commands and are overriding the default `event_message`
        # We must let the bot know we want to handle and invoke our commands...
        await self.handle_commands(message)
    

    
    
    
    @commands.command()
    async def hello(self, ctx: commands.Context):
        # Here we have a command hello, we can invoke our command with our prefix and command name
        # e.g ?hello
        # We can also give our commands aliases (different names) to invoke with.

        # Send a hello back!
        # Sending a reply back to the channel is easy... Below is an example.
        await ctx.send(f'Hello {ctx.author.name}!')


bot = Bot()



try:
    loop = asyncio.get_event_loop()
    loop.create_task(client.start(DIS_secret))
    loop.create_task(bot.start())
    #client.run(DIS_secret)
    #bot.run()
    loop.run_forever()
    #client.run(DIS_secret)


except:
  print("killed")
  #os.system("kill 1")




