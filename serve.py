import discord
import os
import logging
import aiohttp
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("DISCORD_BOT_TOKEN")
INFERENCE_SERVER = os.getenv("INFERENCE_SERVER")
BOT_SYSTEM_PROMPT = os.getenv(
    "BOT_SYSTEM_PROMPT", "You are Wumlla, a helpful assistant."
)


logger = logging.getLogger(__name__)
logging.basicConfig(format="%(asctime)s - %(levelname)s - %(message)s")

intents = discord.Intents.default()
intents.messages = True
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)


async def call_llm(messages: list):
    payload = {
        "model": "local-llm",
        "messages": messages,
        "temperature": 0.7,
    }

    async with aiohttp.ClientSession() as session:
        async with session.post(
            f"{INFERENCE_SERVER}/v1/chat/completions", json=payload
        ) as response:
            if response.status == 200:
                res_data = await response.json()
                res_msg = res_data["choices"][0]["message"]["content"]
                return res_msg
            else:
                logger.error(f"Request failed with status code: {response.status}")
                logger.error(f"Response Text: {await response.text()}")
                return None


def arrange_msgs_history(messages: list):
    msgs_container = [
        {
            "role": "system",
            "content": BOT_SYSTEM_PROMPT,
        }
    ]

    for msg in messages:
        msgs_container.append(
            {
                "role": "user" if msg.author != bot.user else "assistant",
                "content": msg.content,
            }
        )

    return msgs_container


def chunk_message(message, max_length=2000):
    chunks = []
    while message:
        if len(message) <= max_length:
            chunks.append(message)
            break
        chunks.append(message[:max_length])
        message = message[max_length:]
    return chunks


@bot.event
async def on_ready():
    logger.info(f"Logged in as {bot.user}")


@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    if isinstance(message.channel, discord.Thread):
        if message.channel.parent and message.channel.parent.name == "local-llm-wmll":
            try:
                async with message.channel.typing():
                    messages = []
                    async for msg in message.channel.history(limit=20):
                        messages.append(msg)

                    msgs = arrange_msgs_history(reversed(messages))
                    res = await call_llm(msgs)

                chunks = chunk_message(res)
                for chunk in chunks:
                    await message.channel.send(chunk)
            except Exception as e:
                logger.exception(e)
                await message.channel.send(f"An error occurred: {e}")

    await bot.process_commands(message)


if __name__ == "__main__":
    bot.run(BOT_TOKEN)
