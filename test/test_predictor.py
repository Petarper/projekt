import os, sys
ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, ROOT_DIR)

from app.prediction import connect, prediction_in_hr
import pandas as pd
import unittest
from unittest.mock import patch
from datetime import datetime, timedelta

class TestScraper(unittest.TestCase):

    def test_prediction_in_hr(self):
        now = datetime.now()
        timestamps = [now - timedelta(hours=i) for i in range(5)][::-1]
        data = {
            "timestamp": [ts.strftime("%Y-%m-%d %H:%M:%S") for ts in timestamps],
            "temperature": [20 + i for i in range(5)],
            "feels_like": [19 + i for i in range(5)]
        }
        df = pd.DataFrame(data)

        pred, time_str = prediction_in_hr(df)
        self.assertIsNotNone(pred, "Prediction returned None — model likely didn't fit.")
        self.assertIsInstance(pred, float)
        self.assertIsInstance(time_str, str)
        

    @patch("pandas.read_sql_query")
    @patch("sqlite3.connect")
    def test_connect(self, mock_connect, mock_read_sql):
        mock_df = pd.DataFrame({
            "timestamp": ["2023-07-01 12:00:00", "2023-07-01 13:00:00"],
            "temperature": [25.0, 26.5],
            "feels_like": [24.0, 26.0]
        })
        mock_read_sql.return_value = mock_df

        df = connect("fake_path.db")

        self.assertIsNotNone(df)
        self.assertFalse(df.empty)
        self.assertIn("temperature", df.columns)

    @patch("pandas.read_sql_query")
    @patch("sqlite3.connect")
    def test_connect_returns_none_if_df_too_small(self, mock_connect, mock_read_sql):
        mock_df = pd.DataFrame({
            "timestamp": ["2023-07-01 12:00:00"],
            "temperature": [25.0],
            "feels_like": [24.0]
        })
        mock_read_sql.return_value = mock_df

        df = connect("fake_path.db")

        self.assertIsNone(df)

if __name__ == "__main__":
    unittest.main()

