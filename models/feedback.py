from models.base_model import BaseModel
from models.user import User
import peewee as pw
from playhouse.hybrid import hybrid_property


class Feedback(BaseModel):
    message = pw.CharField(null=False)
    subject = pw.CharField(null=False)
    answered = pw.BooleanField(null=False)
    requester = pw.ForeignKeyField(User, backref='receivers')
    receiver = pw.ForeignKeyField(User, backref='requesters') # current_user.requesters means we are looking for current_user == receiver


        