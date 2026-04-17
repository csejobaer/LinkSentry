import aiohttp
import asyncio
import time


# =========================
# ⚡ CHECK SINGLE URL
# =========================
async def check_url(session, url):

    try:
        async with session.get(url, timeout=15, allow_redirects=True) as res:

            return {
                "url": url,
                "status": res.status,
                "final_url": str(res.url),
                "redirects": [str(r.url) for r in res.history]
            }

    except:
        return {
            "url": url,
            "status": "ERROR",
            "final_url": None,
            "redirects": []
        }


# =========================
# 🚀 10K SCANNER ENGINE
# =========================
async def scan_urls(urls, concurrency=300):

    connector = aiohttp.TCPConnector(limit=concurrency, ssl=False)
    timeout = aiohttp.ClientTimeout(total=15)

    start = time.time()

    async with aiohttp.ClientSession(
        connector=connector,
        timeout=timeout
    ) as session:

        sem = asyncio.Semaphore(concurrency)

        async def worker(url):
            async with sem:
                return await check_url(session, url)

        tasks = [worker(u) for u in urls]

        for coro in asyncio.as_completed(tasks):

            result = await coro

            elapsed = time.time() - start + 0.001
            speed = len(tasks) / elapsed

            yield {
                "result": result,
                "speed": round(speed, 2),
                "done": len(tasks),
                "total": len(tasks)
            }
