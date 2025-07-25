from bs4 import BeautifulSoup
import requests
import re
import sqlite3
import os 

DB_PATH = os.path.join("data", "weather.db")

URL = ("https://www.timeanddate.com/weather/@3187232")
page = requests.get(URL)

soup = BeautifulSoup(page.content, "html.parser")

temp_div = soup.find("div", class_="h2")
temperature = temp_div.text.strip() if temp_div else None

p_tags = soup.find_all("p")

feels_like = None

for p in p_tags:
    if "Feels Like:" in p.text:
        match = re.search(r"Feels Like:\s*(\d+)", p.text)
        if match:
            feels_like = match.group(1)
        break

temp = None
if temperature:
    temp = re.findall(r'\d+', temperature)
    temp = int(temp[0]) if temp else None

conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()


cursor.execute(
        "INSERT INTO weather_data(temperature, feels_like) VALUES(?, ?)",
        (temp, feels_like)
            )
conn.commit()
conn.close()

print('Feels like: ', feels_like)
print('Actual temperature: ', temp)
