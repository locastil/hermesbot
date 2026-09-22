
import discord
      2 from discord.ext import commands
      3 import random
      4 import asyncio
      5 from datetime import datetime
      6
      7 # Set up the bot with intents
      8 intents = discord.Intents.default()
      9 intents.message_content = True
     10 intents.members = True
     11
     12 bot = commands.Bot(
     13     command_prefix="!",
     14     intents=intents,
     15     help_command=None  # We'll create our own help system
     16 )
     17
     18 # Joke collection
     19 jokes = [
     20     "Why did the scarecrow win an award? Because he was outstanding in his field!",
     21     "What do you call fake spaghetti? An impasta!",
     22     "Why don't skeletons fight each other? They don't have the guts.",
     23     "What do you get when you cross a snowman and a vampire? Frostbite!",
     24     "Why did the math book look sad? Because it had too many problems."
     25 ]
     26
     27 # Fortune cookies
     28 fortunes = [
     29     "You will find treasure in unexpected places.",
     30     "Today is a good day to wear something colorful.",
     31     "Your creativity will shine bright today.",
     32     "You'll meet someone who will change your perspective.",
     33     "A long journey begins with a single step."
     34 ]
     35
     36 @bot.event
     37 async def on_ready():
     38     print(f"🎉 {bot.user.name} is online!")
     39     await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.playing, name="being silly"))
     41 @bot.command()
     42 async def hello(ctx):
     43     """Greet the bot with a whimsical response"""
     44     responses = [
     45         "Hello, my dear! 🌟",
     46         "Oh, hello there! 👋",
     47         "Greetings, traveler! 🧙‍♂️",
     48         "Howdy partner! 🐎",
     49         "Salutations! 🪐"
     51     await ctx.send(random.choice(responses))
     52
     53 @bot.command()
     54 async def joke(ctx):
     55     """Tell a random joke"""
     56     await ctx.send("😄 Here's a joke for you:")
     57     await asyncio.sleep(1)
     58     await ctx.send(random.choice(jokes))
     59
     60 @bot.command()
     61 async def fortune(ctx):
     62     """Receive a silly fortune cookie"""
     63     await ctx.send("🥠 Here's your fortune:")
     64     await asyncio.sleep(1)
     65     await ctx.send(random.choice(forturnes))  # <-- Note: Typo here (fortunes → fountunes)
     66
     67 @bot.command()
     68 async def trivia(ctx):
     69     """Answer a fun trivia question"""
     70     questions = [
     71         {"question": "What is the fastest land animal?", "answer": "Cheetah"},
     72         {"question": "How many bones do humans have?", "answer": "206"},
     73         {"question": "What is the capital of France?", "answer": "Paris"},
     74         {"question": "What is 2+2?", "answer": "4"},
     75         {"question": "What color is the sky on a clear day?", "answer": "Blue"}
     76     ]
     77
     78     question = random.choice(questions)
     79     await ctx.send(f"🧠 Trivia question: {question['question']}")
     80
     81     try:
     82         answer = await bot.wait_for('message', timeout=15.0, check=lambda m: m.author == ctx.author)
     83         if answer.content.lower() == question['answer'].lower():
     84             await ctx.send("🎉 Correct! You're a trivia master!")
     85         else:
     86             await ctx.send(f"❌ Wrong! The correct answer is: {question['answer']}")
     87     except asyncio.TimeoutError:
     88         await ctx.send(f"⏰ Time's up! The correct answer is: {question['answer']}")
     90 @bot.command()
     91 async def echo(ctx, *, text: str):
     92     """Repeat back what the user says, but with flair"""
     93     if text.lower() in ["quit", "stop", "exit"]:
     94         await ctx.send("🛑 Alright, I'll stop talking. But you'll miss my wit!")
     95         return
     96
     97     responses = [
     98         f"Ah, you said: \"{text}\" 🤭",
     99         f"Interesting... you mentioned: \"{text}\" 🤔",
     100         f"Did you just say: \"{text}\"? Fascinating! 🧠",
     101         f"Ah, \"{text}\"... how intriguing! 🌟",
     102         f"You utter: \"{text}\"... I shall remember that. 🧾"
     103     ]
     104     await ctx.send(random.choice(responses))
     105
 106 @bot.command()
     107 async def help(ctx):
     108     """Show available commands with a fun twist"""
     109     embed = discord.Embed(
     110         title="🌈 Welcome to the Whimsical Bot!",
     111         description="I'm your companion for fun and games! 🎭",
     112         color=discord.Color.purple()
     113     )
     114
     115     embed.add_field(name="!hello", value="Greet the bot with a whimsical response", inline=False)
     116     embed.add_field(name="!joke", value="Tell a random joke", inline=False)
     117     embed.add_field(name="!fortune", value="Receive a silly fortune cookie", inline=False)
     118     embed.add_field(name="!trivia", value="Answer a fun trivia question", inline=False)
     119     embed.add_field(name="!echo [text]", value="Repeat back what you say, but with flair", inline=False)
     120     embed.add_field(name="!help", value="Show this help message", inline=False)
     121
     122     embed.set_footer(text="Have fun! 🎉")
     123     await ctx.send(embed=embed)
     124
     125 # Error handling
     126 @bot.listen()
     127 async def on_command_error(ctx, error):
     128     if isinstance(error, commands.CommandNotFound):
     129         await ctx.send("🤷‍♀️ I don't know that command. Type !help for a list of commands.")
     130     elif isinstance(error, commands.MissingRequiredArgument):
     131         await ctx.send("⚠️ You forgot to provide an argument. Try again!")
     132     else:
     133         await ctx.send(f"🩸 Something went wrong: {str(error)}")
     134
     135 # Run the bot
     136 bot.run("YOUR_BOT_TOKEN")
