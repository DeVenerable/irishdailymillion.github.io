import pandas as pd
from pathlib import Path

START_YEAR = 2012
END_YEAR = 2026

results = []

for year in range(END_YEAR, START_YEAR - 1, -1):

    url = f"https://www.irishlottery.com/daily-million-archive-{year}"

    print(f"Reading {url}")

    try:

        tables = pd.read_html(url)

    except Exception as e:

        print(f"Failed {year}: {e}")

        continue

    for table in tables:

        cols = [str(c).lower() for c in table.columns]

        if not any("date" in c for c in cols):
            continue

        for _, row in table.iterrows():

            line = " | ".join(str(x) for x in row.tolist())

            if line.strip():

                results.append(line)

html_results = "\n".join(
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
    background:black;
    color:#00ff66;
    font-family:Courier New, monospace;
    padding:20px;
}}

h1 {{
    color:#ffcc66;
}}

.draw {{
    padding:3px 0;
    border-bottom:1px solid #222;
    white-space:pre-wrap;
}}

</style>

</head>

<body>

<h1>Irish Daily Million Results Archive (2012–2026)</h1>

{html_results}

</body>
</html>
"""

Path("index.html").write_text(html, encoding="utf-8")

Path("irish_daily_million_archive.txt").write_text(
    "\n".join(results),
    encoding="utf-8"
)

print(f"Generated {len(results)} rows.")
