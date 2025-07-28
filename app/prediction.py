import sqlite3
import pandas as pd
from sklearn.linear_model import LinearRegression
from datetime import datetime
from zoneinfo import ZoneInfo
import os 


def connect(db_path):

    con = sqlite3.connect(db_path)
    df = pd.read_sql_query("SELECT timestamp, temperature, feels_like FROM weather_data", con)
    con.close()
    
    df = df.dropna()
    if df.empty or len(df) < 2:
        print("DF too small or empty")
        return None
    return df

def prediction_in_hr(df):
    if df is None:
        return None, None
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    df['time_num'] = df['timestamp'].astype('int64', errors='raise') // 10**9  # UNIX time in seconds

    X = df[['time_num']]
    y = df['temperature']

    model = LinearRegression()
    model.fit(X, y)

    now = int(datetime.now(ZoneInfo("Europe/Berlin")).timestamp())
    in_an_hour = now + 3600
    in_an_hour_dt = datetime.fromtimestamp(in_an_hour).strftime("%H:%M:%S")
    X_new = pd.DataFrame([[in_an_hour]], columns=['time_num']) # type: ignore
    prediction = model.predict(X_new)
    
    return prediction[0], in_an_hour_dt

if __name__ == "__main__":

    DB_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "data", "weather.db"))
    df = connect(DB_PATH)
    pred, time_str = prediction_in_hr(df)
    if pred is not None:
        print(f"Prediction for {time_str}: {pred:.2f}")
    else:
        print("Not enough data to make prediction.")
