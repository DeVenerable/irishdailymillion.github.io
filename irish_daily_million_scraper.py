import requests
from pathlib import Path

url = "https://www.irishlottery.com/daily-million-archive-2024"

headers = {
    "User-Agent": "Mozilla/5.0"
}

response = requests.get(
    url,
    headers=headers,
    timeout=20
)

print("STATUS:", response.status_code)

Path("debug.html").write_text(
    response.text,
    encoding="utf-8"
)

print("Saved debug.html")
