import os
from playhouse.db_url import connect

from peewee import * 
import datetime 
from flask_login import UserMixin

DATABASE = connect(os.environ.get('DATABASE_URL') or 'sqlite:///members.sqlite')

class User(UserMixin, Model):
    username = CharField()
    last_name = CharField(null=True)
    dob = DateField()
    email = CharField(unique=True)
    password = CharField()
    
    # photo = ??

    class Meta:
        database = DATABASE

class Member(Model):
    name = CharField() #string
    last_name = CharField(null=True) #string
    relation = CharField() #mom, dad, sis, etc
    dob = DateField() #date of birth
    status = BooleanField() #alive? if not, dod field -- default FALSE
    dod = DateField(null=True) #date of death - default NULL
    direct_relation = CharField(null=True) #string
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


