import requests
from bs4 import BeautifulSoup
from pathlib import Path

START_YEAR = 2012
END_YEAR = 2026

results = []

headers = {
    "User-Agent": "Mozilla/5.0"
}

print("Building archive...")

for year in range(END_YEAR, START_YEAR - 1, -1):

    url = f"https://www.irishlottery.com/daily-million-archive-{year}"

    print(f"Fetching {year}")

    try:

        response = requests.get(
            url,
            headers=headers,
            timeout=15
        )

        soup = BeautifulSoup(response.text, "html.parser")

        tables = soup.find_all("table")

        for table in tables:

            rows = table.find_all("tr")

            for row in rows:

                cols = row.find_all("td")

                if len(cols) < 2:
                    continue

                date_text = cols[0].get_text(" ", strip=True)

                draw_text = cols[1].get_text(" ", strip=True)

                numbers = []

                for item in draw_text.replace(",", " ").split():

                    cleaned = item.strip()

                    if cleaned.isdigit():

                        numbers.append(cleaned)

                if len(numbers) < 7:
                    continue

                main = " ".join(numbers[:6])

                bonus = numbers[6]

                line = f"{date_text}: {main} ({bonus})"

                results.append(line)

    except Exception as e:

        print(f"Failed {year}: {e}")

results = list(dict.fromkeys(results))

html_output = "\n".join(
    f'<div class="draw">{r}</div>'
    for r in results
)

html = f"""
<!DOCTYPE html>
<html>
<head>

<meta charset="utf-8">

<title>Irish Daily Million Results Archive</title>

<style>

body {{
    background:#000;
    color:#00ff66;
    font-family:Consolas, monospace;
    padding:20px;
    line-height:1.5;
}}

h1 {{
    color:#ffcc66;
}}

.draw {{
    padding:2px 0;
    border-bottom:1px solid #111;
}}

.draw:hover {{
    background:#111;
}}

</style>

</head>

<body>

<h1>Irish Daily Million Results Archive (2012–2026)</h1>

{html_output}

</body>
</html>
"""

Path("index.html").write_text(
    html,
    encoding="utf-8"
)

Path("irish_daily_million_archive.txt").write_text(
    "\n".join(results),
    encoding="utf-8"
)

print(f"Generated {len(results)} results.")
