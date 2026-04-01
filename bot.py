import os
import discord
from discord.ext import commands, tasks
from datetime import datetime, time
from zoneinfo import ZoneInfo

TOKEN = os.getenv("DISCORD_TOKEN")
CHANNEL_ID = 1443873834045407232

HEURE_RAPPEL = time(hour=7, minute=0, tzinfo=ZoneInfo("Europe/Zurich"))

intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"Connecté en tant que {bot.user}")
    if not rappel.is_running():
        rappel.start()

@tasks.loop(time=HEURE_RAPPEL)
async def rappel():
    aujourd_hui = datetime.now(ZoneInfo("Europe/Zurich")).weekday()

    channel = bot.get_channel(CHANNEL_ID)
    if channel is None:
        print("Salon introuvable")
        return

    if aujourd_hui == 0:
        message = "@everyone Bon début de semaine 💪 N'oubliez pas de pointer !"
    elif 1 <= aujourd_hui <= 3:
        message = "@everyone N'oubliez pas de pointer ✅"
    elif aujourd_hui == 4:
        message = "@everyone N'oubliez pas de pointer ✅ C'est bientôt le week-end 🎉"
    else:
        return

    await channel.send(
        message,
        allowed_mentions=discord.AllowedMentions(everyone=True)
    )

@rappel.before_loop
async def before():
    await bot.wait_until_ready()

if not TOKEN:
    raise ValueError("La variable d'environnement DISCORD_TOKEN est manquante.")

bot.run(TOKEN)