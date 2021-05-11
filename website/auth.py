from flask import Blueprint, render_template, request, flash, redirect, url_for, session
from .models import User, Ops
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
# from flask_login import login_user, login_required, logout_user, current_user
from datetime import datetime
from authlib.integrations.flask_client import OAuth
from . import lis
import os



auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
	if ('user' in session):
		return redirect(url_for('views.home'))
	if request.method == 'POST':
		email = request.form.get('email')
		password = request.form.get('password')
		user = User.query.filter_by(email=email).first()
		if user:
			if check_password_hash(user.password, password):
				flash('logged in successfully', category = 'success')
				session['user'] = user.id
				session['roles'] = user.roles
				return render_template("home.html", user = session.get("user", None), roles = session.get('roles', None))
			else:
				flash('incorrect password', category = 'error')
		else:
			flash('email does not exist', category = 'error')
	data = request.form
	print(data)
	return render_template("login.html", user = session.get("user", None), roles = session.get('roles', None))

@auth.route('/logout')
def logout():  
	session.pop('user', None)
	session.pop('roles', None)
	return redirect(url_for('views.home'))

@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
	if request.method == 'POST':
		email = request.form.get('email')
		first_name = request.form.get('firstName')
		password1 = request.form.get('password1')
		password2 = request.form.get('password2')
		roles = 'admin'
		user = User.query.filter_by(email=email).first()
		if user:
			flash('Email already exist', category='error')
		elif len(email) < 4:
			flash('email is too short', category='error')
		elif len(first_name)<2:
			flash('firstName is too short', category='error')
		elif password1 != password2:
			flash('password aint match', category='error')
		elif len(password1) < 7:
			flash('password too short', category='error')
		else:
			new_user = User(email=email, first_name=first_name, password=generate_password_hash(password1, method='sha256'), roles = roles)
			db.session.add(new_user)
			db.session.commit()
			flash('success', category='success')
			session['user'] = new_user.id
			session['roles'] = new_user.roles
			return render_template("home.html", user = session.get("user", None), roles = session.get('roles', None))

	return render_template("sign_up.html", user = session.get("user", None), roles = session.get('roles', None))


@auth.route('/post_ops', methods=['GET', 'POST'])
def post_ops(): 
	user = User.query.filter_by(id=session['user']).first()
	if user.roles != "admin":
		return redirect(url_for('views.home'))
	if request.method == 'POST':
		title = request.form.get('title')
		deadline = request.form.get('deadline')
		data = request.form.get('data')
		url = request.form.get('url')
		if len(title)<1:
			flash('Please enter title')
		elif len(deadline)<1:
			flash('Please enter deadline')
		elif len(data)<1:
			flash('Please enter information')
		elif len(url)<1:
			flash('Please enter url')
		else:
			date = datetime(int(deadline[0:4]), int(deadline[5:7]), int(deadline[8:]), 23, 59, 59)
			new_op = Ops(title=title, date = date, data = data, url = url)
			db.session.add(new_op)
			db.session.commit()
			flash('success')
			return render_template("oppertunities.html", user = session.get("user", None), roles = session.get('roles', None))
	return render_template("post_ops.html", user = session.get("user", None), roles = session.get('roles', None))

@auth.route('/glogin')
def glogin():
	print(lis[0])
	google = lis[0].create_client('google')  # create the google lis[0] client
	redirect_uri = url_for('auth.authorize', _external=True)
	return google.authorize_redirect(redirect_uri)

@auth.route('/authorize')
def authorize():
    google = lis[0].create_client('google')  # create the google lis[0] client
    token = google.authorize_access_token()  # Access token from google (needed to get user info)
    resp = google.get('userinfo')  # userinfo contains stuff u specificed in the scrope
    user_info = resp.json()
    user = lis[0].google.userinfo()  # uses openid endpoint to fetch user info
    # Here you use the profile/user data that you got and query your database find/register the user
    # and set ur own data in the session not the profile from google
    userlist = User.query.filter_by(googleID=user_info.get('id')).first()
    if userlist:
    	session['user'] = userlist.id
    	session['roles'] = userlist.roles
    else:
    	new_user = User(googleID=user_info.get("id"), email=user_info.get("email"), password = generate_password_hash(user_info.get("id"), method='sha256'),first_name=user_info.get("given_name"), roles = "student")
    	db.session.add(new_user)
    	db.session.commit()
    	session['user'] = new_user.id
    	session['roles'] = new_user.roles
    # session['profile'] = user_info
    
    session.permanent = True  # make the session permanant so it keeps existing after broweser gets closed
    return render_template("home.html", user = session.get("user", None), roles = session.get('roles', None))

