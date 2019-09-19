from models.base_model import BaseModel
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from playhouse.hybrid import hybrid_property
import peewee as pw


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


    @hybrid_property
    def progress(self):
        from models.objective import Objective
        trueprogress = len([obj for obj in Objective.select().where(
            (Objective.user_id == self.id) & (Objective.done == True))])

        falseprogress = len([obj for obj in Objective.select().where(
        (Objective.user_id == self.id) & (Objective.done == False))])
        try:
            ppprogress = trueprogress/(trueprogress+falseprogress)
        except ZeroDivisionError:
            ppprogress = 0

        return ppprogress


    # @hybrid_property
    # def incomplete_progress(self):
    #     from models.objective import Objective
    #     progress = len([obj for obj in Objective.select().where(
    #         (Objective.user_id == self.id) & (Objective.done == False))])

    #     if progress == 0:
    #         break

    #     return progress

    # @hybrid_property
    # def complete_progress(self):
    #     from models.objective import Objective
    #     progress = len([obj for obj in Objective.select().where(
    #         (Objective.user_id == self.id) & (Objective.done == True))])

    #     if progress == 0:
    #         break

    #     return progress

    @hybrid_property
    def my_replies(self):
        from models.replies import Replies
        from models.feedback import Feedback
        return Replies.select().join(Feedback).where(Feedback.requester_id == self.id)

    @hybrid_property
    def profile_image(self):
        from app import app
        if self.profile_picture:
            return f"{app.config['S3_LOCATION']}" + self.profile_picture
        else:
            return "https://api.adorable.io/avatars/285/abott@adorable.png"

    @hybrid_property
    def completed_objective(self):
        from models.objective import Objective
        return [obs for obs in Objective.select().where((Objective.user_id == self.id) & (Objective.done == True)).order_by(Objective.id.desc())]

    @hybrid_property
    def incomplete_objective(self):
        from models.objective import Objective
        return [obs for obs in Objective.select().where((Objective.user_id == self.id) & (Objective.done == False)).order_by(Objective.id.asc())]

    # @hybrid_property
    # def all_requesters(self):
    #     from models.feedback import Feedback
    #     requesters_ids = [feedback.requester_id for feedback in current_user.requesters]
    #     if requesters_ids:
    #         return [user for user in User.select().where(User.id << requesters_ids)]
    #     else:
    #         return False

    # @hybrid_property
    # def all_receivers(self):
    #     from models.feedback import Feedback
    #     receivers_ids = [feedback.receiver_id for feedback in current_user.receivers]
    #     return [user for user in User.select().where(User.id << receivers_ids)]

    @hybrid_property
    def unread_notification(self):
        from models.notification import Notification
        return [notifications for notifications in Notification.select().where((Notification.recipient_id == self.id) & (Notification.read == False))]

    @hybrid_property
    def sorted_notification(self):
        from models.notification import Notification
        return [notifications for notifications in Notification.select().where((Notification.recipient_id == self.id)).order_by(Notification.id.desc()).limit(5)]
