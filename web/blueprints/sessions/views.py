from flask import Blueprint, render_template, redirect, request, url_for, jsonify
from models.user import User
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user

sessions_blueprint = Blueprint('sessions',
                               __name__,
                               template_folder='templates')


@sessions_blueprint.route('/new', methods=['GET'])
def new():
    # jsonify({
    #     'success': True,
    # })
    return render_template('sessions/new.html')


@sessions_blueprint.route('/', methods=['POST'])
def create():
    email = request.form.get('email')
    password = request.form.get('password')

    user = User.get_or_none(User.email == email)



    if user and (user.password == password):
        print("LOGIN SUCCESFULLY")

        login_user(user)

        # login_user(user)
        # session["user_id"] = user.id
        # session["username"] = user.username
        return redirect(url_for('users.show', username=user.name))
    else:
        print("NOT LOGIN")
        return redirect(url_for('users.show', username=user.name))
