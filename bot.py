import os
import discord
import asyncio
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()

intents = discord.Intents.default()

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    await bot.tree.sync()
    print(f"Conectado como {bot.user}")

async def main():
    await bot.load_extension("slashCommands.ping")
    await bot.load_extension("slashCommands.hardwarestatus")
    await bot.load_extension("cogs.monitor")

    
    
    print("Slash commands sincronizados")
    await bot.start(os.getenv("DISCORD_TOKEN"))

asyncio.run(main())