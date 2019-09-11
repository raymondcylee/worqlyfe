from models.base_model import BaseModel
import peewee as pw
from models.user import User


class Compliment(BaseModel):
    compliment = pw.CharField(unique=False, null=False)
    sender = pw.ForeignKeyField(User, backref='recipients')
    recipient = pw.ForeignKeyField(User, backref='senders')