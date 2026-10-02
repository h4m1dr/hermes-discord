# Hermes Discord Bot on Render

A custom runner for Hermes Agent on Discord, using a lightweight HTTP keep-alive server to prevent Render from throwing port detection timeouts.

## Features
- Runs Hermes Agent gateway for Discord.
- Includes a lightweight HTTP keep-alive server (`server.py`) to satisfy Render's port binding requirements (`PORT 10000`).
- Supports automatic sleep and wake-up via incoming HTTP requests or Discord interactions.

## Environment Variables
Make sure to set these in your Render Dashboard:
- `DISCORD_BOT_TOKEN`: Your Discord Bot Token.
- `LLM_API_BASE`: API Base URL (e.g., 9Router or OmniRoute endpoint).
- `LLM_API_KEY`: Your API Key.
