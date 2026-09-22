import os
import random
import threading
import aiohttp
from flask import Flask
import discord
from discord.ext import commands

# 1. Background web server to keep Render Web Service alive
app = Flask('')

@app.route('/')
def home():
    return "Hermes is running!"

def run_web():
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port)

threading.Thread(target=run_web, daemon=True).start()

# 2. Discord bot setup
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")

# 3. Custom Commands
@bot.command(name="ping", help="Checks Hermes' response time.")
async def ping(ctx):
    latency = round(bot.latency * 1000)
    await ctx.send(f"🏓 Pong! Latency: `{latency}ms`")

@bot.command(name="trivia", help="Generates a random gaming trivia question.")
async def trivia(ctx):
    url = "https://opentdb.com/api.php?amount=1&category=15&type=multiple"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            data = await resp.json()
            if not data.get("results"):
                return await ctx.send("Could not grab trivia right now.")
            
            item = data["results"][0]
            question = (
                item["question"]
                .replace("&quot;", '"')
                .replace("&#039;", "'")
                .replace("&amp;", "&")
            )
            correct = item["correct_answer"]
            options = item["incorrect_answers"] + [correct]
            random.shuffle(options)
            choices = "\n".join([f"• {opt}" for opt in options])
            
            await ctx.send(
                f"🎮 **Gaming Trivia:**\n{question}\n\n**Choices:**\n{choices}\n\n*(Reveal answer: ||{correct}||)*"
            )

@bot.command(name="drop", help="Decides a tactical drop point or plan.")
async def drop(ctx, *locations):
    if not locations:
        locations = ["Military Base", "North Compound", "Hot Drop Airfield", "Loot Outskirts", "Town Center"]
    choice = random.choice(locations)
    await ctx.send(f"🎯 **Hermes orders:** Drop at **{choice}**!")

@bot.command(name="roll", help="Rolls a die (e.g. !roll 20).")
async def roll(ctx, sides: int = 6):
    result = random.randint(1, max(sides, 1))
    await ctx.send(f"🎲 Rolled a **{result}** (1-{sides})")

# 4. Start the bot
bot.run(os.getenv("DISCORD_TOKEN"))
