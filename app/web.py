import sqlite3
from flask import Flask
from app.prediction import prediiction_in_hr
import os

app = Flask(__name__)

DB_PATH = os.path.join("data", "weather.db")

@app.route("/")
def home():
    predict, in_one_hour_dt = prediiction_in_hr()
    

    con = sqlite3.connect(DB_PATH)
    cur = con.cursor()
    cur.execute("SELECT timestamp, temperature, feels_like FROM weather_data ORDER BY timestamp DESC LIMIT 10")
    rows = cur.fetchall()
    con.close()

    table_rows = ""
    for ts, temp, feels_like in rows:
        table_rows += f"<tr><td>{ts}</td><td>{temp}</td><td>{feels_like}</td></tr>"


        # Full HTML with prediction and table
    html = f"""
    <h1>Predicted temperature at {in_one_hour_dt}: {predict:.2f} °C</h1>
    <h2>Recent Weather Data</h2>
    <table border="1" cellpadding="5" cellspacing="0">
      <tr><th>Timestamp</th><th>Temperature (°C)</th><th>Feels Like (°C)</th></tr>
      {table_rows}
    </table>
    """

    return html

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
