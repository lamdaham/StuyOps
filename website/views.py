from flask import Blueprint, render_template
from flask_login import login_required, current_user

views = Blueprint('views', __name__)

@views.route('/')
def home():
	return render_template("home.html", user = current_user)

@views.route('/about')
def about():
	return render_template("about.html", user = current_user)

@views.route('/ops')
@login_required
def ops():
	return render_template("oppertunities.html", user=current_user)