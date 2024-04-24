from peewee import *

db = MySQLDatabase('wallet',user='main', password='adl@p144',
                   host='localhost', port=3309)

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
def init():
    db.create_tables([Wallet,Transaction],safe=True)

init()