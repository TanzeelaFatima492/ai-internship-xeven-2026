
PG_USER = "postgres"
PG_PASSWORD = 7866
PG_HOST = "localhost"
PG_PORT = 5432
PG_DATABASE = "postgres"
# SQL Server connection string from environment variables
DB_URI = f"postgresql://{PG_USER}:{PG_PASSWORD}@{PG_HOST}:{PG_PORT}/{PG_DATABASE}?sslmode=disable"

