import psycopg2
import time
from src.vault_client import get_db_credentials

def get_db_connection():
    creds = get_db_credentials()
    return psycopg2.connect(
        host="db",
        user=creds["user"],
        password=creds["password"],
        database=creds["dbname"]
    )

def init_db():
    # Даем СУБД время на запуск внутри docker-compose
    time.sleep(5)
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS predictions_history (
                id SERIAL PRIMARY KEY,
                age INT,
                current_weight NUMERIC,
                caloric_deficit NUMERIC,
                prediction NUMERIC,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """)
        conn.commit()
        cursor.close()
        conn.close()
        print("[INFO] База данных успешно инициализирована.")
    except Exception as e:
        print(f"[ERROR] Ошибка инициализации БД: {e}")