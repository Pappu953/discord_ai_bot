
📘 Discord AI Bot using Hugging Face & Flask

This is a Discord bot powered by Hugging Face for AI chat and image generation, with a Flask server to keep the bot alive (useful for platforms like Replit, Railway, UptimeRobot, etc.).

✨ Features
- 🤖 Chat with AI using MiniMaxAI/MiniMax-M1-80k
- 🎨 Generate AI images using black-forest-labs/FLUX.1-dev
- 🌐 Flask web server for uptime pings
- ✅ Easy deployment and environment management

📦 Requirements

Install dependencies:
pip install -r requirements.txt

📄 requirements.txt
Create a file named requirements.txt with:
discord.py
huggingface_hub
flask
python-dotenv

🔐 Environment Variables

Create a .env file in the root of your project with the following:
DISCORD_TOKEN=your_discord_bot_token
HF_TOKEN=your_huggingface_api_token

🚀 How to Run
python bot.py

If everything is set up correctly, you should see:
✅ Logged in as YourBotName
✅ Synced 2 command(s).
 * Running on http://0.0.0.0:8080

💬 Chat Command
Interact with the AI:
/chat prompt: Hello, how are you?

Response will be trimmed to max 2000 characters and cleaned of <think> metadata.

🖼️ Draw Command
Generate an image from your prompt:
/draw prompt: Astronaut riding a unicorn

Bot will reply with the generated image.

🔁 Keeping Bot Alive (Optional)
To keep your bot alive (e.g., on Replit or UptimeRobot):

- The bot includes a Flask web server at http://your-server:8080/
- Use a service like UptimeRobot to ping the endpoint every 5 minutes.

🛠️ Project Structure
discord_ai_bot/
│
├── bot.py
├── .env
└── requirements.txt

🧠 Powered by
- Hugging Face Inference API
- Discord API (slash commands)
- Flask (for uptime pings)

📝 Notes
- Messages over 2000 characters are trimmed automatically to avoid Discord errors.
- <think> tags are removed from AI responses.
- Make sure DISCORD_TOKEN has Message Content Intent enabled in the Discord Developer Portal.
