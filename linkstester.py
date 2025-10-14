import json
import aiohttp
import asyncio

async def check_link(session, url):
    try:
        async with session.head(url, timeout=5) as response:
            return url, response.status == 200
    except:
        return url, False

async def main():
    with open('conteudo.json', 'r', encoding='utf-8') as f:
        data = json.load(f)

    urls = []
    for categoria, grupos in data.items():
        if isinstance(grupos, dict):
            for grupo_nome, lista in grupos.items():
                urls.extend(lista)

    offline = []
    async with aiohttp.ClientSession() as session:
        tasks = [check_link(session, url) for url in urls]
        for url, ok in await asyncio.gather(*tasks):
            if not ok:
                print(f"❌ {url}")
                offline.append(url)
            else:
                print(f"✅ {url}")

    print(f"\nTotal offline: {len(offline)}")

asyncio.run(main())
