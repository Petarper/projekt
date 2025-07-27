import unittest
import sys
import os
ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, ROOT_DIR)
from unittest.mock import patch, MagicMock
from app.scraper import fetch_html, parse_data, insert_data
import sqlite3

class TestScraper(unittest.TestCase):
    def test_parse_weather(self):
        html = '''
            <div class="h2">27&nbsp;°C</div>
            <p>Feels Like: 24&nbsp;°C</p>
        '''
        temp, feels_like = parse_data(html)
        self.assertEqual(temp, 27)
        self.assertEqual(feels_like, '24')
    @patch('app.scraper.requests.get')
    def test_fetch_weather_html(self, mock_get):
        mock_response = MagicMock()
        mock_response.content = b"<html></html>"
        mock_get.return_value = mock_response

        html = fetch_html("https://example.com")
        self.assertEqual(html, b"<html></html>")
        mock_get.assert_called_once()
    
    def test_insert_weather(self):
        conn = sqlite3.connect(":memory:")
        cursor = conn.cursor()
        cursor.execute("CREATE TABLE weather_data (temperature INTEGER, feels_like INTEGER)")
        conn.commit()

        # Override the DB_PATH to use in-memory database
        insert_data(28, 26, db_path=":memory:", conn=conn)  # this won't insert to our test DB

        # So we insert manually using same logic to test the schema instead
        conn.commit()
        cursor.execute("SELECT * FROM weather_data")
        rows = cursor.fetchall()
        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0], (28, 26))
        conn.close()

if __name__ == "__main__":
    unittest.main()
