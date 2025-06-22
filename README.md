🤖 Discord AI Chatbot & Image Generator

A powerful Discord bot powered by Hugging Face models. It supports AI text chatting and image generation via slash commands.

🚀 Features

- 💬 /chat – Ask anything, get AI answers using DeepSeek R1 model
- 🎨 /draw – Generate stunning AI images from text prompts
- 🔍 Autocomplete suggestions in /draw (e.g., "anime", "cyberpunk")
- 🧹 Cleans out <think> and hidden system notes from AI responses
- 🌐 Easy deployment on Render

🧪 Models Used

| Feature     | Model Name                                 | Provider       |
|-------------|---------------------------------------------|----------------|
| Text Chat   | deepseek-ai/DeepSeek-R1-0528               | Fireworks      |
| Image Gen   | black-forest-labs/FLUX.1-dev               | Nebius         |

🛠 Setup Instructions (Local or Render)

1. Clone this repo

    git clone https://github.com/Pappu953/discord_ai_bot.git
    cd discord-ai-bot

2. Install dependencies

    pip install -r requirements.txt

3. Create .env file

    DISCORD_TOKEN=your_discord_bot_token_here
    HF_TOKEN=your_huggingface_read_token_here

4. Run the bot

    python bot.py

🌐 Deploy to Render (FREE)

1. Push this repo to GitHub.
2. Go to https://render.com and click New > Background Worker.
3. Connect your GitHub repo.
4. Use these Render settings:

| Setting           | Value                               |
|-------------------|-------------------------------------|
| Environment       | Python                              |
| Build Command     | pip install -r requirements.txt     |
| Start Command     | python bot.py                       |
| Instance Type     | Starter (Free) or higher            |

5. Go to Environment > Add Environment Variables and set:

    DISCORD_TOKEN=your_discord_bot_token
    HF_TOKEN=your_huggingface_read_token

6. Click Deploy. You're done!

✨ Slash Command Examples

    /chat What is the capital of Japan?
    /draw anime robot with glowing sword
    /draw cyberpunk city at night, pixel art
    /draw fantasy castle under moonlight

📦 Project Files

    .
    ├── bot.py             # Main bot code
    ├── .env               # Hidden env file (add yourself)
    ├── requirements.txt   # Python dependencies
    └── README.md          # You're reading it!

📃 requirements.txt

    discord.py
    python-dotenv
    huggingface_hub
    pillow

Install with:

    pip install -r requirements.txt

📜 License

This project is open-source under the MIT License.

❤️ Credits

- Built using discord.py
- Powered by Hugging Face Inference API
- Hosted on Render

Need help or want to add buttons, dropdowns, or AI memory features? Message the repo maintainer or open an issue!
