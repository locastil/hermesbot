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
     
      # Run the bot
bot.run("YOUR_BOT_TOKEN")
