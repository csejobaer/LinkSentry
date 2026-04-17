from rich.console import Console
from rich.live import Live
from rich.table import Table
from rich.panel import Panel
import asyncio
import time

from core.scanner import scan_urls
from core.url_utils import normalize_url
from crawler.crawler import crawl_site
from report.report_generator import generate
from core.ai_fix import suggest_fix

console = Console()


# =========================
# 🎬 BANNER
# =========================
def show_banner():
    console.print(Panel.fit("""
[bold cyan]
██╗     ██╗███╗   ██╗██╗  ██╗███████╗███████╗███╗   ██╗████████╗██╗   ██╗
██║     ██║████╗  ██║██║ ██╔╝██╔════╝██╔════╝████╗  ██║╚══██╔══╝╚██╗ ██╔╝
██║     ██║██╔██╗ ██║█████╔╝ ███████╗█████╗  ██╔██╗ ██║   ██║    ╚████╔╝ 
██║     ██║██║╚██╗██║██╔═██╗ ╚════██║██╔══╝  ██║╚██╗██║   ██║     ╚██╔╝  
███████╗██║██║ ╚████║██║  ██╗███████║███████╗██║ ╚████║   ██║      ██║   
╚══════╝╚═╝╚═╝  ╚═══╝╚═╝  ╚═╝╚══════╝╚══════╝╚═╝  ╚═══╝   ╚═╝      ╚═╝   

        LinkSentry PRO MODE 🚀
   Real-Time Broken URL + AI Fix + Speed Monitor
[/bold cyan]
""", border_style="cyan"))


# =========================
# 📊 TABLE
# =========================
def create_table(speed=0, total=0, broken=0):

    table = Table(
        title=f"⚡ Speed: {speed} URLs/sec | 🔴 Broken: {broken} | 🌐 Total: {total}"
    )

    table.add_column("URL", style="cyan", overflow="fold")
    table.add_column("STATUS", justify="center")
    table.add_column("RESULT", justify="center")
    table.add_column("AI FIX", style="green", overflow="fold")

    return table


# =========================
# 🔍 HELPERS
# =========================
def is_broken(status):
    return status == "ERROR" or (isinstance(status, int) and status >= 400)


# =========================
# 🚀 MAIN CLI
# =========================
def start_cli():

    show_banner()

    raw_url = console.input("Enter website URL: ")

    url, error = normalize_url(raw_url)

    if error:
        console.print(error)
        return

    console.print("🌐 Crawling website...")

    async def collect():

        urls = []

        async for u in crawl_site(url):
            console.print(u)   # realtime view
            urls.append(u)

        return urls

    urls = asyncio.run(collect())

    console.print(f"✔ Total URLs found: {len(urls)}")

    console.print(f"[green]✔ Total URLs found: {len(urls)}[/green]\n")

    results = []
    broken_count = 0
    start_time = time.time()

    table = create_table()

    # =========================
    # STEP 2: LIVE SCAN ENGINE
    # =========================
    async def run_live(live):

        nonlocal broken_count, table

        async for data in scan_urls(urls):

            r = data["result"]

            url = r["url"]
            status = r["status"]

            speed = data["speed"]
            done = data["done"]

            broken = is_broken(status)

            if broken:
                broken_count += 1

            fix = suggest_fix(url) if broken else "-"

            results.append({
                "url": url,
                "status": status,
                "broken": broken,
                "fix": fix
            })

            table = create_table(speed, done, broken_count)

            table.add_row(
                url[:80],
                str(status),
                "🔴 BROKEN" if broken else "🟢 OK",
                str(fix)
            )

            live.update(table)

    # =========================
    # STEP 3: LIVE DISPLAY LOOP
    # =========================
    with Live(table, refresh_per_second=10, console=console) as live:
        asyncio.run(run_live(live))

    # =========================
    # FINAL REPORT
    # =========================
    console.print(Panel.fit("✅ SCAN COMPLETE", border_style="green"))

    generate(results)

    console.print("[bold blue]📄 Report saved → output/report.html[/bold blue]")
