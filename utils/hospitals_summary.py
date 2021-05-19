# Usage:
# hospitals_summary.py hospitals.csv > output.json
#
import csv
import sys
import json

with open(sys.argv[1]) as csvfile:
    reader = csv.DictReader(csvfile)
    rows = []
    for row in reader:
        hospital_id = int(row["編號"])
        hospital = {
            "address": row["地址"],
            "department": row["科別"],
            "hospitalId": int(row["編號"]),
            "location": row["縣市"],
            "name": row["醫院名稱"],
            "phone": row["電話"],
            "website": row["Website"],
        }
        rows.append(hospital)

    print(json.dumps(rows, ensure_ascii=False, indent=2))
