import requests
from bs4 import BeautifulSoup
from pathlib import Path

START_YEAR = 2012
END_YEAR = 2026

output_txt = Path("irish_daily_million_archive.txt")
output_html = Path("index.html")

lines = []

html_parts = []

for year in range(END_YEAR, START_YEAR - 1, -1):

    url = f"https://www.irishlottery.com/daily-million-archive-{year}"

    print(f"Fetching {url}")

    r = requests.get(url, timeout=30)

    soup = BeautifulSoup(r.text, "html.parser")

    draws = soup.select("table.archive-table tbody tr")

    for row in draws:

        cols = [c.get_text(" ", strip=True) for c in row.find_all("td")]

        if len(cols) < 2:
            continue

        line = " | ".join(cols)

        lines.append(line)

        html_parts.append(f'<div class="draw">{line}</div>')

output_txt.write_text("\n".join(lines), encoding="utf-8")

html = f"""
<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<title>Irish Daily Million Results Archive</title>

<style>

body {{
    background: black;
    color: #00ff66;
    font-family: monospace;
    padding: 20px;
}}

h1 {{
    color: #ffcc66;
}}

.draw {{
    padding: 3px 0;
    border-bottom: 1px solid #222;
    white-space: pre-wrap;
}}

</style>

</head>

<body>

<h1>Irish Daily Million Results Archive (2012–2026)</h1>

{''.join(html_parts)}

</body>
</html>
"""

output_html.write_text(html, encoding="utf-8")

print("Archive generated successfully.")
