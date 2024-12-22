# Discord Bot - GPT Integration

A Discord bot built with `discord.js` to interact with GPT. The bot listens to commands prefixed with `!gpt` and responds intelligently.

---

## Features
- Responds to `!gpt` commands.
- Simple setup and configuration.
- Includes tests using `jest`.

---

## Installation
1. Clone the repository.
   ```bash
   git clone <repository_url>
   cd discord-bot-gpt
   ```

2. Install dependencies.
   ```bash
   npm install
   ```

---

## Configuration
1. Open the `config/config.json` file.
2. Replace `YOUR_BOT_TOKEN` with your actual Discord bot token.

```json
{
  "token": "YOUR_BOT_TOKEN"
}
```

---

## Running the Bot
1. Start the bot.
   ```bash
   npm start
   ```

The bot will log in and begin listening for `!gpt` commands in Discord channels where it has access.

---

## Testing
1. Run tests to ensure functionality.
   ```bash
   npm test
   ```

The tests cover:
- Bot login functionality.
- Command handling for `!gpt`.

---

## Notes
- Make sure the bot has the necessary permissions in the Discord server.
- Keep your token private to prevent unauthorized access.

---

## License
MIT