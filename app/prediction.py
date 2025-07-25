import sqlite3
import pandas as pd
from sklearn.linear_model import LinearRegression
from datetime import datetime
import os 
def prediiction_in_hr():

    DB_PATH = os.path.join("data", "weather.db")

    con = sqlite3.connect(DB_PATH)
    df = pd.read_sql_query("SELECT timestamp, temperature, feels_like FROM weather_data", con)
    con.close()


    df.dropna()

    df['timestamp'] = pd.to_datetime(df['timestamp'])
    df['time_num'] = df['timestamp'].astype(int) // 10**9  # UNIX time in seconds

    X = df[['time_num']]
    y = df['temperature']

    model = LinearRegression()
    model.fit(X, y)

    now = int(datetime.now().timestamp())
    in_an_hour = now + 3600
    in_an_hour_dt = datetime.fromtimestamp(in_an_hour).strftime("%H:%M:%S")
    X_new = pd.DataFrame([[in_an_hour]], columns=['time_num']) # type: ignore
    prediction = model.predict(X_new)
    
    return prediction[0], in_an_hour_dt
