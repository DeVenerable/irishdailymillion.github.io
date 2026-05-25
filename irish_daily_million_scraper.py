import requests
from bs4 import BeautifulSoup
from pathlib import Path

START_YEAR = 2012
END_YEAR = 2026

all_results = []

for year in range(END_YEAR, START_YEAR - 1, -1):

    url = f"https://www.irishlottery.com/daily-million-archive-{year}"

    print(f"Fetching {url}")

    response = requests.get(url, timeout=30)

    soup = BeautifulSoup(response.text, "html.parser")

    rows = soup.select("table tr")

    for row in rows:

        cols = row.find_all("td")

        if len(cols) != 2:
            continue

        date_text = cols[0].get_text(" ", strip=True)

        numbers = cols[1].find_all("li")

        nums = [n.get_text(strip=True) for n in numbers]

        if len(nums) < 7:
            continue

        main = " ".join(nums[:6])

        bonus = nums[6]

        line = f"{date_text}: {main} Bonus {bonus}"

        all_results.append(line)

html_lines = "\n".join(
    f'<div class="draw">{x}</div>'
    for x in all_results
)

html = f"""
<!DOCTYPE html>
<html>
<head>

<meta charset="utf-8">

<title>Irish Daily Million Results Archive</title>

<style>

body {{
    background: #000;
    color: #00ff66;
    font-family: monospace;
    padding: 20px;
}}

h1 {{
    color: #ffcc66;
}}

.draw {{
    padding: 2px 0;
    border-bottom: 1px solid #222;
    white-space: pre-wrap;
}}

</style>

</head>

<body>

<h1>Irish Daily Million Results Archive (2012–2026)</h1>

{html_lines}

</body>
</html>
"""

Path("index.html").write_text(html, encoding="utf-8")

Path("irish_daily_million_archive.txt").write_text(
    "\n".join(all_results),
    encoding="utf-8"
)

print(f"Generated {len(all_results)} results.")
