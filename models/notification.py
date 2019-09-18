from models.base_model import BaseModel
from models.user import User
import peewee as pw
import re
from flask_login import LoginManager, UserMixin
from playhouse.hybrid import hybrid_property


class Notification(BaseModel):
    notification_type = pw.IntegerField(null=False)
    sender = pw.ForeignKeyField(User, backref="notification_recipients")
    recipient = pw.ForeignKeyField(User, backref="notification_senders")
    read = pw.BooleanField(default=False)
