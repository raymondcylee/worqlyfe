from __future__ import print_function
from flask import Blueprint, render_template, request, flash, redirect, url_for, jsonify
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from models.user import User
from models.feedback import Feedback
from models.replies import Replies
from models.objective import Objective
from models.compliment import Compliment
from models.medal import Medal
from models.user import User
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from app import s3, app
import os



dashboard_blueprint = Blueprint('dashboard',
                                __name__,
                                template_folder='templates')


@dashboard_blueprint.route('/')
def index():
    objective = Objective.select().where(Objective.user_id == current_user.id)
    compliments = Compliment.select()
    departments = User.select().where(User.department == current_user.department)
    all_users = User.select()
    compliments_received = Compliment.select().where(Compliment.recipient_id == current_user.id).count()
    compliments_given = Compliment.select().where(Compliment.sender_id == current_user.id).count()
    user = User.get_or_none(User.id == current_user.id)
    feedback_exist = Feedback.select().where((Feedback.receiver_id == current_user.id) & (Feedback.answered == False))
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

    return render_template('dashboard/new.html', objectives=objective, compliments=compliments, departments=departments ,all_users=all_users, user=user, progress_percentage=progress_percentage, progress=progress, compliments_received=compliments_received, compliments_given=compliments_given, gold=gold, silver=silver, bronze=bronze, star=star, feedback_exist=feedback_exist)



@dashboard_blueprint.route('/feedback/<id>', methods=['POST'])
def feedback(id):
    recipient = User.get_by_id(id)
    
    feedback_subject = request.form.get('formSubject')
    feedback_message = request.form.get('formMessage')
    
    Feedback(subject=feedback_subject,message=feedback_message,requester_id=current_user.id,receiver_id=recipient.id,answered=False).save()

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
@dashboard_blueprint.route('/message/<id>')
def message(id):
    get_message = Feedback.get_by_id(id)
    if get_message:
        return jsonify(get_message.message)
    else:
        return False


@dashboard_blueprint.route('/replies/<id>', methods=["POST"])
def reply(id):
    reply_message = request.form.get('formReply')
    Feedback.update(answered=True).where(Feedback.id == id).execute()
    Replies(reply_message=reply_message,feedback_replied_id=id).save()
    any_feedback_left = False
    feedback_exist = Feedback.select().where((Feedback.receiver_id == current_user.id) & (Feedback.answered == False))
    if feedback_exist:
        any_feedback_left = True

    resp = {
        'success': True,
        'any_feedback_left': any_feedback_left
    }
    return jsonify(resp)
