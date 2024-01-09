import asyncio
from discord.ext import commands
import discord
import responses


async def send_message(message, user_message):
    try:
        response = responses.get_response(user_message)
        async with message.channel.typing():
            await asyncio.sleep(0.5)
            await message.channel.send(response, reference=message)
    except Exception as e:
        print(e)


def run_discord_bot():
    global bot
    TOKEN = ''
    intents = discord.Intents.default()
    intents.message_content = True
    client = discord.Client(intents=intents)

    @client.event
    async def on_ready():
        global bot
        print(f'{client.user} is now running!')

    @client.event
    async def on_message(message):
        if client.user in message.mentions:
            if message.author == client.user:
                return
            username = str(message.author)
            user_message = str(message.content)
            channel = str(message.channel)

            print(f'{username} said: "{user_message}" in ({channel})')
            await send_message(message, user_message)

    client.run(TOKEN)
