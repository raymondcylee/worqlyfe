from app import app
from flask import render_template
from web.blueprints.users.views import users_blueprint
from web.blueprints.sessions.views import sessions_blueprint
from web.blueprints.compliments.views import compliments_blueprint
from web.blueprints.dashboard.views import dashboard_blueprint
from web.blueprints.objectives.views import objectives_blueprint
# from web.blueprints.notifications.views import notifications_blueprint
from flask_assets import Environment, Bundle
from .util.assets import bundles

assets = Environment(app)
assets.register(bundles)

app.register_blueprint(users_blueprint, url_prefix="/users")
app.register_blueprint(sessions_blueprint, url_prefix="/sessions")
app.register_blueprint(compliments_blueprint, url_prefix="/compliments")
app.register_blueprint(dashboard_blueprint, url_prefix="/dashboard")
app.register_blueprint(objectives_blueprint, url_prefix="/objectives")
# app.register_blueprint(notifications_blueprint, url_prefix="/notifications")


@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500


@app.route("/")
def home():
    return render_template('home.html')
