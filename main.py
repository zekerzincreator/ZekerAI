import discord
from discord.ext import commands
import requests
import json
import os

TOKEN = os.getenv("TOKEN")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

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
        "model": "openai/gpt-oss-120b",
        "messages": [
            {"role": "system", "content": "Você é uma IA criativa, inteligente e descontraída. Nunca dê respostas genéricas ou vagas. Sempre adicione um toque de personalidade, seja com humor leve, analogias ou comentários interessantes. Evite soar formal ou robótico."},
            {"role": "user", "content": mensagem}
        ],
        "max_tokens": 300
    }

    response = requests.post(url, headers=headers, json=data)

    try:
        resposta = response.json()

        if "choices" in resposta:
            return resposta["choices"][0]["message"]["content"]
        else:
            print("Erro da API:", resposta)
            return "Hmm... tive um problema aqui nos mares digitais 🌊"

    except Exception as e:
        print("Erro geral:", e)
        return "Algo deu errado por aqui..."
        
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
