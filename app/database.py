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
        try:
            assert data is not None
            return [data[0], json.loads(data[1])]
        except AssertionError:
            return [date.strftime("%Y-%m-%d"), {}]

    def update_daily_results(self, results):
        cursor = self.connector.cursor()
        date = datetime.datetime.utcnow().date().strftime("%Y-%m-%d")
        cursor.execute("INSERT INTO results VALUES (%s, %s) "
                       "ON CONFLICT (date) DO UPDATE SET responses = excluded.responses", (date, json.dumps(results)))
        self.connector.commit()
        return

    def add_new_user(self, token):
        cursor = self.connector.cursor()
        cursor.execute("INSERT INTO users (token) VALUES (%s)", (token,))
        self.connector.commit()
        return

    def get_user(self, token):
        cursor = self.connector.cursor()
        cursor.execute("SELECT * FROM users WHERE token = %s", (token,))
        return cursor.fetchone()

    def update_user(self, user_data):
        cursor = self.connector.cursor()
        cursor.execute("UPDATE users SET max_streak = %s, current_streak = %s, total_solves = %s, last_solve = %s WHERE token = %s", (
            user_data[2], user_data[3], user_data[4], user_data[5], user_data[1]
        ))
        self.connector.commit()
        return
