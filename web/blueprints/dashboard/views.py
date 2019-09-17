from __future__ import print_function
from flask import Blueprint, render_template, request, flash, redirect, url_for, jsonify
from models.user import User
import os
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from models.user import User
from models.objective import Objective
from models.compliment import Compliment
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from models.medal import Medal



dashboard_blueprint = Blueprint('dashboard',
                                __name__,
                                template_folder='templates')


@dashboard_blueprint.route('/<id>')
def index(id):
    objective = Objective.select().where(Objective.user_id == current_user.id)
    compliments = Compliment.select()
    departments = User.select().where(User.department == current_user.department)
    all_users = User.select()
    compliments_received = Compliment.select().where(Compliment.recipient_id == current_user.id).count()
    compliments_given = Compliment.select().where(Compliment.sender_id == current_user.id).count()
    user = User.get_or_none(User.id == id)
    star = Medal.select().where(Medal.medal_caption == "Star").get()
    gold = Medal.select().where(Medal.medal_caption == "Gold").get()
    silver = Medal.select().where(Medal.medal_caption == "Silver").get()
    bronze = Medal.select().where(Medal.medal_caption == "Bronze").get()
    
    completed_objectives = Objective.select().where((Objective.user_id == user.id) & (Objective.done == True))
    incomplete_objectives = Objective.select().where((Objective.user_id == user.id) & (Objective.done == False))
    try:
        progress = (completed_objectives.count()/(completed_objectives.count()+incomplete_objectives.count()))
    except ZeroDivisionError:
        progress = 0
    progress_percentage = "{:.0%}".format(progress)

    return render_template('dashboard/new.html', objectives=objective, compliments=compliments, departments=departments, ,all_users=all_users, user=user, progress_percentage=progress_percentage, progress=progress, compliments_received=compliments_received, compliments_given=compliments_given, gold=gold, silver=silver, bronze=bronze, star=star)


@dashboard_blueprint.route('/feedback/<id>', methods=['POST'])
def feedback(id):
    recipient = User.get_by_id(id)

    message = Mail(
        from_email='worqlyfe@example.com',
        to_emails=recipient.email,
        subject='Feedback Form Notification',
        html_content=current_user.name + ' sent you a feedback form.')
    try:
        sg = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))
        response = sg.send(message)
        print(response.status_code)
        print(response.body)
        print(response.headers)
    except Exception as e:
        print(str(e))

    resp = {
        'success': True
    }
    return jsonify(resp)


@dashboard_blueprint.route('/upload', methods=['POST'])
def upload():
    file = request.files.get('user_image')
    try:

        s3.upload_fileobj(
            file,
            app.config['S3_BUCKET'],
            file.filename,
            ExtraArgs={
                "ACL": "public-read",
                "ContentType": file.content_type
            }
        )

        User.update(profile_picture=file.filename).where(
            User.id == current_user.id).execute()

    except Exception as e:
        flash(str(e))

    return redirect(url_for('dashboard.index'))
