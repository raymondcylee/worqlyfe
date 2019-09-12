from flask import Blueprint, render_template, redirect, request, jsonify
from models.user import User
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user


users_blueprint = Blueprint('users',
                            __name__,
                            template_folder='templates')


@users_blueprint.route('/new', methods=['GET'])
def new():
    return render_template('users/new.html')


@users_blueprint.route('/', methods=['POST'])
def create():
    name = request.form.get('name')
    email = request.form.get('email')
    password = request.form.get('password')
    confirmPassword = request.form.get('confirmPassword')
    role = request.form.get('role')
    department = request.form.get('department')
    is_manager = request.form.get('isManager')
    is_executive = request.form.get('isExecutive')
    manager = User.get_or_none(User.name == request.form.get('manager'))

    if password == confirmPassword:
        user = User(name=name, email=email,
                    password=password, role=role, department=department,
                    is_manager=is_manager, is_executive=is_executive,
                    manager_id=manager.id if manager else None)
        if user.save():
            login_user(user)
            return redirect('/')
    return redirect('/')
    #     if create_user.save():
    #         flash(f'User profile: {username} succesfully created!')
    #         # return redirect(url_for('users.new'))
    #         return redirect(url_for('users.show', username=username))
    #     return render_template("users/new.html", errors=create_user.errors)
    # return render_template("users/new.html", errors=["Password and confirm password doesn't match"])


@users_blueprint.route('/<username>', methods=["GET"])
def show(username):
    return "<h1>You are login</h1>"


@users_blueprint.route('/', methods=["GET"])
def index():
    return "USERS"


@users_blueprint.route('/<id>/edit', methods=['GET'])
def edit(id):
    pass


@users_blueprint.route('/<id>', methods=['POST'])
def update(id):
    pass


@users_blueprint.route('/department/<department>', methods=['GET'])
def department(department):
    # users = User.select().where(User.department == department, User.is_manager == True)

    # for user in users:
    #     print(user.name)
    print([user.name for user in User.select().where(
        User.department == department, User.is_manager == True)])
    return jsonify([user.name for user in User.select().where(User.department == department, User.is_manager == True)])
