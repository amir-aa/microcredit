from peewee import *
from playhouse.pool import PooledMySQLDatabase
db = PooledMySQLDatabase('wallet',user='main', password='adl`',
                   host='localhost', port=3309,max_connections=8, stale_timeout=300,connect_timeout=100)

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