import requests
import pandas as pd
import time

BASE_URL = "https://planning.lacity.gov/dcpapi2/meetings/api/cpc/commissions/{year}"
START_YEAR = 2000
END_YEAR = 2026

records = []
for year in range(START_YEAR, END_YEAR + 1):
    url = BASE_URL.format(year=year)
    try:
        resp = requests.get(url, timeout=30)
        resp.raise_for_status()
        data = resp.json()
        if isinstance(data, list):
            for item in data:
                item["year"] = year
                records.append(item)
        elif isinstance(data, dict):
            data["year"] = year
            records.append(data)
        print(f"{year}: {len(data) if isinstance(data, list) else 1} records")
    except Exception as e:
        print(f"{year}: ERROR — {e}")
    time.sleep(0.3)

df = pd.DataFrame(records)
out_path = "/Users/tylerjacobson/Dropbox/Lawsuits Asymmetry/data/raw/cpc_minutes/cpc_meetings.csv"
df.to_csv(out_path, index=False)
print(f"\nSaved {len(df)} rows to {out_path}")
