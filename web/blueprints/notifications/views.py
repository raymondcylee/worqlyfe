from __future__ import print_function
from flask import Blueprint, render_template, request, flash, redirect, url_for, jsonify
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from models.user import User
from models.objective import Objective
from models.compliment import Compliment
from models.notification import Notification
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from app import app, s3
import os

notification_blueprint = Blueprint('notification',
                                   __name__,
                                   template_folder='templates')


@notification_blueprint.route('/')
def show():
    pass
