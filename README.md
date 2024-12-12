# wumlla

Use Discord chat threads as the UI for your local LLM inference server (or actually any OpenAI-compatible API server; local or not).

This is basically for those who live in Discord, and for those who don't want to spin up another UI for interacting with LLMs.

## Get started

### 1. Create and install a Discord Bot

Follow the instructions of creating and installing a Bot to your server: [Creating a Bot Account | discord.py Docs](https://discordpy.readthedocs.io/en/stable/discord.html)

Important Bot Permissions are: `Send Messages`, `Send Messages in Threads`, `Read Message History`

Also, keep note of your Bot token for later.

### 2. Create a specific Text Channel

Create a channel named `local-llm-wmll` (case sensitive). The bot will only work inside Threads that are in this channel.

### 3. Pull Docker image (or Clone this repo)

#### 3.1 Pull Docker image and run right away

Quickest way to run is getting the docker image.

`docker pull ghcr.io/neil-vqa/wumlla-server:latest`

Set `DISCORD_BOT_TOKEN`, `INFERENCE_SERVER`, and `BOT_SYSTEM_PROMPT` environment variables when running a container.

#### 3.2 Clone this repo

If you want to extend or configure something, clone this to your local machine or VPS, then follow the next steps.

### 4. Set environment variables

Rename `.env.sample` to `.env`, then provide `DISCORD_BOT_TOKEN`, `INFERENCE_SERVER`, and `BOT_SYSTEM_PROMPT`.

### 5. Build and run (using Docker or pip)

#### Docker

The `instructions.txt` provides copy-pastable commands to build and run the bot server.

#### pip

Usual step of 1) create a virtual environment, 2) install dependencies, 3) run `python serve.py`

## Roadmap

- [ ] Build the system in a way that will allow to have plugins/extensions for the functionality of the LLM bot.

## Demo

Here is a screenshot of Wumlla as a podcaster assistant, working within `local-llm-wmll` channel `docker` thread. I have llama.cpp serve `SmolLM2-1.7B-Instruct-Q6_K` locally.

![demo](/assets/wumlla-ss1.png)

![demo](/assets/wumlla.webp)

*Wumlla the podcaster*