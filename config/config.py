import os

PSQL_URL = os.environ['POSTGRES_URL']
PSQL_URL = PSQL_URL.replace("postgres", "postgresql", 1)
