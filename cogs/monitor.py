import os
import discord
import psutil
from discord.ext import commands, tasks
from dotenv import load_dotenv
import requests

load_dotenv()

TEMP_LIMIT = int(os.getenv("TEMPERATURE_LIMIT")) or 60 # °C
INTERVAL = int(os.getenv("INTERVAL")) or 30  # intervalo de segundos
USER_ID = int(os.getenv("USER_ID")) or 0

class Monitor(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.temp_limit = TEMP_LIMIT
        self.user_id = USER_ID
        self.monitor_task.start()

    def cog_unload(self):
        self.monitor_task.cancel()

    def get_cpu_temp(self):
        try:
            # Chama o servidor do LibreHardwareMonitor
            data = requests.get("http://localhost:8085/data.json", timeout=3).json()
        except Exception as e:
            print("Erro ao acessar LibreHardwareMonitor:", e)
            return None

        def walk(node):
            if "Children" in node:
                for child in node["Children"]:
                    result = walk(child)
                    if result is not None:
                        return result

            if node.get("Text", "").startswith("Temperatures"):
                for child in node["Children"]:
                    if child.get("Text", "").startswith("CPU"):
                        return float(child["Value"].replace("ºC", "").replace("°C", "").replace(",", ".").strip())
        return walk(data)
        
        

    @tasks.loop(seconds=INTERVAL)
    async def monitor_task(self):
        temp = None
        try:
            temp = psutil.sensors_temperatures()
        except Exception as e:
            print(e)
            temp = None

        if not temp:
            temp = self.get_cpu_temp()
            if not temp:
                print("Erro ao fornecer temperatura: requisitos no sistema operacional não suportados.")
        if temp and temp >= self.temp_limit:
            await self.send_alert(temp)

    async def send_alert(self, temp):
        embed = discord.Embed(
            title="ALERTA DE TEMPERATURA:",
            description="Temperatura acima do normal",
            color=discord.Color.red()
        )
        embed.add_field(name="Temperatura", value=f"{temp}°C")
        
        try:
            user = await self.bot.fetch_user(self.user_id)
            await user.send(embed=embed)
        except discord.Forbidden:
            print("Usuário bloqueou DM")
        except Exception as e:
            print(e)

async def setup(bot: commands.Bot):
    await bot.add_cog(Monitor(bot))