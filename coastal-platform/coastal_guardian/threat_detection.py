import pandas as pd
import sqlite3
from sklearn.ensemble import IsolationForest

DB_PATH = 'coastal_data.db'
TABLE = 'coastal_data'

# Load data from SQLite
def load_data():
    conn = sqlite3.connect(DB_PATH)
    df = pd.read_sql_query(f"SELECT * FROM {TABLE}", conn)
    conn.close()
    return df

# Detect anomalies for each parameter
def detect_anomalies(df, parameter='tide_level'):
    param_df = df[df['parameter'] == parameter]
    if param_df.empty:
        print(f"No data found for parameter '{parameter}'.")
        return pd.DataFrame()
    X = param_df[['value']].values
    model = IsolationForest(contamination=0.05, random_state=42)
    param_df['anomaly'] = model.fit_predict(X)
    anomalies = param_df[param_df['anomaly'] == -1]
    return anomalies

if __name__ == '__main__':
    df = load_data()
    print("Loaded data:")
    print(df.head())
    for param in df['parameter'].unique():
        print(f"\nDetecting anomalies for: {param}")
        anomalies = detect_anomalies(df, parameter=param)
        print(anomalies)
