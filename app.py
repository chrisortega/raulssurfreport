from flask import Flask, jsonify, render_template
import requests
from datetime import datetime, timedelta
from collections import Counter

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/api/surf")
def surf_forecast():
    url = "https://services.surfline.com/kbyg/spots/forecasts/surf"
    params = {
        "cacheEnabled": "false",
        "days": "5",
        "intervalHours": "1",
        "spotId": "584204204e65fad6a77091be",
        "units[waveHeight]": "M"
    }

    res = requests.get(url, params=params)
    data = res.json()

    surf_data = data["data"]["surf"]
    daily_summary = {}

    for item in surf_data:
        utc_offset = item["utcOffset"]
        local_time = datetime.utcfromtimestamp(item["timestamp"]) + timedelta(hours=utc_offset)
        date_key = local_time.strftime("%Y-%m-%d")

        if date_key not in daily_summary:
            daily_summary[date_key] = {"min": [], "max": [], "conditions": []}

        surf = item["surf"]
        daily_summary[date_key]["min"].append(surf["min"])
        daily_summary[date_key]["max"].append(surf["max"])
        if surf.get("humanRelation"):
            daily_summary[date_key]["conditions"].append(surf["humanRelation"])

    result = []
    for date_key, values in daily_summary.items():
        date_obj = datetime.strptime(date_key, "%Y-%m-%d")
        condition = "N/A"
        if values["conditions"]:
            condition = Counter(values["conditions"]).most_common(1)[0][0]

        min_val = round(min(values["min"]), 1)
        max_val = round(max(values["max"]), 1)

        # Custom surf quality thresholds
        if max_val < 0.6:
            color = "#e74c3c"   # red
            quality = "Bad"
        elif max_val < 0.9:
            color = "#f39c12"   # orange
            quality = "Poor"
        elif max_val < 1.4:
            color = "#2ecc71"   # light green
            quality = "Good"
        elif max_val < 2.0:
            color = "#27ae60"   # darker green
            quality = "Great"
        else:
            color = "#004d00"   # deep green
            quality = "Epic"

        result.append({
            "date": date_obj.strftime("%A, %b %d"),
            "min": min_val,
            "max": max_val,
            "condition": condition,
            "quality": quality,
            "color": color
        })

    return jsonify(result)


if __name__ == "__main__":
    app.run(debug=True)
