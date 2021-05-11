from flask import Blueprint, render_template, request, flash, redirect, url_for, session
# from flask_login import login_required, current_user
from .models import User, Ops, assignee
from . import db


views = Blueprint('views', __name__)

def isLoggedIn():
	return ('user' in session)

@views.route('/') 
def home():
	for key, val in session.items():
		print(key, ' -> ', val)
	return render_template("home.html", user = session.get("user", None), roles = session.get('roles', None))

@views.route('/about') 
def about():
	return render_template("about.html", user = session.get("user", None), roles = session.get('roles', None))

@views.route('/ops')
def ops():
	if isLoggedIn():
		search = request.args.get('search')
		if search:
			posts = Ops.query.filter(Ops.title.contains(search) | Ops.data.contains(search)) 
		else:
			posts = Ops.query.all()
		return render_template("oppertunities.html", user = session.get("user", None), roles = session.get('roles', None), fulldata=posts)
	return redirect(url_for("views.home", user = session.get("user", None), roles = session.get('roles', None)))

@views.route('/op/<oppertunities>', methods=['GET', 'POST']) 
def op(oppertunities):
	if isLoggedIn():
		allOps = Ops.query.filter_by(ops_id = oppertunities).first_or_404()
		user = User.query.filter_by(id=session.get('user')).first()
		if request.method == 'POST':
			newop = Ops.query.filter_by(ops_id=oppertunities).first()
			for x in user.savedOps:
				if x == newop:
					flash("op already added")
					return render_template("ops.html", user = session.get("user", None), roles = session.get('roles', None), oppertunities = allOps)		
			user.savedOps.append(newop)
			db.session.commit()
			flash("success")
			return render_template("ops.html", user = session.get("user", None), roles = session.get('roles', None), oppertunities = allOps)
		return render_template("ops.html", user = session.get("user", None), roles = session.get('roles', None), oppertunities = allOps)
	return redirect(url_for("views.home", user = session.get("user", None), roles = session.get('roles', None)))


@views.route('/profile')
def profile():
	if isLoggedIn():
		userData = User.query.filter_by(id=session.get('user')).first()
		return render_template("profile.html", user = session.get("user", None), roles = session.get('roles', None), userData = userData)
	return redirect(url_for("views.home", user = session.get("user", None), roles = session.get('roles', None)))

@views.route('/deleteOp/<oppertunities>', methods=['GET','POST'])
def deleteOp(oppertunities):
	if isLoggedIn():
		userData = User.query.filter_by(id=session['user']).first()
		thisOp = Ops.query.filter_by(ops_id = oppertunities).first()
		userData.savedOps.remove(thisOp)
		db.session.commit()
		flash("success")
		return render_template("profile.html", user = session.get("user", None), roles = session.get('roles', None), userData = userData)
	return redirect(url_for("views.home", user = session.get("user", None), roles = session.get('roles', None)))

