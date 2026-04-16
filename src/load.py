import sys
import os
import pandas as pd
from sqlalchemy import create_engine
from dotenv import load_dotenv

load_dotenv()

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from transform import parse_evtx_directory_to_dataframe


def load_to_postgres(df, db_url, table_name):
    if df.empty:
        print("[!] No data to load.")
        return

    print("[*] Connecting to database via SSH Tunnel...")
    engine = create_engine(db_url)

    try:
        df.to_sql(table_name, engine, if_exists='replace', index=False)
        print(f"[*] Success! Loaded {len(df)} records into '{table_name}' table.")
    except Exception as e:
        print(f"[!] Database load error: {e}")


if __name__ == "__main__":
    target_dir = "EVTX-ATTACK-SAMPLES/Discovery"
    df = parse_evtx_directory_to_dataframe(target_dir)

    if not df.empty:
        DB_USER = os.getenv("DB_USER")
        DB_PASSWORD = os.getenv("DB_PASSWORD")
        DB_HOST = "localhost"
        DB_NAME = "forensic_logs"

        DB_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:5432/{DB_NAME}"

        df_clean = df.drop(columns=['RawXML'])
        load_to_postgres(df_clean, DB_URL, "windows_events")
    else:
        print("[!] Pipeline aborted. No data extracted.")