from logging.config import fileConfig
from os import environ
from alembic import context

# Alembic Config объект предоставляет доступ
# к переменным из файла alembic.ini
# config = context.config
#
# section = config.config_ini_section
# config.set_section_option(section, "DB_USER", environ['DB_USER'])
# config.set_section_option(section, "DB_PASS", environ['DB_PASS'])
# config.set_section_option(section, "DB_NAME", environ['DB_NAME'])
# config.set_section_option(section, "DB_HOST", environ['DB_HOST'])
#
# fileConfig(config.config_file_name)
#
# target_metadata = [users.metadata, posts.metadata]


from logging.config import fileConfig
from alembic import context
from models import users, posts
from models.users import metadata as users_metadata
from models.posts import metadata as posts_metadata
# Alembic Config объект предоставляет доступ
# к переменным из файла alembic.ini
config = context.config

# Подключаем переменные окружения
DB_USER = environ.get("DB_USER")
DB_PASS = environ.get("DB_PASS")
DB_NAME = environ.get("DB_NAME")
DB_HOST = environ.get("DB_HOST")

# Устанавливаем опции в секции
section = config.config_ini_section
config.set_section_option(section, "DB_USER", DB_USER)
config.set_section_option(section, "DB_PASS", DB_PASS)
config.set_section_option(section, "DB_NAME", DB_NAME)
config.set_section_option(section, "DB_HOST", DB_HOST)

# Применяем конфигурацию логгера
fileConfig(config.config_file_name)

# Устанавливаем метаданные
# target_metadata = [users_metadata, posts_metadata]
# print("Target metadata:", target_metadata)
target_metadata = None
# target_metadata = {'fdf':3445}
