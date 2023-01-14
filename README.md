# openAI.Twitch.Discord.bot
this is a chat bot for Twitch AND Discord that uses Open.AI's GPT3 model.  when it runs, the bot will respond in either Twitch or Discord, depending on where the 
question came from.  I built this for my own Twitch channel (https://twitch.tv/deseipel) and Discord server, so you may need to edit it for your needs.  I didn't build this to be a universal bot. 


Prequisites:
Open AI Account/Key

Discord Bot account/Key

Twitch bot account/key

TwitchIO

Discord.py

OpenAI


This is a locally run python-based bot for Twitch and Discord that uses the OpenAI GPT3 model/API.  I don't call myself a programmer, so if you see my code and 
laugh at how 'wrong' it is, be a good human and lemme know.  I'll gladly try to fix it.  It 

You'll need to create a .env file to store your discord, twitch & OpenAI tokens.  Once you have all that setup (not a trivial task, but I am not getting into how 
to do all that), you just open a cmd prompt or terminal and use python to run it.  for example, if the file is named main.py, you'd run "python main.py".  

Twitter limits chat messages to 500 characters, so I've accounted for that the best I can.  

OpenAI limits the 'prompt' to 4000-ish 'tokens' which I've also tried to account for.  
