import aiohttp
import asyncio
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse

import warnings
from bs4 import XMLParsedAsHTMLWarning

warnings.filterwarnings("ignore", category=XMLParsedAsHTMLWarning)


# =========================
# 🌐 DOMAIN CHECK
# =========================
def same_domain(base, url):
    base_domain = urlparse(base).netloc.replace("www.", "")
    url_domain = urlparse(url).netloc.replace("www.", "")
    return base_domain in url_domain


# =========================
# 🔥 EXTRACT LINKS
# =========================
def extract_links(base_url, html):

    soup = BeautifulSoup(html, "html.parser")
    links = set()

    for tag in soup.find_all(["a", "link", "script", "img"]):

        for attr in ["href", "src"]:
            value = tag.get(attr)
            if value:
                links.add(urljoin(base_url, value))

    return links


# =========================
# 🚀 FINAL SAFE CRAWLER (10K READY)
# =========================
async def crawl_site(start_url, max_pages=10000):

    visited = set()
    queue = asyncio.Queue()

    await queue.put(start_url)

    connector = aiohttp.TCPConnector(limit=50, ssl=False)
    timeout = aiohttp.ClientTimeout(total=10)

    async with aiohttp.ClientSession(
        connector=connector,
        timeout=timeout
    ) as session:

        while len(visited) < max_pages:

            # 🔥 SAFE QUEUE GET (NO HANG)
            try:
                url = await asyncio.wait_for(queue.get(), timeout=5)
            except asyncio.TimeoutError:
                break  # queue empty → exit safely

            if url in visited:
                continue

            visited.add(url)

            try:
                async with session.get(url, allow_redirects=True) as res:

                    html = await res.text(errors="ignore")

                    yield url   # 🔥 STREAM OUTPUT (IMPORTANT FOR REALTIME CLI)

                    # extract new links
                    for link in extract_links(url, html):

                        clean = link.split("#")[0]

                        if (
                            clean.startswith("http")
                            and same_domain(start_url, clean)
                            and clean not in visited
                        ):
                            await queue.put(clean)

            except:
                continue
