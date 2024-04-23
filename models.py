from peewee import *

db = SqliteDatabase('wallet.db')

class BaseModel(Model):
    class Meta:
        database = db

class Wallet(BaseModel):
    username = CharField(unique=True)
    balance = FloatField(default=0.0)

class Transaction(BaseModel):
    wallet = ForeignKeyField(Wallet, backref='transactions')
    description = TextField()
    amount = FloatField()
    timestamp = DateTimeField()
