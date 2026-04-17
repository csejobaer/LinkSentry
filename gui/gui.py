import tkinter as tk
import asyncio
from crawler.crawler import crawl_site
from core.checker import check_urls

def start_gui():
    root = tk.Tk()
    root.title("LinkSentry v4")

    text = tk.Text(root)
    text.pack()

    def run():
        url = entry.get()
        urls = asyncio.run(crawl_site(url))
        results = asyncio.run(check_urls(urls))

        for r in results:
            text.insert(tk.END, str(r)+"\n")

    entry = tk.Entry(root)
    entry.pack()

    btn = tk.Button(root, text="Scan", command=run)
    btn.pack()

    root.mainloop()
