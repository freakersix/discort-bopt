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
bot = commands.Bot(command_prefix='!?', intents=intents, help_command=None)

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
    "We straight gassin', cuttin' straight to the bricks!", "Listen...", "Blah!", 
    "I got that dog in me, but something's fucking wrong with it, I think it's got parvo", "I smoke the shit that comes out of Northern Bharat."
]
dracula_boasts = [
    "my Audemars Piguet is worth the GDP of Yemen.", "I'm back to back with God, shaking the fucking universe.",
    "I was flippin' bricks for Mansa Musa before y'all even became a type-1 civilization!",
    "I'm him! I've been him! I will continue to be him!",
    "I walked across the sand dunes of the Sahara Desert for 40 days and 40 nights with nothing but a pack of Newports and a fifth of Henny.",
    "my cock is sanded down smooth!", "I'm 12 million years old!", "I got strands of RNA in my hookah! Every puff is an insult to God!", 
    "I invented bitcoin and then forgot my password. I don't give a fuck. I just scream into the payphone and money comes out.",
    "Pure crystal. Straight up icing my noggin before we get down to fuckin'. I blow harder than an eskimo in seal gut."
]
dracula_threats = [
    "I threw the opp in the particle collider; watched his ass get pulled apart into a million pieces, turned his sorry ass into some high-quality data!",
    "the last guy who ran off on the pack got choked out by some Givenchy gloves; the last thing he ever saw was the price tag on them.",
    "I psychologically terrorized the opp until he k!lled himself at the Michael Jordan Steakhouse!",
    "reach for my neck, you'll get turned into an example!",
    "this weed will have you in purgatory, screaming like some type of sebacious ghoul for eternity!",
    "I put him on a T-shirt and turned him into a real fashion icon!",
    "Do you see my Smith & Wesson? Fuck no, I already capped you.",
    "I pulled up and asked for the opp's coordinates, they said this was a Jamba Juice.",
    "I made it to the edge of the omniverse, didn't like what I saw, so I made haste back to the manor and pacified myself with some Norwegian milkers."
]
dracula_non_sequiturs = [
    "I was at the Battle of Jericho, taunting both sides with my balls out.",
    "I'm gulping sea monkeys by the gallon, my tummy feel crazy!",
    "If Santa come down my chimney, I'mma have to lay pipe!",
    "I can't tell if I want to kill my opps or fuck 'em!",
    "I'm trying to explain to the cop that we’re all just atoms,,, so he might as well let me go!",
    "I chill with the Apaches while they recite unwritten hymns and share a pipe packed with some shit I ain't ever witnessed.",
    "I graft my own skin off and suck on it like an Amazonian tree frog just to feel something.",
    "I touched the untouchables just to fuck with'em."
]
dracula_closers = [
    "This shit ain't nothing to me, man!", "I really do this shit!", "Sounds like her problem to me, ha ha!",
    "I'm a real glutton! AH!", "There are consequences to your crimes against the natural order, prepare thyself, THOT!",
    "This shit's got me roaring like Aslan when he's schooling the white bitch.",
    "Somebody get me a benzo, the boogeyman's trying to fuck with me and he doesn't know that I'm strapped.",
    "Opps wanted some initiative, froze his whole board. I'll kill you, you stupid peice of shit."
]

# --- Freaker Speech Components (Based on the REALEST freaker) ---
freaker_openers = [
    "you're worried about {topic}?",
    "so your whole deal is '{quote}'?",
    "you really just said '{quote}'?",
    "hold up, you think {topic} is the problem?",
    "woah, woah, woah. did you just say '{quote}'?"
]

freaker_twists = [
    "worry about that dawg in you first, playa.",
    "uh-oh, guys, we got a real crybaby mcpisserton over here.",
    "that sounds like a real bad case of freakadeliosis to me.",
    "that's some real gancer (gay cancer) type shyt, sorry ganglius.",
    "poo-poo, pee-pee.",
    "and suddenly, it's bad again..."
]

freaker_closers = [
    "lock the fuck in.",
    "rise n grind, gaymers.",
    "freaker mode: activated.",
    "go shit your pants.",
    "let's fucking goooooooo!",
    "are you even trying to lock tf in right now?"
]

# --- Bot Events ---
@bot.event
async def on_ready():
    print(f'Bot is logged in as {bot.user.name}')
    print('------')
# --- Commands ---
@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    # Check for commands first and stop if it is one
    if message.content.startswith(bot.command_prefix):
        await bot.process_commands(message)
        return

    data = load_data()
    for phrase in data['learned_phrases']:
        if phrase.lower() in message.content.lower():
            await asyncio.sleep(random.uniform(0.5, 1.5))

            # --- NEW FREAKER LOGIC ---
            user_quote = message.content
            triggered_topic = phrase

            opener_template = random.choice(freaker_openers)
            twist = random.choice(freaker_twists)
            closer = random.choice(freaker_closers)

            opener = opener_template.format(quote=user_quote, topic=triggered_topic)

            final_response = f"{opener} {twist}. {closer}."

            await message.channel.send(final_response)

            # --- END OF LOGIC ---
            return # Exit after responding

# --- Commands ---
@bot.command(name='help', aliases=['list'])
async def help_command(ctx):
    """Displays this help message with all commands."""
    embed = discord.Embed(
        title="Command List for discort-bopt",
        description="Here are all the available commands. This list updates automatically!",
        color=discord.Color.from_rgb(139, 0, 255) # A nice purple/violet color
    )
    
    # Loop through all registered commands
    for command in bot.commands:
        # Don't list the help command itself in the list
        if command.name == 'help':
            continue
        
        # Use the command's docstring as its description
        # The text in """triple quotes""" below a command's definition
        help_text = command.help if command.help else "No description provided."
        embed.add_field(name=f"{bot.command_prefix}{command.name}", value=help_text, inline=False)
        
    await ctx.send(embed=embed)

@bot.command()
async def truthseeker(ctx):
    """Tells a random truth from memory."""
    data = load_data()
    if data['truthseeker']:
        await ctx.send(random.choice(data['truthseeker']))
    else:
        await ctx.send("The hivemind knows no truths. The master must edit the database.")

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
@bot.command()
async def lockin(ctx):
    """Announces that the user is locked in."""
    await ctx.message.delete() # Deletes the "!lockin" message
    
    # We can pull from your existing freaker lists for variety!
    announcement = random.choice([
        "is now locked the fuck in.",
        "has activated freaker mode.",
        "is on that evil grind-set",
        "is freaking the freak out"
    ])
    
    # @ctx.author.mention will automatically tag you
    final_message = f"**Heard. {ctx.author.mention} {announcement}**"
    
    await ctx.send(final_message)
@bot.command()
async def lockout(ctx):
    """Announces that the user is locked out."""
    await ctx.message.delete() # Deletes the "!lockout" message
    
    # A new list of phrases for logging off
    announcement = random.choice([
        "is no longer locked in. The simulation can return to its regularly scheduled programming.",
        "has been released from the mainframe. Freakadeliosis levels are returning to normal.",
        "is tapping out. The gaymers can now rest.",
        "has logged off. Go shit your pants."
    ])
    
    # @ctx.author.mention will automatically tag you
    final_message = f"**Understood. {ctx.author.mention} {announcement}**"
    
    await ctx.send(final_message)

# --- Run the Bot ---
# Replace 'YOUR_BOT_TOKEN_HERE' with your bot token
bot.run(os.environ['DISCORD_TOKEN'])

