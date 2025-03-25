import psycopg
from psycopg.rows import dict_row
from .config import settings



# Create a function to get the database connection
def get_db_connection():
    try:
        conn = psycopg.connect(
            host=settings.database_hostname,
            dbname=settings.database_name,
            user=settings.database_username,  
            password=settings.database_password,
            row_factory=dict_row
        )
        print("Connected to the database")
        return conn
    except Exception as e:
        print(f"Database connection error: {e}")
        raise

# Create a dependency for FastAPI to use
def get_db():
    conn = get_db_connection()
    try:
        yield conn
    finally:
        conn.close()