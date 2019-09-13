from models.base_model import BaseModel
from models.user import User
from models.badge import Badge
import peewee as pw


class Compliment(BaseModel):
    compliment = pw.CharField(unique=False, null=False)
    sender = pw.ForeignKeyField(User, backref='recipients')
    recipient = pw.ForeignKeyField(User, backref='senders')
    badge = pw.ForeignKeyField(Badge, backref='badge')

