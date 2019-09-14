from flask import Blueprint, render_template, redirect, request, url_for, jsonify
from models.user import User
from models.objective import Objective
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user

objectives_blueprint = Blueprint('objectives',
                                 __name__,
                                 template_folder='templates')


@objectives_blueprint.route('/<username>', methods=['POST'])
def create(username):
    user = User.get_or_none(User.name == username)
    obj = request.form.get("objective")
    Objective.create(objective=obj, user=user.id)
    return redirect(url_for('users.show', username=username))


@objectives_blueprint.route('/<id>/edit', methods=['GET'])
def edit(id):
    pass


@objectives_blueprint.route('/<id>', methods=['POST'])
def update(id):

    obj = Objective.get_by_id(id)

    if obj.done:
        Objective.update(done=False).where(Objective.id == obj.id).execute()
        response = {
            "sucess": True,
            "done": False

        }
    else:
        Objective.update(done=True).where(Objective.id == obj.id).execute()
        response = {
            "sucess": True,
            "done": True

        }
    return jsonify(response)
