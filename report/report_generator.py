import os
from datetime import datetime

def generate(results):

    os.makedirs("output", exist_ok=True)

    broken = [r for r in results if r["broken"]]

    html = f"""
    <html>
    <head>
        <title>LinkSentry Report</title>
    </head>
    <body style="background:#0f172a;color:white;font-family:Arial">

    <h1>🔴 Broken URLs Report</h1>
    <p>Generated: {datetime.now()}</p>

    <h2>Total Broken: {len(broken)}</h2>

    <table border="1" style="width:100%">
        <tr>
            <th>URL</th>
            <th>Status</th>
            <th>AI Suggestion</th>
        </tr>
    """

    for r in broken:
        html += f"""
        <tr>
            <td>{r['url']}</td>
            <td>{r['status']}</td>
            <td>{r.get('fix')}</td>
        </tr>
        """

    html += "</table></body></html>"

    with open("output/report.html", "w", encoding="utf-8") as f:
        f.write(html)
