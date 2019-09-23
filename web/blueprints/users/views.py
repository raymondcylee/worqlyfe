from __future__ import print_function
from flask import Blueprint, render_template, redirect, request, jsonify, url_for, flash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from models.user import User
from models.review import Review
from models.compliment import Compliment
from models.objective import Objective
from models.notification import Notification
from models.medal import Medal
from googleapiclient.discovery import build
import os
import datetime
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

SCOPES = ['https://www.googleapis.com/auth/calendar']

users_blueprint = Blueprint('users',
                            __name__,
                            template_folder='templates')


@users_blueprint.route('/new', methods=['GET'])
def new():
    return render_template('users/new.html')


@users_blueprint.route('/', methods=['POST'])
def create():
    name = request.form.get('name').strip()
    email = request.form.get('email').strip()
    password = request.form.get('password')
    confirmPassword = request.form.get('confirmPassword')
    role = request.form.get('role').strip()
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


@users_blueprint.route('/logout', methods=["POST"])
def destroy():
    logout_user()
    return redirect('/')


@users_blueprint.route('/<username>', methods=["GET"])
def show(username):
    user = User.get_or_none(User.name == username)
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

    if user:
        return render_template("users/profile.html", user=user, star=star, gold=gold, silver=silver, bronze=bronze, completed_objectives=completed_objectives, incomplete_objectives=incomplete_objectives, progress=progress, progress_percentage=progress_percentage)


@users_blueprint.route('/', methods=["GET"])
def index():
    return "USERS"


@users_blueprint.route('/<id>/edit', methods=['GET'])
def edit(id):
    pass


@users_blueprint.route('/notification', methods=['POST'])
def update():
    Notification.update(read=True).where(
        Notification.recipient_id == current_user.id).execute()
    response = {
        "success": True,
        "read": True
    }
    return jsonify(response)


@users_blueprint.route('/department/<department>', methods=['GET'])
def department(department):
    # users = User.select().where(User.department == department, User.is_manager == True)

    # for user in users:
    #     print(user.name)
    print([user.name for user in User.select().where(
        User.department == department, User.is_manager == True)])
    return jsonify([user.name for user in User.select().where(User.department == department, User.is_manager == True)])


@users_blueprint.route('/review/<id>', methods=['GET'])
def show_review(id):
    user = User.get_or_none(User.id == id)
    star = Medal.select().where(Medal.medal_caption == "Star").get()
    gold = Medal.select().where(Medal.medal_caption == "Gold").get()
    silver = Medal.select().where(Medal.medal_caption == "Silver").get()
    bronze = Medal.select().where(Medal.medal_caption == "Bronze").get()
    manager = User.get_or_none(User.id == user.manager_id)
    completed_objectives = Objective.select().where(
        (Objective.user_id == user.id) & (Objective.done == True))
    incomplete_objectives = Objective.select().where(
        (Objective.user_id == user.id) & (Objective.done == False))
    try:
        progress = (completed_objectives.count() /
                    (completed_objectives.count()+incomplete_objectives.count()))
    except ZeroDivisionError:
        progress = 0
    progress_percentage = "{:.0%}".format(progress)
    executive_notes = Review.select().where((Review.executive_id == user.id)
                                            & (Review.executive_notes.is_null(False)))
    manager_notes = Review.select().where((Review.executive_id == user.id)
                                          & (Review.manager_notes.is_null(False)))
    return render_template('users/review.html', user=user, manager=manager, star=star, gold=gold, silver=silver, bronze=bronze, executive_notes=executive_notes, manager_notes=manager_notes, completed_objectives=completed_objectives, incomplete_objectives=incomplete_objectives, progress_percentage=progress_percentage)


@users_blueprint.route('/create-manager-review/<id>', methods=['POST'])
def create_manager_notes(id):
    user = User.get_or_none(User.id == id)
    manager = User.get_or_none(User.id == user.manager_id)
    comments = request.form.get("manager_notes")
    review_date = request.form.get("review_date")
    Review(manager_notes=comments, executive_id=user.id,
           review_date=review_date).save()
    if user.id != current_user.id:
        Notification(notification_type=4, sender=current_user.id, recipient=user.id).save()
        flash("Manager commment added")
    return redirect(url_for('users.show_review', user=user, manager=manager, id=user.id))


@users_blueprint.route('/create-my-notes/<id>', methods=['POST'])
def create_my_notes(id):
    user = User.get_or_none(User.id == id)
    manager = User.get_or_none(User.id == user.manager_id)
    comments = request.form.get("my_notes")
    review_date = request.form.get("review_date")
    Review(executive_notes=comments, executive_id=user.id,
           review_date=review_date).save()
    flash("My note added")
    return redirect(url_for('users.show_review', user=user, manager=manager, id=user.id))

@users_blueprint.route('/delete-comment/<id>',methods=['POST'])
def destroy_comment(id):
    selected_review = Review.get_by_id(id)
    Review.delete().where(Review.id == id).execute()
    response = {
        "status": "success"
    }
    return jsonify(response)
    # return redirect(url_for('users.show_review', id=selected_review.executive_id))



@users_blueprint.route('/https://www.googleapis.com/calendar/v3/calendars/primary/events/<username>', methods=['POST'])
def calender(username):
    creds = None

    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('calendar', 'v3', credentials=creds)
    title = request.form.get('event-title')
    description = request.form.get('event-details')
    startdatetime = request.form.get('startdaytime')
    enddatetime = request.form.get('enddaytime')
    GMT_OFF = '+08:00'
    event = {
        'summary': title,
        'description': description,
        'start': {
            'dateTime': startdatetime + ':00' + GMT_OFF
        },
        'end': {
            'dateTime': enddatetime + ':00' + GMT_OFF
        }}
    create_event = service.events().insert(
        calendarId='primary', body=event).execute()
    if create_event:
        flash('Event created')
    else:
        flash('Failed')

    return redirect(url_for('users.show', username=username))

@users_blueprint.route('/feed', methods=["GET"])
def show_feed():
    users = User.select()
    star = Medal.select().where(Medal.medal_caption == "Star").get()
    gold = Medal.select().where(Medal.medal_caption == "Gold").get()
    silver = Medal.select().where(Medal.medal_caption == "Silver").get()
    bronze = Medal.select().where(Medal.medal_caption == "Bronze").get()
    
    return render_template('users/feed.html', users=users, star=star, gold=gold, silver=silver, bronze=bronze)