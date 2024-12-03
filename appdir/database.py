import inspect
import sys

from peewee import *
from playhouse.pool import PooledPostgresqlExtDatabase
from playhouse.postgres_ext import *

from appdir import pass_db


DB_CONFIG = {
    'database': 'postgres',
    'user': 'postgres',
    'password': 'qwer',
    'host': '127.0.0.1',
    'port': 5432,
    'max_connections': 32,
    'stale_timeout': 300,
    'register_hstore': False,
    'autocommit': True,
    'autorollback': True
    # 'asyn': True
}

db = PooledPostgresqlExtDatabase(**DB_CONFIG)


def create_all_tables():
    for cls in sys.modules[__name__].__dict__.values():
        if hasattr(cls, '_meta') and inspect.isclass(cls) and issubclass(cls, Model):
            if cls is not BaseModel:
                cls.create_table()


class BaseModel(Model):
    class Meta:
        database = db
        schema = 'py_project_24'


class Book(BaseModel):
    id = CharField(max_length=255, primary_key=True)
    name = CharField(max_length=255)
    published_year = CharField(max_length=255)

    class Meta:
        db_table = "books"


class Worker(BaseModel):
    id = AutoField(primary_key=True)
    name = CharField(max_length=255)

    class Meta:
        db_table = "workers"


class User(BaseModel):
    id = IntegerField(primary_key=True)
    mail = CharField(max_length=255)
    username = CharField(max_length=255)
    creation_date = DateField()

    class Meta:
        db_table = "users"


class Review(BaseModel):
    id = AutoField(primary_key=True)
    book_id = ForeignKeyField(Book)
    user_id = ForeignKeyField(User)
    score = IntegerField()
    description = TextField()

    class Meta:
        db_table = "reviews"


class Role(BaseModel):
    id = AutoField(primary_key=True)
    book_id = ForeignKeyField(Book)
    worker_id = ForeignKeyField(Worker)
    role = CharField(max_length=255)

    class Meta:
        db_table = "roles"


class Image(BaseModel):
    id = AutoField(primary_key=True)
    book_id = ForeignKeyField(Book)
    image_url = TextField()


create_all_tables()
