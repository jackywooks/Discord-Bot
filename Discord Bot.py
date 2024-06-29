import os
import discord
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")
GUILD = os.getenv("DISCORD_GUILD")
fname = "memberLogon.csv"

intents = discord.Intents.all()
intents.members = True

#create discord client
client = discord.Client(intents=intents)

# create csv file when new connection established
@client.event 
async def on_ready():
    guild = discord.utils.get(client.guilds, name=GUILD) 
    #create a new report writer
    with open(fname, "w") as reportWriter:
        #header
        reportWriter.writelines(["Member Name",",","Join Time","\n"])
        #write every member to the csv
        for member in guild.members:
            reportWriter.writelines([member.name,",",datetime.now().strftime("%m/%d/%Y %H:%M:%S"),"\n"])

@client.event
async def on_member_join(member):
    guild = discord.utils.get(client.guilds, name=GUILD)
    #create a new report writer to append record when a new member join
    with open(fname, "a") as reportWriter:
        #do below when a new member join
        reportWriter.writelines([member.name,",",datetime.now().strftime("%m/%d/%Y %H:%M:%S"),"\n"])
        reportWriter.close()

@client.event
async def on_member_remove(member):
    guild = discord.utils.get(client.guilds, name=GUILD)
    lines = []
    #create a report reader to read through the file
    with open(fname,"r") as reportReader:
        lines = reportReader.readlines()
    #create a new report writer and write only if the lines of memeber that exist
    with open(fname, "w") as reportWriter:
        for line in lines:
            #remove the line if the member name match exactly as the value before the first delimeter (,)
            if not line.startswith(f"{member.name},"):
                reportWriter.writelines([line.strip(),"\n"])
        
# Run the bot
client.run(TOKEN)