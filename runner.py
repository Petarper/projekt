import time 
import subprocess

interval = 45

while True:
    subprocess.run(["python3", "scraper.py"])
    time.sleep(interval * 60)
