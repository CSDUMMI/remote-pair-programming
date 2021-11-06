import peewee as pw
import os

DATABASE = os.environ["DATABASE"]

database = pw.SqliteDatabase(DATABASE)

class BaseModel(pw.Model):
    class Meta:
        database = database

class User(BaseModel):
    id = pw.UUIDField(primary_key = True)
    name = pw.TextField(null = True)
    languages = pw.ArrayField(CharField, default = ["eng","deu"])
    
    password_hash = pw.CharField(max_length=64)
    password_salt = pw.CharField(max_length=64)
    
class Experience(BaseModel):
    topic = pw.CharField()
    user = pw.ForeignKeyField(User, backref = "experience")
    exp = pw.IntegerField()

