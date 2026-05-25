import pandas as pd
from pathlib import Path

START_YEAR = 2012
END_YEAR = 2026

results = []

print("Building Irish Daily Million archive...")

for year in range(END_YEAR, START_YEAR - 1, -1):

    url = f"https://www.irishlottery.com/daily-million-archive-{year}"

    print(f"Fetching {year}...")

    try:

        tables = pd.read_html(url)

    except Exception as e:

        print(f"Failed {year}: {e}")

        continue

    for table in tables:

        columns = [str(c).lower() for c in table.columns]

        if not any("date" in c for c in columns):
            continue

        for _, row in table.iterrows():

            row_data = [str(x).strip() for x in row.tolist()]

            if len(row_data) < 2:
                continue

            date_text = row_data[0]

            draw_text = row_data[1]

            numbers = []

            for part in draw_text.replace(",", " ").split():

                if part.isdigit():

                    numbers.append(part)

            if len(numbers) < 7:
                continue

            main_numbers = " ".join(numbers[:6])

            bonus = numbers[6]

            formatted = f"{date_text}: {main_numbers} ({bonus})"

            results.append(formatted)

results = list(dict.fromkeys(results))

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
    background: #000;
    color: #00ff66;
    font-family: Consolas, Courier New, monospace;
    padding: 20px;
    line-height: 1.5;
}}

h1 {{
    color: #ffcc66;
    margin-bottom: 25px;
}}

.draw {{
    padding: 2px 0;
    border-bottom: 1px solid #111;
    white-space: pre-wrap;
}}

.draw:hover {{
    background: #111;
}}

.footer {{
    margin-top: 30px;
    color: #666;
    font-size: 12px;
}}

</style>

</head>

<body>

<h1>Irish Daily Million Results Archive (2012–2026)</h1>

{html_results}

<div class="footer">
Automatically updated via GitHub Actions
</div>

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
