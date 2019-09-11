from models.base_model import BaseModel
import peewee as pw


class User(BaseModel):
    name = pw.CharField(unique=False, null=False)
    email = pw.CharField(unique=True, null=False)
    password = pw.CharField(null=False)
    role = pw.CharField(null=False)
    department = pw.CharField(null=False)
    profile_picture = pw.CharField(null=True)
    is_manager = pw.BooleanField(null=True)
    is_executive = pw.BooleanField(null=True)
    manager_id = pw.IntegerField(null=True)