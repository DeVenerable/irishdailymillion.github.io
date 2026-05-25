import requests
from bs4 import BeautifulSoup
from pathlib import Path

START_YEAR = 2012
END_YEAR = 2026

results = []

for year in range(END_YEAR, START_YEAR - 1, -1):

    url = f"https://irish.national-lottery.com/daily-million/results-archive-{year}"

    print(f"Loading {year}...")

    html = requests.get(url).text

    soup = BeautifulSoup(html, "html.parser")

    days = soup.find_all("div", class_="archive-item")

    for day in days:

        text = day.get_text("\n", strip=True)

        lines = [x.strip() for x in text.split("\n") if x.strip()]

        if len(lines) < 3:
            continue

        date = lines[0]

        nums = []

        for line in lines[1:]:

            if "Bonus" in line or any(ch.isdigit() for ch in line):
                nums.append(line)

        output = f"{date}: " + " | ".join(nums)

        results.append(output)

html_output = f"""
<!DOCTYPE html>
<html>
<head>

<meta charset="utf-8">

<title>Irish Daily Million Archive</title>

<style>

body {{
    background:#000;
    color:#00ff66;
    font-family:Courier New, monospace;
    padding:20px;
}}

h1 {{
    color:#ffcc66;
}}

.draw {{
    padding:4px 0;
    border-bottom:1px solid #222;
}}

</style>

</head>

<body>

<h1>Irish Daily Million Results Archive (2012–2026)</h1>

{''.join(f'<div class="draw">{r}</div>' for r in results)}

</body>
</html>
"""

Path("index.html").write_text(html_output, encoding="utf-8")

Path("irish_daily_million_archive.txt").write_text(
    "\n".join(results),
    encoding="utf-8"
)

print("Finished.")
