import json
import psycopg2
import hashlib
from psycopg2 import sql
from awscli.clidriver import create_clidriver

# Read JSON data from AWS SQS Queue
def read_from_sqs(queue_url):
    # Simulate reading from SQS Queue
    sample_sqs_data = [
        {
            "user_id": "user123",
            "device_id": "device456",
            "ip": "192.168.1.1",
            "locale": "en",
            "app_version": 2,
            "create_date": "2023-08-29",
        },
        # Add more sample data here...
    ]
    return sample_sqs_data
# Mask PII data while preserving the ability to identify duplicates
def mask_pii(data):
    masked_data = []
    mask_map = {}

    for record in data:
        masked_record = record.copy()
        
        # Mask device_id
        if record["device_id"] not in mask_map:
            masked_device_id = hashlib.sha256(record["device_id"].encode()).hexdigest()
            mask_map[record["device_id"]] = masked_device_id
        else:
            masked_device_id = mask_map[record["device_id"]]
        masked_record["masked_device_id"] = masked_device_id

        # Mask ip
        if record["ip"] not in mask_map:
            masked_ip = hashlib.sha256(record["ip"].encode()).hexdigest()
            mask_map[record["ip"]] = masked_ip
        else:
            masked_ip = mask_map[record["ip"]]
        masked_record["masked_ip"] = masked_ip

        masked_data.append(masked_record)

    return masked_data
# Write masked data to PostgreSQL database
def write_to_postgres(data):
    conn = psycopg2.connect(
        dbname="postgres", user="postgres", password="postgres", host="localhost", port="5432"
    )
    cursor = conn.cursor()

    for record in data:
        insert_query = sql.SQL(
            "INSERT INTO user_logins (user_id, device_type, masked_ip, masked_device_id, locale, app_version, create_date) VALUES (%s, %s, %s, %s, %s, %s, %s)"
        )
        cursor.execute(
            insert_query,
            [
                record["user_id"],
                record["device_type"],
                record["masked_ip"],
                record["masked_device_id"],
                record["locale"],
                record["app_version"],
                record["create_date"],
            ],
        )
conn.commit()
    cursor.close()
    conn.close()

# Main function
if __name__ == "__main__":
    sqs_queue_url = "http://localhost:4566/000000000000/login-queue"
    data = read_from_sqs(sqs_queue_url)
    masked_data = mask_pii(data)
    write_to_postgres(masked_data)
