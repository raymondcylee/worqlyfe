from __future__ import print_function
from flask import Blueprint, render_template, request, flash, redirect, url_for
from models.user import User
import os
from models.objective import Objective
from models.compliment import Compliment
from googleapiclient.discovery import build
import datetime
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

SCOPES = ['https://www.googleapis.com/auth/calendar']

dashboard_blueprint = Blueprint('dashboard',
                                __name__,
                                template_folder='templates')


@dashboard_blueprint.route('/')
def index():
    manager = User.get_or_none(
        (User.is_manager == True) & (User.is_executive == False))
    executive = User.get_or_none((User.is_manager == False) & (
        User.is_executive == True) & (User.id == 2))
    user = manager
    objective = Objective.select().where(Objective.user_id == user.id)
    compliments = Compliment.select()
    departments = User.select().where(User.department == 'Marketing')
    return render_template('dashboard/new.html', user=user, objectives=objective, compliments=compliments, departments=departments)


@dashboard_blueprint.route('/https://www.googleapis.com/calendar/v3/calendars/primary/events', methods=['POST'])
def create():
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
    create_event = service.events().insert(calendarId='primary', body=event).execute()
    if create_event:
        flash('Event created')
    else:
        flash('Failed')

    return redirect(url_for('dashboard.index'))


@dashboard_blueprint.route('/testing')
def test():
    return render_template('dashboard/testing.html')
