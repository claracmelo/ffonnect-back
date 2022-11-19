import os
from playhouse.db_url import connect

from peewee import * 
import datetime 
from flask_login import UserMixin

if os.environ.get("FLASK_ENV")!="production": # later we will manually add this env var
                              # in heroku so we can write this code
  DATABASE = connect(os.environ.get('DATABASE_URL')) # heroku will add this
                                                     # env var for you
                                                     # when you provision the
                                                     # Heroku Postgres Add-on
else:
  DATABASE = SqliteDatabase('members.sqlite')

class User(UserMixin, Model):
    username = CharField()
    dob = DateField()
    email = CharField(unique=True)
    password = CharField()
    # photo = ??

    class Meta:
        database = DATABASE

class Member(Model):
    name = CharField() #string
    relation = CharField() #mom, dad, sis, etc
    dob = DateField() #date of birth
    status = BooleanField() #alive? if not, dod field -- default FALSE
    dod = DateField() #date of death - default NULL
    direct_relation = CharField() #string
    # change this:
    # owner = ForeignKeyField(User, backref='dogs') # string for now, later this can be a relation
    # for this:
    relation_id = ForeignKeyField(User, backref='members') #user_id connected to family members
    created_at = DateTimeField(default=datetime.datetime.now)

    class Meta:
        database = DATABASE 

def initialize(): 
    DATABASE.connect()  
    DATABASE.create_tables([User,Member], safe=True)
    print("Connected to the DB and created tables if they don't already exist")
    DATABASE.close()


