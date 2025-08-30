import pandas as pd
import numpy as np
import sqlite3
import json
from datetime import datetime, timedelta
import random

class DataCollector:
    def __init__(self, db_path='coastal_data.db'):
        self.db_path = db_path
        self._init_db()

    def _init_db(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS coastal_data (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT,
                source TEXT,
                parameter TEXT,
                value REAL
            )
        ''')
        conn.commit()
        conn.close()

    def fetch_mock_sensor_data(self):
        now = datetime.now()
        sensors = [
            {'parameter': 'tide_level', 'value': round(random.uniform(0.5, 3.5), 2)},
            {'parameter': 'wind_speed', 'value': round(random.uniform(5, 25), 2)},
            {'parameter': 'pollution_index', 'value': round(random.uniform(10, 100), 2)}
        ]
        data = []
        for s in sensors:
            data.append({
                'timestamp': now.isoformat(),
                'source': 'sensor',
                'parameter': s['parameter'],
                'value': s['value']
            })
        return data

    def fetch_satellite_data(self):
        now = datetime.now()
        # Simulate satellite data (could be loaded from a JSON file or dummy API)
        sat_data = [
            {'parameter': 'sea_temp', 'value': round(random.uniform(20, 32), 2)},
            {'parameter': 'cyclone_alert', 'value': random.choice([0, 1])}
        ]
        data = []
        for s in sat_data:
            data.append({
                'timestamp': now.isoformat(),
                'source': 'satellite',
                'parameter': s['parameter'],
                'value': s['value']
            })
        return data

    def load_historical_data(self, csv_path):
        df = pd.read_csv(csv_path)
        data = []
        for _, row in df.iterrows():
            data.append({
                'timestamp': pd.to_datetime(row['timestamp']).isoformat() if 'timestamp' in row else datetime.now().isoformat(),
                'source': 'historical',
                'parameter': row['parameter'] if 'parameter' in row else 'unknown',
                'value': row['value'] if 'value' in row else np.nan
            })
        return data

    def clean_data(self, data):
        df = pd.DataFrame(data)
        # Fill missing values
        df['timestamp'] = pd.to_datetime(df['timestamp'], errors='coerce').dt.strftime('%Y-%m-%dT%H:%M:%S')
        df['parameter'] = df['parameter'].fillna('unknown')
        df['value'] = pd.to_numeric(df['value'], errors='coerce').fillna(np.nan)
        df['source'] = df['source'].fillna('unknown')
        df = df.dropna(subset=['timestamp', 'parameter', 'value'])
        return df.to_dict('records')

    def save_to_db(self, data):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        for entry in data:
            cursor.execute('''
                INSERT INTO coastal_data (timestamp, source, parameter, value)
                VALUES (?, ?, ?, ?)
            ''', (entry['timestamp'], entry['source'], entry['parameter'], entry['value']))
        conn.commit()
        conn.close()
        print('Data successfully saved to database.')

# Example usage
if __name__ == '__main__':
    collector = DataCollector()
    sensor = collector.fetch_mock_sensor_data()
    sat = collector.fetch_satellite_data()
    hist = collector.load_historical_data('historical_data.csv')
    all_data = sensor + sat + hist
    cleaned = collector.clean_data(all_data)
    collector.save_to_db(cleaned)
