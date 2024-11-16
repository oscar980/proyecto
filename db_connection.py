# db_connection.py
import os
from sqlalchemy import create_engine, Table, Column, Integer, String, MetaData, DateTime
from dotenv import load_dotenv

# Cargar variables de entorno desde .env
load_dotenv()

# Configuración de conexión a PostgreSQL usando variables de entorno
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")

DATABASE_URL = f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# Crear motor de conexión
engine = create_engine(DATABASE_URL)
metadata = MetaData()

# Definir las tablas
users_table = Table(
    'users', metadata,
    Column('id', Integer, primary_key=True),
    Column('name', String(50)),
    Column('identification_number', String(20)),
    Column('slug', String(50)),
    Column('video', String(255)),
    Column('email', String(100)),
    Column('gender', String(10)),
    Column('created_at', DateTime),
    Column('updated_at', DateTime)
)

profiles_table = Table(
    'profiles', metadata,
    Column('id', Integer, primary_key=True),
    Column('user_id', Integer),
    Column('onboarding_goal', String(50)),
    Column('created_at', DateTime),
    Column('updated_at', DateTime),
    Column('views', Integer)
)

resumes_table = Table(
    'resumes', metadata,
    Column('id', Integer, primary_key=True),
    Column('user_id', Integer),
    Column('name', String(100)),
    Column('type', String(50)),
    Column('video', String(255)),
    Column('views', Integer),
    Column('created_at', DateTime)
)

challenges_table = Table(
    'challenges', metadata,
    Column('id', Integer, primary_key=True),
    Column('name', String(255)),
    Column('description', String(1000)),
    Column('status', String(50)),
    Column('opencall_objective', String(50)),
    Column('created_at', DateTime)
)

# Crear las tablas en la base de datos si no existen
metadata.create_all(engine)
