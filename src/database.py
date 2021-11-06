import peewee as pw
import os

DATABASE = os.environ["DATABASE"]

database = pw.SqliteDatabase(DATABASE)

class BaseModel(pw.Model):
    class Meta:
        database = database

class User(BaseModel):
    id = pw.UUIDField(primary_key = True)
    name = pw.TextField(unique = True)
    languages = pw.ArrayField(CharField, default = ["eng","deu"])
    
    password_hash = pw.BlobField()
    password_salt = pw.BlobField()
    
class Experience(BaseModel):
    topic = pw.CharField()
    user = pw.ForeignKeyField(User, backref = "experience")
    exp = pw.IntegerField()

