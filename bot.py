import os
import discord
from discord.ext import commands
import random
import json
import asyncio

# --- Bot Setup ---
intents = discord.Intents.default()
intents.messages = True
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

# --- Database File ---
DATABASE_FILE = 'database.json'

def load_data():
    """Loads data from the JSON file."""
    try:
        with open(DATABASE_FILE, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return {"jokes": [], "learned_phrases": []}

def save_data(data):
    """Saves data to the JSON file."""
    with open(DATABASE_FILE, 'w') as f:
        json.dump(data, f, indent=4)

# --- Dracula Flow Speech Components (Based on TV Tropes analysis) ---
dracula_openers = [
    "This shit ain't nothin' to me, man!", "They must have amnesia, they forgot that I'm him!",
    "We straight gassin', cuttin' straight to the bricks!", "Listen...", "Blah!"
]
dracula_boasts = [
    "my Audemars Piguet is worth the GDP of Yemen.", "I'm back to back with God, shaking the fucking universe.",
    "I was flippin' bricks for Mansa Musa before y'all even became a type-1 civilization!",
    "I'm him! I've been him! I will continue to be him!",
    "I walked across the sand dunes of the Sahara Desert for 40 days and 40 nights with nothing but a pack of Newports and a fifth of Henny.",
    "my cock is sanded down smooth!", "I'm 12 million years old!", "I got strands of RNA in my hookah! Every puff is an insult to God!"
]
dracula_threats = [
    "I threw the opp in the particle collider; watched his ass get pulled apart into a million pieces, turned his sorry ass into some data!",
    "The last guy who ran off on the pack got choked out by some Givenchy gloves; the last thing he ever saw was the price tag on them.",
    "I psychologically terrorized the opp until he killed himself at the Michael Jordan Steakhouse!",
    "Reach for my neck, you'll get turned into an example!",
    "The weed will have you in purgatory, screaming for eternity!",
    "I put him on the news and turned him into a real superstar!"
]
dracula_non_sequiturs = [
    "I was at the Battle of Jericho, taunting both sides with my cock out.",
    "I'm gulping sea monkeys by the gallon, my tummy feel crazy!",
    "If Santa come down my chimney, I'mma fuck him!",
    "I can't tell if I want to kill my opps or fuck 'em!",
    "I'm trying to explain to the cop that we’re all just atoms so he might as well let me go!"
]
dracula_closers = [
    "This shit ain't nothing to me, man!", "I really do this shit!", "Sounds like her problem to me, ha ha!",
    "I'm a real glutton! AH!", "There are consequences to your crimes against Dracula!"
]

# --- Bot Events ---
@bot.event
async def on_ready():
    print(f'Bot is logged in as {bot.user.name}')
    print('------')

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    if not message.content.startswith('!'):
        data = load_data()
        for phrase in data['learned_phrases']:
            if phrase.lower() in message.content.lower():
                await asyncio.sleep(random.uniform(0.5, 1.5))
                if data['jokes']:
                    await message.channel.send(random.choice(data['jokes']))
                break
    await bot.process_commands(message)

# --- Commands ---

@bot.command()
async def joke(ctx):
    """Tells a random joke from memory."""
    data = load_data()
    if data['jokes']:
        await ctx.send(random.choice(data['jokes']))
    else:
        await ctx.send("The hivemind knows no jokes. The master must edit the database.")

@bot.command()
async def learn(ctx, *, phrase: str):
    """Teaches the bot a new phrase to listen for."""
    data = load_data()
    phrase = phrase.lower()
    if phrase not in data['learned_phrases']:
        data['learned_phrases'].append(phrase)
        save_data(data)
        await ctx.send(f"Affirmative. The concept '{phrase}' has been assimilated.")
    else:
        await ctx.send("The hivemind is already aware of that concept.")

@bot.command()
async def dracula(ctx):
    """Speaks with the true Dracula Flow."""
    # Construct a 2-4 line monologue
    num_lines = random.randint(2, 4)
    lines = [random.choice(dracula_openers)]
    
    # Create a pool of lines to avoid repetition
    line_pool = dracula_boasts + dracula_threats + dracula_non_sequiturs
    random.shuffle(line_pool)

    for _ in range(num_lines - 2):
        if line_pool:
            lines.append(line_pool.pop())
    
    lines.append(random.choice(dracula_closers))
    
    # Join the lines with a slight delay to simulate thought
    monologue = ""
    for line in lines:
        monologue += line + "\n"
    
    await ctx.send(monologue)


# --- Run the Bot ---
# Replace 'YOUR_BOT_TOKEN_HERE' with your bot token
bot.run(os.environ['DISCORD_TOKEN'])

