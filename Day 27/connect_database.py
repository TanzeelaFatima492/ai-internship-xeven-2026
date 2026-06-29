import psycopg2

try:
    connection = psycopg2.connect(
        host="localhost",
        port="5432",
        database="chatbot_db",
        user="postgres",
        password="12345"
    )

    print("Connected to PostgreSQL!")

    connection.close()

except Exception as e:
    print("Connection Failed")
    print(e)