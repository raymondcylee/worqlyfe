from models.base_model import BaseModel
import peewee as pw

class Badge(BaseModel):
    badge = pw.CharField(null=False)
    badge_caption = pw.CharField(null=False)