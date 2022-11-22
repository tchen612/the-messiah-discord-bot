import os
import discord
import random
from dotenv import load_dotenv
from discord.ext import commands

load_dotenv()

BOT_ID = int(os.getenv('BOT_ID'))
GUILD_ID = int(os.getenv('GUILD_ID'))
LOBBY_CHANNEL_ID = int(os.getenv('LOBBY_CHANNEL_ID'))
ROLE_MESSAGE_ID = int(os.getenv('ROLE_MESSAGE_ID'))
TOKEN = os.getenv('DISCORD_TOKEN')

VOLLEYBALL_SCHEDULE_URL = 'https://sites.google.com/site/oakleighvolleyball/home/fixture/friday-fixture?fbclid=IwAR0BInng4HxL_icPexoHYxDkT5HfiYjttv8b5qteKJs4Filn_ECrvcvxzwc'

class discord_bot(discord.Client):
    def __init__(self):
        super().__init__(intents = discord.Intents.all())
        self.synced = False

    async def on_ready(self):
        await self.wait_until_ready()
        # this will check if commands are synced to guild, if not, sync commands to guild
        if not self.synced:
            await tree.sync(guild = discord.Object(id = GUILD_ID))
            self.synced = True
        print("Bot is online")

bot = discord_bot()
tree = discord.app_commands.CommandTree(bot)

@bot.event
async def on_member_join(member):
    channel = bot.get_channel(LOBBY_CHANNEL_ID)
    await channel.send(f"Hey {member.mention}, welcome to **{member.guild}** 🎉🤗 ! If you want to stay, you gotta be willing to work dat booty for it ;)")

@bot.event
async def on_member_remove(member):
    channel = bot.get_channel(LOBBY_CHANNEL_ID)
    await channel.send(f"{member.mention} just left the server. Good fucking riddance! Hated that cunt anyway~~")

@bot.event
async def on_raw_reaction_add(payload):
    if payload.message_id == ROLE_MESSAGE_ID:
        # iterate through all the bot's guilds to find the correct one
        guild = discord.utils.find(lambda guild: guild.id == payload.guild_id, bot.guilds)
        
        if payload.emoji.name == 'lol':
            role = discord.utils.get(guild.roles, name='league of legends')
        elif payload.emoji.name == 'csgo':
            role = discord.utils.get(guild.roles, name='csgo')
        elif payload.emoji.name == 'terraria':
            role = discord.utils.get(guild.roles, name='terraria')
        elif payload.emoji.name == 'minecraft':
            role = discord.utils.get(guild.roles, name='minecraft')
        else:
            role = None

        if role is not None:
            # iterate through all the members in the guild to find the correct one to assign role to
            member = discord.utils.find(lambda member: member.id == payload.user_id, guild.members)
            if member is not None:
                await member.add_roles(role)
        
@bot.event
async def on_raw_reaction_remove(payload):
    if payload.message_id == ROLE_MESSAGE_ID:
        # iterate through all the bot's guilds to find the correct one
        guild = discord.utils.find(lambda guild: guild.id == payload.guild_id, bot.guilds)
        
        if payload.emoji.name == 'lol':
            role = discord.utils.get(guild.roles, name='league of legends')
        elif payload.emoji.name == 'csgo':
            role = discord.utils.get(guild.roles, name='csgo')
        elif payload.emoji.name == 'terraria':
            role = discord.utils.get(guild.roles, name='terraria')
        elif payload.emoji.name == 'minecraft':
            role = discord.utils.get(guild.roles, name='minecraft')
        elif payload.emoji.name == 'pokemon':
            role = discord.utils.get(guild.roles, name='Pokémon')
        else:
            role = None

        if role is not None:
            # iterate through all the members in the guild to find the correct one to assign role to
            member = discord.utils.find(lambda member: member.id == payload.user_id, guild.members)
            if member is not None:
                await member.remove_roles(role)

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    
    messages = ['Thanks Mr. Bot', 'Thanks @The Messiah', 'thanks @The Messiah', 'ty @The Messiah', 'TY @The Messiah', 'Ty @The Messiah', 'Thanks Jesus']
    thank_list = ['Thanks', 'thanks', 'Thank', 'thank', 'TY', 'ty', 'Ty']
    for keyword in thank_list:
        if keyword in message.content and f'<@{BOT_ID}>' in message.content:
            await message.channel.send('You are welcome my child', reference=message)
            break

    if message.content == 'Amen':
        await message.channel.send('Amen', reference=message)

@tree.command(name = "help", description = "Shows help for the bot", guild = discord.Object(id = GUILD_ID))
async def self(interaction: discord.Interaction):
    em = discord.Embed(title = "The Messiah User Guide", description = 'Find the source code here: https://github.com/tchen612/the-messiah-discord-bot')
    
    em.add_field(name = "Commands", value = "/help\n/stoic-chad\n/volleyball")

    await interaction.response.send_message(embed = em)

@tree.command(name = "volleyball", description = "Links the volleyball schedule", guild = discord.Object(id = GUILD_ID))
async def self(interaction: discord.Interaction):
    await interaction.response.send_message(VOLLEYBALL_SCHEDULE_URL)

@tree.command(name = "stoic-chad", description = "Shows a random stoic quote", guild = discord.Object(id = GUILD_ID))
async def self(interaction: discord.Interaction):
    # generate a random line number to read a quote off of
    rand = random.randint(0, 402)
    rand = (rand // 4) * 4
    line_number = rand

    file= open('stoic-quotes.txt', 'r')
    lines = file.readlines()[line_number:line_number+3]

    await interaction.response.send_message(''.join(lines))

@tree.command(name = "colour", description = "Asks you what your favourite colour is", guild = discord.Object(id = GUILD_ID))
async def self(interaction: discord.Interaction):
    # generate a random line number to read a quote off of
    line_number = random.randint(1, 69)

    file= open('what-is-your-favourite-colour.txt', 'r')
    lines = file.readlines()[line_number]

    await interaction.response.send_message(''.join(lines))

bot.run(TOKEN)