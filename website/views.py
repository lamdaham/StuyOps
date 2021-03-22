from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from .models import Ops


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
	search = request.args.get('search')
	if search:
		posts = Ops.query.filter(Ops.title.contains(search) | Ops.data.contains(search)) 
	else:
		posts = Ops.query.all()
	return render_template("oppertunities.html", user=current_user, fulldata=posts)

@views.route('/op/<oppertunities>')
@login_required  
def op(oppertunities):
	print("k") 
	allOps = Ops.query.filter_by(id = oppertunities).first_or_404()
	return render_template("ops.html", user = current_user, oppertunities = allOps)