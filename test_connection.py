from sqlalchemy import create_engine

DB_USER = "postgres"
DB_PASSWORD = "1234"
DB_HOST = "localhost"
DB_PORT = "5432"
DB_NAME = "fuel_dss"

import os
from sqlalchemy import create_engine

DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(DATABASE_URL)
connection = engine.connect()

print("Database Connected Successfully!")