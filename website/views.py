from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from .models import Ops, assignee
from . import db


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

@views.route('/op/<oppertunities>', methods=['GET', 'POST'])
@login_required  
def op(oppertunities):
	print(current_user.savedOps)
	allOps = Ops.query.filter_by(ops_id = oppertunities).first_or_404()
	if request.method == 'POST':
		newop = Ops.query.filter_by(ops_id=oppertunities).first()
		for x in current_user.savedOps:
			if x == newop:
				flash("op already added")
				return render_template("ops.html", user = current_user, oppertunities = allOps)		
		current_user.savedOps.append(newop)
		db.session.commit()
		flash("success")
		return render_template("ops.html", user = current_user, oppertunities = allOps)		
	return render_template("ops.html", user = current_user, oppertunities = allOps)


@views.route('/profile')
@login_required
def profile():
	return render_template("profile.html", user = current_user)


@views.route('/deleteOp/<oppertunities>', methods=['GET','POST'])
@login_required
def deleteOp(oppertunities):
	print(current_user.savedOps)
	thisOp = Ops.query.filter_by(ops_id = oppertunities).first()
	current_user.savedOps.remove(thisOp)
	db.session.commit()
	flash("success")
	return render_template("profile.html", user = current_user)