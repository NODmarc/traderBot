import psycopg2
from config import HOST, USER, PASSWORD, DB_NAME

def get_all_chat_ids():
    chat_ids = []
    try:
        connection = psycopg2.connect(
            host=HOST,
            user=USER,
            password=PASSWORD,
            database=DB_NAME
        )
        with connection.cursor() as cursor:
            cursor.execute("SELECT chat_id FROM telegram_users")
            rows = cursor.fetchall()
            chat_ids = [row[0] for row in rows]
    except Exception as _ex:
        print("[INFO] Error while fetching chat_ids from PostgreSQL", _ex)
    finally:
        if connection:
            connection.close()
            print("[INFO] PostgreSQL connection closed - get_all_chat_ids")
    return chat_ids

def insert_subscribers(chat_id):
    try:
        # connect db
        connection = psycopg2.connect(
            host=HOST,
            user=USER,
            password=PASSWORD,
            database=DB_NAME
        )

        # the cursor for performing db operation
        with connection.cursor() as cursor:
            cursor.execute(
                """INSERT INTO telegram_users (chat_id) VALUES (%s)""",
                (chat_id,)
            )
            connection.commit()
            print(f"Chat ID {chat_id} inserted successfully.")

    except Exception as _ex:
        print("[INFO] Error while working with PostgreSQL", _ex)
    finally:
        if connection:
            connection.close()
            print("[INFO] PostgreSQL connection closed - insert_subscribers")

def delete_subscriber(chat_id):
    try:
        connection = psycopg2.connect(
            host=HOST,
            user=USER,
            password=PASSWORD,
            database=DB_NAME
        )
        with connection.cursor() as cursor:
            cursor.execute(
                "DELETE FROM telegram_users WHERE chat_id = %s",
                (chat_id,)
            )
            connection.commit()
            print(f"Chat ID {chat_id} deleted successfully.")
    except Exception as _ex:
        print("[INFO] Error while deleting from PostgreSQL", _ex)
    finally:
        if 'connection' in locals() and connection:
            connection.close()
            print("[INFO] PostgreSQL connection closed - delete_subscriber")