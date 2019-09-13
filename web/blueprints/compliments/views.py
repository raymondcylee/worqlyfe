from flask import Blueprint, render_template, flash, request, redirect, url_for
from flask_login import login_required, current_user
from models.user import User
from models.badge import Badge
from models.compliment import Compliment

compliments_blueprint = Blueprint('compliments',
                            __name__,template_folder='templates')


@compliments_blueprint.route('/new', methods=['GET'])
def new():
    users = User.select()
    badges = Badge.select()
    compliments = Compliment.select().order_by(Compliment.id.desc())
    return render_template('compliments/new.html', users=users, badges=badges, compliments=compliments)

@compliments_blueprint.route('/newcompliment', methods=['POST'])
def create():
    compliment_badge = request.form['badgeId']
    compliment_recipient = request.form['recipientList']
    compliment_comment = request.form['comment']
    new_compliment = Compliment(compliment=compliment_comment, sender_id=current_user.id, recipient_id=compliment_recipient, badge_id=compliment_badge)
    new_compliment.save()
    return redirect(url_for('compliments.new'))



