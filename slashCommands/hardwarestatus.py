import discord
import psutil
from discord.ext import commands
import requests

class StatusMonitor(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

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
        
        

    async def get_status(self):
        cpu = psutil.cpu_percent(interval=1)
        ram = psutil.virtual_memory().percent
        temp = None
        try:
            temps = psutil.sensors_temperatures()
            if temps:
                for entries in temps.values():
                    for entry in entries:
                        if entry.current:
                            temp = entry.current
                            break
        except Exception:
            pass

        if temp is None:
            temp = self.get_cpu_temp()

        return cpu, ram, temp


    @discord.app_commands.command(
        name="hardwarestatus",
        description="Mostra o status do computador"
    )
    async def hardware_status(self, interaction: discord.Interaction):
        cpu, ram, temp = await self.get_status()

        embed = discord.Embed(
            title="🖥️ STATUS DO COMPUTADOR",
            color=discord.Color.blue()
        )
        embed.add_field(name="CPU", value=f"{cpu}%")
        embed.add_field(name="RAM", value=f"{ram}%")
        embed.add_field(
            name="Temperatura",
            value=f"{temp}°C" if temp is not None else "Não suportado"
        )

        await interaction.response.send_message(embed=embed)

async def setup(bot: commands.Bot):
    await bot.add_cog(StatusMonitor(bot))