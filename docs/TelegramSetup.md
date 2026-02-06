# Telegram Channel Setup

Follow these steps to connect PulseBot to Telegram.

## Prerequisites

- PulseBot installed and configured
- Timeplus running
- A Telegram account

## Step 1: Create a Telegram Bot

1. Open Telegram and search for **@BotFather**
2. Start a chat and send `/newbot`
3. Follow the prompts:
   - Enter a **name** for your bot (e.g., "My PulseBot")
   - Enter a **username** for your bot (must end in `bot`, e.g., "my_pulsebot")
4. BotFather will give you a **bot token** like:
   ```
   123456789:ABCdefGHIjklMNOpqrsTUVwxyz
   ```
5. Save this token securely - you'll need it in Step 3

## Step 2: Get Your Telegram User ID (Optional)

If you want to restrict the bot to specific users only:

1. Search for **@userinfobot** on Telegram
2. Start a chat and it will show your user ID (a number like `123456789`)
3. Note down the user IDs of all allowed users

> **Note**: Skip this step if you want the bot to respond to everyone.

## Step 3: Configure PulseBot

### Set the Environment Variable

```bash
export TELEGRAM_BOT_TOKEN="your_bot_token_here"
```

Or add it to your `.env` file:
```
TELEGRAM_BOT_TOKEN=your_bot_token_here
```

### Update config.yaml

```yaml
channels:
  telegram:
    enabled: true
    token: "${TELEGRAM_BOT_TOKEN}"
    allow_from: []  # Empty = allow all users
```

To restrict to specific users, add their Telegram user IDs (as integers):
```yaml
channels:
  telegram:
    enabled: true
    token: "${TELEGRAM_BOT_TOKEN}"
    allow_from:
      - 123456789
      - 987654321
```

## Step 4: Start PulseBot

Start the agent to begin processing messages:

```bash
pulsebot run
```

The agent will automatically:
- Connect to Telegram using your bot token
- Listen for incoming messages
- Process them through the AI agent
- Send responses back to users

## Step 5: Test Your Bot

1. Open Telegram and search for your bot by its username
2. Click **Start** or send `/start`
3. Send a message like "Hello, what can you do?"
4. Wait for the response from PulseBot

### Available Commands

| Command | Description |
|---------|-------------|
| `/start` | Start the bot and see welcome message |
| `/help` | Show help information |

## Troubleshooting

| Issue | Possible Cause | Solution |
|-------|----------------|----------|
| Bot not responding | Agent not running | Ensure `pulsebot run` is running |
| "Not authorized" message | User ID not in allow list | Add your user ID to `allow_from` in config |
| Token invalid error | Incorrect token | Check the token is correct with no extra spaces |
| No response from agent | Timeplus not running | Ensure Timeplus/Proton is running |
| Connection timeout | Network issues | Check your internet connection |

### Check Logs

View agent logs for debugging:

```bash
pulsebot run --log-level DEBUG
```

### Verify Streams

Ensure the messages stream exists:

```bash
pulsebot setup
```

## Security Recommendations

1. **Restrict Users**: Always set `allow_from` in production to prevent unauthorized access
2. **Protect Token**: Never commit your bot token to version control
3. **Use Environment Variables**: Store sensitive values in environment variables, not directly in config files

## Architecture

When using Telegram:

```
Telegram User
     │
     ▼
Telegram Bot API
     │
     ▼
TelegramChannel (PulseBot)
     │
     ▼ writes user_input
messages stream (Timeplus)
     │
     ▼ reads user_input
Agent Core
     │
     ▼ writes agent_response
messages stream (Timeplus)
     │
     ▼ reads agent_response
TelegramChannel (PulseBot)
     │
     ▼
Telegram Bot API
     │
     ▼
Telegram User
```
