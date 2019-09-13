from models.base_model import BaseModel
import peewee as pw
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from playhouse.hybrid import hybrid_property


class User(BaseModel, UserMixin):
    name = pw.CharField(unique=False, null=False)
    password = pw.CharField(null=False)
    email = pw.CharField(unique=True, null=False)
    role = pw.CharField(null=False)
    department = pw.CharField(null=False)
    profile_picture = pw.CharField(null=True)
    is_manager = pw.BooleanField(null=True)
    is_executive = pw.BooleanField(null=True)
    manager_id = pw.IntegerField(null=True)

