#あくまでjsonデータの生成のみなのでこの辺は素で書く

import requests
import json
from pathlib import Path
from dotenv import load_dotenv
import os

load_dotenv()

DATA_DIR = Path(__file__).parent.parent / "data"
DATA_DIR.mkdir(exist_ok=True)

URL = os.getenv("API_URL")


if not URL:
    raise RuntimeError("Environment variable 'API_URL' is not set.")

res = requests.get(URL, timeout=10)
res.raise_for_status()

tmp_path = DATA_DIR / "data.json.tmp"
final_path = DATA_DIR / "data.json"

with open(tmp_path, "w", encoding="utf-8") as f:
    json.dump(res.json(), f, ensure_ascii=False, indent=2)

tmp_path.replace(final_path)

print("data.json updated")
