import discord
from discord.ext import commands
import requests
import json
import os

TOKEN = os.getenv("MTQ4ODE5OTY4OTExNDQ4NDczNg.GIlgYn.a5r6yeRsiqVOVWcS_gvgRtC12GTKJmj3xXQ3Pk")
GROQ_API_KEY = os.getenv("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")

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

# memória simples
try:
    with open("memoria.json", "r") as f:
        memoria = json.load(f)
except:
    memoria = {}

def salvar_memoria():
    with open("memoria.json", "w") as f:
        json.dump(memoria, f)

def perguntar_groq(mensagem):
    url = "https://api.groq.com/openai/v1/chat/completions"

    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }

    data = {
        "model": "mixtral-8x7b-32768",
        "messages": [
            {"role": "system", "content": "Você é uma IA estilo capitão pirata inteligente, engraçado e amigável."},
            {"role": "user", "content": mensagem}
        ]
    }

    response = requests.post(url, headers=headers, json=data)
    resposta = response.json()

    return resposta["choices"][0]["message"]["content"]

@bot.event
async def on_ready():
    print(f"Logado como {bot.user}")

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    user = str(message.author)

    if user not in memoria:
        memoria[user] = []

    memoria[user].append(message.content)
    salvar_memoria()

    if bot.user in message.mentions or message.content.startswith("!"):
        resposta = perguntar_groq(message.content)
        await message.channel.send(resposta)

    await bot.process_commands(message)

bot.run(TOKEN)
