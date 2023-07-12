import datetime
import json

import psycopg2
import os


class Database:
    """
    Helper class storing CRUD methods for the database
    """
    def __init__(self, url=os.getenv("POSTGRES_URL")):
        self.connector = psycopg2.connect(url)  # Connect to database with provided URL

    def get_daily_results(self, date=None):
        if not date:
            date = datetime.datetime.utcnow().date().strftime("%Y-%m-%d")
        cursor = self.connector.cursor()
        cursor.execute("SELECT * FROM results WHERE date = %s", (date,))
        data = cursor.fetchone()
        print(data)
        return [data[0], json.loads(data[1])]

    def update_daily_results(self, results):
        cursor = self.connector.cursor()
        date = datetime.datetime.utcnow().date().strftime("%Y-%m-%d")
        cursor.execute("INSERT INTO results VALUES (%s, %s) "
                       "ON CONFLICT (date) DO UPDATE SET responses = excluded.responses", (date, json.dumps(results)))
        self.connector.commit()

