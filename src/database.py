import peewee as pw
import os

DATABASE = os.environ["DATABASE"]

database = pw.SqliteDatabase(DATABASE)

class BaseModel(pw.Model):
    class Meta:
        database = database

class User(BaseModel):
    