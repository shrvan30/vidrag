import psycopg2
from config import POSTGRES_URL

def get_conn():
    return psycopg2.connect(POSTGRES_URL)