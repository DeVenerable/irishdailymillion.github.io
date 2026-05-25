
import requests
from bs4 import BeautifulSoup
from pathlib import Path

START_YEAR = 2012
END_YEAR = 2026

output_txt = Path("irish_daily_million_archive.txt")
output_html = Path("irish_daily_million_archive.html")

lines = []
html_rows = []

for year in range(END_YEAR, START_YEAR - 1, -1):
    url = f"https://irish.national-lottery.com/daily-million/results-archive-{year}"
    print(f"Fetching {url}")

    r = requests.get(url, timeout=30)
    r.raise_for_status()

    soup = BeautifulSoup(r.text, "html.parser")

    draws = soup.select(".archive-item, .results, table tr")

    for draw in draws:
        text = " ".join(draw.get_text(" ", strip=True).split())

        if len(text) < 20:
            continue

        lines.append(text)
        html_rows.append(f"<tr><td>{text}</td></tr>")

output_txt.write_text("\n".join(lines), encoding="utf-8")

html = f"""
<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8">
  <title>Irish Daily Million Archive</title>
  <style>
    body {{
      font-family: monospace;
      background: #111;
      color: #0f0;
      padding: 20px;
    }}
    table {{
      border-collapse: collapse;
      width: 100%;
    }}
    td {{
      padding: 4px 8px;
      border-bottom: 1px solid #333;
      white-space: pre;
    }}
  </style>
</head>
<body>
  <h1>Irish Daily Million Results Archive (2012–2026)</h1>
  <table>
    {''.join(html_rows)}
  </table>
</body>
</html>
"""

output_html.write_text(html, encoding="utf-8")

print("Done.")
