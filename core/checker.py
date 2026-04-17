import aiohttp
import asyncio

async def check(url, session):
    try:
        async with session.get(url, timeout=5) as r:
            return {"url": url, "status": r.status}
    except:
        return {"url": url, "status": "ERROR"}

async def check_urls(urls):
    async with aiohttp.ClientSession() as session:
        tasks = [check(u, session) for u in urls]
        return await asyncio.gather(*tasks)
import aiohttp
import asyncio

async def check(urls):
    results = []

    async with aiohttp.ClientSession() as session:
        for url in urls:
            try:
                async with session.get(url) as r:
                    results.append((url, r.status))
            except:
                results.append((url, "ERROR"))

    return results
