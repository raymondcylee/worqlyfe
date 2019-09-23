from flask import Blueprint, render_template, redirect, request, url_for, jsonify, flash
from models.user import User
from models.objective import Objective
from models.notification import Notification
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user

objectives_blueprint = Blueprint('objectives',
                                 __name__,
                                 template_folder='templates')


@objectives_blueprint.route('/<username>', methods=['POST'])
def create(username):
    user = User.get_or_none(User.name == username)
    obj = request.form.get("objective")
    Objective.create(objective=obj, user=user.id)
    if user.id != current_user.id:
        Notification.create(notification_type=1,
                            sender=current_user.id, recipient=user.id)
    flash("Objective succesfully added")
    return redirect(url_for('users.show', username=username))


@objectives_blueprint.route('/team')
def show():
    users = User.select().where(User.manager_id == current_user.id)
    return render_template('objectives/new.html', users=users)


@objectives_blueprint.route('/<id>/edit', methods=['GET'])
def edit(id):
    pass


@objectives_blueprint.route('/update/<id>', methods=['POST'])
def update(id):

    obj = Objective.get_by_id(id)

    if obj.done:
        Objective.update(done=False).where(Objective.id == obj.id).execute()
        progress = len(Objective.select().where((Objective.user_id == obj.user_id) & (Objective.done == True))) / (len(Objective.select().where((Objective.user_id ==
                                                                                                                                                 obj.user_id) & (Objective.done == True))) + len(Objective.select().where((Objective.user_id == obj.user_id) & (Objective.done == False))))
        progress_percentage = "{:.0%}".format(progress)

        response = {
            "success": True,
            "done": False,
            "progress": progress_percentage
        }

    else:
        Objective.update(done=True).where(Objective.id == obj.id).execute()
        progress = len(Objective.select().where((Objective.user_id == obj.user_id) & (Objective.done == True))) / (len(Objective.select().where((Objective.user_id ==
                                                                                                                                                 obj.user_id) & (Objective.done == True))) + len(Objective.select().where((Objective.user_id == obj.user_id) & (Objective.done == False))))
        progress_percentage = "{:.0%}".format(progress)
        response = {
            "success": True,
            "done": True,
            "progress": progress_percentage

        }
    return jsonify(response)


@objectives_blueprint.route('/delete/<id>', methods=['POST'])
def destroy(id):
    obj = Objective.get_by_id(id)

    Objective.delete().where(Objective.id == id).execute()

    progress = len(Objective.select().where((Objective.user_id == obj.user_id) & (Objective.done == True))) / (len(Objective.select().where((Objective.user_id ==
                                                                                                                                             obj.user_id) & (Objective.done == True))) + len(Objective.select().where((Objective.user_id == obj.user_id) & (Objective.done == False))))
    progress_percentage = "{:.0%}".format(progress)
    response = {
        "success": True,
        "progress": progress_percentage
    }

    return jsonify(response)
