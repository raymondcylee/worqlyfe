from models.base_model import BaseModel
import peewee as pw
from models.user import User


class Review(BaseModel):
    manager_notes = pw.CharField(unique=False, null=False)
    executive_notes = pw.CharField(unique=False, null=False)
    review_date = pw.DateTimeField(null=True)
    executive = pw.ForeignKeyField(User, backref="reviews")