import random
import aiohttp

# 1. Latency check
@bot.command(name="ping", help="Checks Hermes' response time to the server.")
async def ping(ctx):
    latency = round(bot.latency * 1000)
    await ctx.send(f"🏓 Pong! Latency: `{latency}ms`")

# 2. Interactive Video Game Trivia
@bot.command(name="trivia", help="Generates a random gaming trivia question.")
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
            
            # Put options together
            options = item["incorrect_answers"] + [correct]
            random.shuffle(options)
            choices = "\n".join([f"• {opt}" for opt in options])
            
            await ctx.send(
                f"🎮 **Gaming Trivia:**\n{question}\n\n**Choices:**\n{choices}\n\n*(Reveal answer: ||{correct}||)*"
            )

# 3. Squad Drop Picker / Decision Maker
@bot.command(name="drop", help="Decides a tactical drop point or plan for the squad.")
async def drop(ctx, *locations):
    if not locations:
        locations = ["Military Base", "North Compound", "Hot Drop Airfield", "Loot Outskirts", "Town Center"]
    choice = random.choice(locations)
    await ctx.send(f"🎯 **Hermes orders:** Drop at **{choice}**!")

# 4. Dice / Stat Roller
@bot.command(name="roll", help="Rolls a die between 1 and a given number (e.g. !roll 20).")
async def roll(ctx, sides: int = 6):
    result = random.randint(1, max(sides, 1))
    await ctx.send(f"🎲 Rolled a **{result}** (1-{sides})")


import os
import threading
from flask import Flask
import discord
from discord.ext import commands

# 1. Dummy web server so Render knows the service is alive
app = Flask('')

@app.route('/')
def home():
    return "Bot is running!"

def run():
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port)

threading.Thread(target=run, daemon=True).start()

# 2. Discord bot logic
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")

# (Keep your existing @bot.command trivia/other functions here)

# 3. Connect using the DISCORD_TOKEN you set in Render
bot.run(os.getenv("DISCORD_TOKEN"))

import discord
from discord.ext import commands
import random
import asyncio
from datetime import datetime
      
       # Set up the bot with intents
intents = discord.Intents.default()
intents.message_content = True
intents.members = True
     
bot = commands.Bot(
      command_prefix="!",
      intents=intents,
      help_command=None  # We'll create our own help system
      )
     
      # Joke collection
jokes = [
      "Why did the scarecrow win an award? Because he was outstanding in his field!",
      "What do you call fake spaghetti? An impasta!",
      "Why don't skeletons fight each other? They don't have the guts.",
      "What do you get when you cross a snowman and a vampire? Frostbite!",
      "Why did the math book look sad? Because it had too many problems."
      ]
     
      # Fortune cookies
fortunes = [
      "You will find treasure in unexpected places.",
      "Today is a good day to wear something colorful.",
      "Your creativity will shine bright today.",
      "You'll meet someone who will change your perspective.",
      "A long journey begins with a single step."
      ]
     
@bot.event
async def on_ready():
      print(f"🎉 {bot.user.name} is online!")
      await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.playing, name="being silly"))
@bot.command()
async def hello(ctx):
      """Greet the bot with a whimsical response"""
      responses = [
      "Hello, my dear! 🌟",
      "Oh, hello there! 👋",
      "Greetings, traveler! 🧙‍♂️",
      "Howdy partner! 🐎",
      "Salutations! 🪐",
      await ctx.send(random.choice(responses))
]      
      @bot.command()
      async def joke(ctx):
          """Tell a random joke"""
          await ctx.send("😄 Here's a joke for you:")
          await asyncio.sleep(1)
          await ctx.send(random.choice(jokes))
     
      @bot.command()
      async def fortune(ctx):
          """Receive a silly fortune cookie"""
          await ctx.send("🥠 Here's your fortune:")
          await asyncio.sleep(1)
          await ctx.send(random.choice(forturnes))  # <-- Note: Typo here (fortunes → fountunes)
     
      @bot.command()
      async def trivia(ctx):
           """Answer a fun trivia question"""
questions = [
      {"question": "What is the fastest land animal?", "answer": "Cheetah"},
      {"question": "How many bones do humans have?", "answer": "206"},
      {"question": "What is the capital of France?", "answer": "Paris"},
      {"question": "What is 2+2?", "answer": "4"},
      {"question": "What color is the sky on a clear day?", "answer": "Blue"}
          ]
