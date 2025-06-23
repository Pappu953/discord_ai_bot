import os
import discord
from discord import app_commands
from discord.ext import commands
from huggingface_hub import InferenceClient
from dotenv import load_dotenv
import asyncio
import re
from flask import Flask
from threading import Thread

app = Flask(__name__)

@app.route('/')
def home():
    return "Bot is running!"

def run_flask():
    app.run(host="0.0.0.0", port=8080)

# Start the Flask server in a separate thread
Thread(target=run_flask).start()

# Load environment variables
load_dotenv()
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
HF_TOKEN = os.getenv("HF_TOKEN")

if not DISCORD_TOKEN or not HF_TOKEN:
    raise EnvironmentError("DISCORD_TOKEN or HF_TOKEN not set in environment variables.")

# Hugging Face Client
hf_client = InferenceClient(token=HF_TOKEN)

# Discord bot setup
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)
tree = bot.tree

@bot.event
async def on_ready():
    print(f"✅ Logged in as {bot.user}")
    try:
        synced = await tree.sync()
        print(f"✅ Synced {len(synced)} command(s).")
    except Exception as e:
        print(f"❌ Sync failed: {e}")

@tree.command(name="chat", description="Talk with AI using Hugging Face chat model.")
@app_commands.describe(prompt="What do you want to say?")
async def chat_command(interaction: discord.Interaction, prompt: str):
    await interaction.response.defer()
    try:
        result = hf_client.chat_completion(
            model="MiniMaxAI/MiniMax-M1-80k",
            messages=[{"role": "user", "content": prompt}]
        )
        message = result.choices[0].message["content"]

        # Remove <think>...</think> blocks
        cleaned_message = re.sub(r"<think>.*?</think>", "", message, flags=re.DOTALL).strip()

        if len(cleaned_message) > 2000:
            cleaned_message = cleaned_message[:1997] + "..."

        await interaction.followup.send(cleaned_message)

    except Exception as e:
        await interaction.followup.send(f"❌ Error generating chat: {e}")

@tree.command(name="draw", description="Generate image from prompt using HF")
@app_commands.describe(prompt="Describe the image you want to generate")
async def draw_command(interaction: discord.Interaction, prompt: str):
    await interaction.response.defer()
    try:
        def generate_image():
            return hf_client.text_to_image(
                prompt,
                model="black-forest-labs/FLUX.1-dev"
            )

        image = await asyncio.to_thread(generate_image)
        path = "output.png"
        image.save(path)

        with open(path, "rb") as f:
            await interaction.followup.send(file=discord.File(f))

        os.remove(path)

    except Exception as e:
        await interaction.followup.send(f"❌ Error generating image: {e}")

bot.run(DISCORD_TOKEN)
