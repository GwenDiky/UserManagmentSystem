import logging
import logging.config

import uvicorn
from fastapi import FastAPI
from os import environ
import os

# database
from sqlalchemy.orm import Session
from sqlalchemy.exc import OperationalError
import databases  # async query execution
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

app = FastAPI()

# Configure logging
project_root = os.path.dirname(os.path.abspath(__file__))
logging_conf_path = os.path.join(project_root, '..', 'logging.conf')

# Загрузка конфигурации логирования из файла logging.conf
logging.config.fileConfig(logging_conf_path)
logger = logging.getLogger(__name__)

# Дополнительная настройка для записи в файл app.log
file_handler = logging.FileHandler('app.log')
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
logger.addHandler(file_handler)
logging.basicConfig(level=logging.DEBUG, filename='../app.log', filemode='a', format='%(asctime)s - %(levelname)s - %('
                                                                                     'message)s')
logger = logging.getLogger(__name__)

DB_USER = environ.get("DB_USER", "postgres")
DB_PASSWORD = environ.get("DB_PASSWORD", "root")
DB_HOST = environ.get("DB_HOST", "localhost")
DB_PORT = environ.get("DB_PORT", 5432)
DB_NAME = "management_systems"

SQLALCHEMY_DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# Create the engine with the password parameter
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SQLALCHEMY_DATABASE_URL = f"postgresql://postgres:root@localhost:5432/management_systems"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base = declarative_base()
# create a database object that will be used to execute queries
database = databases.Database(SQLALCHEMY_DATABASE_URL)


# target_metadata = [users.metadata, posts.metadata]

def test_db_connection():
    try:
        db: Session = SessionLocal()
        print("Connection to the database established successfully.")
        return True
    except OperationalError as e:
        print("Failed to connect to the database.")
        print(e)
        return False
    finally:
        db.close()


# checking the connection with db
test_db_connection()


async def startup_event():
    """establishing the connection with db"""
    print("Starting up...")


async def shutdown_event():
    """disconnecting the connection with db"""
    print("Shutting down...")


app.add_event_handler("startup", startup_event)
app.add_event_handler("shutdown", shutdown_event)


@app.get("/")
async def root():
    return "Hello, world"


# @app.get("/")
# async def root():
#     """Сбор из БД данных пользователей"""
#     query = (
#         select(
#             [
#                 posts_table.c.id,
#                 posts_table.c.created_at,
#                 posts_table.c.title,
#                 posts_table.c.content,
#                 posts_table.c.user_id,
#                 users_table.c.name.label("user_name"),
#             ]
#         )
#         .select_from(posts_table.join(users_table))
#         .order_by(desc(posts_table.c.created_at))
#     )
#     return await database.fetch_all(query)


@app.get("/items/{item_id}")
async def read_item(item_id: int):
    return {'item_id': item_id}


@app.get("/users")
async def read_users():
    return ["Rick", "Morty"]


@app.get("/users/me")
async def read_user_me():
    return {"user_id": "the current_user"}


@app.get("/users/{user_id}")
async def read_user(user_id: str):
    return {"user_id": user_id}


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
