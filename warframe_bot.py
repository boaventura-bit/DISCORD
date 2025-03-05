import discord
import requests
import asyncio

TOKEN = "MTM0NjY2MzkxOTg5MjE3Mjg0MQ.G-nm-J.Y0YV9DpfFLAKdeA5ZEOUpSwHBdV0xMV84EiLao"
CHANNEL_ID = 1346641887729156126

intents = discord.Intents.default()
client = discord.Client(intents=intents)

enviadas = set()

async def fetch_warframe_news():
    url = "https://api.warframestat.us/pc/news"
    response = requests.get(url)

    if response.status_code == 200:
        news = response.json()
        channel = client.get_channel(CHANNEL_ID)

        if not news or not channel:
            return
        
        novas_noticias = [n for n in news[:5] if n["link"] not in enviadas]

        for noticia in reversed(novas_noticias):  # Envia na ordem certa
            title = noticia["message"]
            link = noticia["link"]
            image = noticia.get("image", "")

            embed = discord.Embed(title="📰 Nova Atualização do Warframe!", description=title, color=0x00ff00)
            embed.add_field(name="Leia mais:", value=f"[Clique aqui]({link})", inline=False)
            if image:
                embed.set_image(url=image)

            await channel.send(embed=embed)
            enviadas.add(link)

async def check_news_loop():
    await client.wait_until_ready()
    await fetch_warframe_news()  # Envia as 5 últimas ao iniciar

    while not client.is_closed():
        await fetch_warframe_news()
        await asyncio.sleep(180)  # Verifica a cada 3 minutos

@client.event
async def on_ready():
    print(f'✅ Bot conectado como {client.user}')
    client.loop.create_task(check_news_loop())

client.run(TOKEN)
