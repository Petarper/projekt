from bs4 import BeautifulSoup
import requests
import re
import sqlite3
import os 

DB_PATH = os.path.join("data", "weather.db")

def fetch_html(URL):
    page = requests.get(URL)
    return page.content


def parse_data(page):
    soup = BeautifulSoup(page, "html.parser")
    temp_div = soup.find("div", class_="h2")
    temperature = temp_div.text.strip() if temp_div else None

    feels_like = None
    p_tags = soup.find_all("p")
    

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

    return temp, feels_like

def insert_data(temp, feels_like, db_path = DB_PATH, conn = None):
    should_close = False
    if conn is None:
        conn = sqlite3.connect(db_path)
        should_close = True
    
    cursor = conn.cursor()


    cursor.execute(
        "INSERT INTO weather_data(temperature, feels_like) VALUES(?, ?)",
        (temp, feels_like)
            )
    conn.commit()
    if should_close:
        conn.close()


if __name__ == "__main__":
    URL = ("https://www.timeanddate.com/weather/@3187232")
    page = fetch_html(URL)
    temp, feels_like = parse_data(page)
    insert_data(temp, feels_like)

    print('Feels like: ', feels_like)
    print('Actual temperature: ', temp)

