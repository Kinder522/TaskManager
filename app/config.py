import os

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql+asyncpg://myuser:mypassword@db:5432/mydatabase")