import os
import re
import threading
import discord
from discord.ext import commands
from discord import app_commands
from dotenv import load_dotenv
from huggingface_hub import InferenceClient
from flask import Flask
from io import BytesIO
from PIL import Image

# Load environment variables
load_dotenv()
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
HF_TOKEN = os.getenv("HF_TOKEN")

# Hugging Face clients
chat_client = InferenceClient(provider="fireworks-ai", api_key=HF_TOKEN)
image_client = InferenceClient(provider="nebius", api_key=HF_TOKEN)

# Discord bot setup
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)
tree = bot.tree

# Autocomplete suggestions
style_suggestions = [
    "anime", "cyberpunk", "realistic", "pixel art", "steampunk",
    "sci-fi", "fantasy", "vaporwave", "low poly", "concept art"
]

async def autocomplete_prompt(interaction: discord.Interaction, current: str):
    return [
        app_commands.Choice(name=style, value=style)
        for style in style_suggestions if current.lower() in style.lower()
    ][:5]

@bot.event
async def on_ready():
    try:
        synced = await tree.sync()
        print(f"✅ Synced {len(synced)} slash commands globally.")
    except Exception as e:
        print(f"❌ Failed to sync commands: {e}")
    print(f"🤖 {bot.user} is now online!")

@tree.command(name="chat", description="Talk to the AI chatbot")
@app_commands.describe(prompt="Your message to the AI")
async def chat_command(interaction: discord.Interaction, prompt: str):
    await interaction.response.defer(thinking=True)
    try:
        completion = chat_client.chat.completions.create(
            model="deepseek-ai/DeepSeek-R1-0528",
            messages=[{"role": "user", "content": prompt}]
        )
        raw_reply = completion.choices[0].message["content"]
        cleaned_reply = re.sub(r"<think>.*?</think>", "", raw_reply, flags=re.DOTALL).strip()
        await interaction.followup.send(cleaned_reply or "🤖 (No response)")
    except Exception as e:
        await interaction.followup.send(f"❌ Error: {str(e)}")

@tree.command(name="draw", description="Generate an AI image from a prompt")
@app_commands.describe(prompt="Describe the image you want")
@app_commands.autocomplete(prompt=autocomplete_prompt)
async def draw_command(interaction: discord.Interaction, prompt: str):
    await interaction.response.defer(thinking=True)
    try:
        image = image_client.text_to_image(prompt, model="black-forest-labs/FLUX.1-dev")
        image_bytes = BytesIO()
        image.save(image_bytes, format="PNG")
        image_bytes.seek(0)
        await interaction.followup.send(file=discord.File(fp=image_bytes, filename="generated.png"))
    except Exception as e:
        await interaction.followup.send(f"❌ Error: {str(e)}")

# Flask web app for Render's port binding
app = Flask(__name__)

@app.route("/")
def home():
    return "🤖 Discord AI Bot is running!"

def run_flask():
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)

# Run Flask and Bot concurrently
if __name__ == "__main__":
    threading.Thread(target=run_flask).start()
    bot.run(DISCORD_TOKEN)
