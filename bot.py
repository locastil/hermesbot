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
     
question = random.choice(questions)
await ctx.send(f"🧠 Trivia question: {question['question']}")
     
try:
      answer = await bot.wait_for('message', timeout=15.0, check=lambda m: m.author == ctx.author)
      if answer.content.lower() == question['answer'].lower():
            await ctx.send("🎉 Correct! You're a trivia master!")
      else:
            await ctx.send(f"❌ Wrong! The correct answer is: {question['answer']}")
except asyncio.TimeoutError:
              await ctx.send(f"⏰ Time's up! The correct answer is: {question['answer']}")
@bot.command()
async def echo(ctx, *, text: str):
          """Repeat back what the user says, but with flair"""
          if text.lower() in ["quit", "stop", "exit"]:
              await ctx.send("🛑 Alright, I'll stop talking. But you'll miss my wit!")
              return
     
          responses = [
              f"Ah, you said: \"{text}\" 🤭",
              f"Interesting... you mentioned: \"{text}\" 🤔",
              f"Did you just say: \"{text}\"? Fascinating! 🧠",
              f"Ah, \"{text}\"... how intriguing! 🌟",
              f"You utter: \"{text}\"... I shall remember that. 🧾"
          ]
          await ctx.send(random.choice(responses))
     
@bot.command()
      async def help(ctx):
          """Show available commands with a fun twist"""
          embed = discord.Embed(
              title="🌈 Welcome to the Whimsical Bot!",
              description="I'm your companion for fun and games! 🎭",
              color=discord.Color.purple()
          )
     
          embed.add_field(name="!hello", value="Greet the bot with a whimsical response", inline=False)
          embed.add_field(name="!joke", value="Tell a random joke", inline=False)
          embed.add_field(name="!fortune", value="Receive a silly fortune cookie", inline=False)
          embed.add_field(name="!trivia", value="Answer a fun trivia question", inline=False)
          embed.add_field(name="!echo [text]", value="Repeat back what you say, but with flair", inline=False)
          embed.add_field(name="!help", value="Show this help message", inline=False)
     
          embed.set_footer(text="Have fun! 🎉")
          await ctx.send(embed=embed)
     
      # Error handling
      @bot.listen()
      async def on_command_error(ctx, error):
          if isinstance(error, commands.CommandNotFound):
              await ctx.send("🤷‍♀️ I don't know that command. Type !help for a list of commands.")
          elif isinstance(error, commands.MissingRequiredArgument):
              await ctx.send("⚠️ You forgot to provide an argument. Try again!")
          else:
              await ctx.send(f"🩸 Something went wrong: {str(error)}")
     
      # Run the bot
      bot.run("YOUR_BOT_TOKEN")
