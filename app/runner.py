import time 
import subprocess

interval = 45

while True:
    subprocess.run(["python3", "app/scraper.py"])
    time.sleep(interval * 60)
