from models.base_model import BaseModel
import peewee as pw
from models.user import User


class Objective(BaseModel):
    objective = pw.CharField(unique=False, null=False)
    user = pw.ForeignKeyField(User, backref="objectives")