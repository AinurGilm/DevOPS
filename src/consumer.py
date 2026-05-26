import os
import json
import psycopg2
from kafka import KafkaConsumer
from src.database import get_db_connection

# Берем сервер из переменных окружения, которые заданы в docker-compose
KAFKA_SERVER = os.getenv("KAFKA_BOOTSTRAP_SERVERS", "ml_kafka_broker:29092")
TOPIC_NAME = "ml_predictions_topic"

def main():
    print("[INFO] Запуск Kafka Consumer...")
    
    # Исправлено: value_deserializer вместо value_serializer
    consumer = KafkaConsumer(
        TOPIC_NAME,
        bootstrap_servers=KAFKA_SERVER,
        value_deserializer=lambda v: json.loads(v.decode('utf-8')),
        auto_offset_reset='earliest',
        group_id='ml-counters'
    )

    for message in consumer:
        event = message.value
        print(f"[CONSUMER] Получено событие: {event}")
        
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            
            # Исправлено: ключи приведены в строгое соответствие с payload из FastAPI
            cursor.execute(
                """
                INSERT INTO predictions_history (age, current_weight, caloric_deficit, prediction)
                VALUES (%s, %s, %s, %s);
                """,
                (
                    int(event.get('Age', 0)), 
                    float(event.get('Current_Weight', 0)), 
                    float(event.get('Caloric_Deficit', 0)), 
                    float(event.get('prediction', 0))
                )
            )
            conn.commit()
            cursor.close()
            conn.close()
            print("[CONSUMER] Данные успешно сохранены в PostgreSQL.")
        except Exception as e:
            print(f"[CONSUMER ERROR] Ошибка записи в БД: {e}")

if __name__ == "__main__":
    main()