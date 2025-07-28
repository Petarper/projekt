import time 
import subprocess

interval = 45

while True:
    subprocess.run(["python3", "app/scraper.py"])
    subprocess.run(["python3", "app/prediction.py"])
    time.sleep(interval * 60)
