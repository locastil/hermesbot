import os
import random
import threading
import aiohttp
from flask import Flask
from groq import Groq
import discord
from discord.ext import commands

# 1. Background web server to keep Render service alive
app = Flask('')

@app.route('/')
def home():
    return "Hermes is running!"

def run_web():
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port)

threading.Thread(target=run_web, daemon=True).start()

# 2. AI & Discord Client Setup
groq_client = Groq(api_key=os.getenv("GROQ_API_KEY"))

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

SYSTEM_PROMPT = (
    "You are Hermes, the witty, sharp, and charismatic patron bot of the WASD Gaming Community. "
    "Keep responses punchy, conversational, and game-savvy. Talk naturally like a community regular on Discord."
)

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")

# 3. Conversational AI Listener
@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    is_mentioned = bot.user in message.mentions or "hermes" in message.content.lower()

    if is_mentioned and not message.content.startswith("!"):
        clean_text = message.clean_content.replace(f"@{bot.user.name}", "").strip()
        
        async with message.channel.typing():
            try:
                chat_completion = groq_client.chat.completions.create(
                    messages=[
                        {"role": "system", "content": SYSTEM_PROMPT},
                        {"role": "user", "content": clean_text or "Hey Hermes!"}
                    ],
                    model="llama-3.3-70b-versatile",
                    max_tokens=250,
                )
                reply = chat_completion.choices[0].message.content
                await message.reply(reply)
            except Exception as e:
                await message.reply("⚡ My connection glitched out for a second.")
                print(f"AI Error: {e}")

    # Keeps prefix commands functioning
    await bot.process_commands(message)

# 4. Standard Commands
@bot.command(name="ping")
async def ping(ctx):
    await ctx.send(f"🏓 Pong! `{round(bot.latency * 1000)}ms`")

@bot.command(name="trivia")
async def trivia(ctx):
    url = "https://opentdb.com/api.php?amount=1&category=15&type=multiple"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            data = await resp.json()
            if not data.get("results"):
                return await ctx.send("Could not grab trivia right now.")
            item = data["results"][0]
            question = item["question"].replace("&quot;", '"').replace("&#039;", "'").replace("&amp;", "&")
            correct = item["correct_answer"]
            options = item["incorrect_answers"] + [correct]
            random.shuffle(options)
            choices = "\n".join([f"• {opt}" for opt in options])
            await ctx.send(f"🎮 **Gaming Trivia:**\n{question}\n\n**Choices:**\n{choices}\n\n*(Reveal: ||{correct}||)*")

@bot.command(name="drop")
async def drop(ctx, *locations):
    if not locations:
        locations = ["Military Base", "North Compound", "Hot Drop Airfield", "Loot Outskirts", "Town Center"]
    choice = random.choice(locations)
    await ctx.send(f"🎯 **Hermes orders:** Drop at **{choice}**!")

@bot.command(name="roll")
async def roll(ctx, sides: int = 6):
    result = random.randint(1, max(sides, 1))
    await ctx.send(f"🎲 Rolled a **{result}** (1-{sides})")

bot.run(os.getenv("DISCORD_TOKEN"))
