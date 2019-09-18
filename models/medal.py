from models.base_model import BaseModel
import peewee as pw

class Medal(BaseModel):
    medal = pw.CharField(null=False)
    medal_caption = pw.CharField(null=False)