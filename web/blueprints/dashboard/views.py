from __future__ import print_function
from flask import Blueprint, render_template, request, flash, redirect, url_for
from models.user import User
import os
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from models.objective import Objective
from models.compliment import Compliment



dashboard_blueprint = Blueprint('dashboard',
                                __name__,
                                template_folder='templates')


@dashboard_blueprint.route('/')
def index():
    objective = Objective.select().where(Objective.user_id == current_user.id)
    compliments = Compliment.select()
    departments = User.select().where(User.department == current_user.department)
    return render_template('dashboard/new.html', objectives=objective, compliments=compliments, departments=departments)


