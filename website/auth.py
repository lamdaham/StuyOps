from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, login_required, logout_user, current_user



auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
	if (current_user.is_authenticated):
		return redirect(url_for('views.home'))
	if request.method == 'POST':
		email = request.form.get('email')
		password = request.form.get('password')
		user = User.query.filter_by(email=email).first()
		if user:
			if check_password_hash(user.password, password):
				flash('logged in successfully', category = 'success')
				login_user(user, remember=True)
				return redirect(url_for('views.home'))
			else:
				flash('incorrect password', category = 'error')
		else:
			flash('email does not exist', category = 'error')
	data = request.form
	print(data)
	return render_template("login.html", user = current_user)

@auth.route('/logout')
@login_required
def logout():
	logout_user()
	return redirect(url_for('auth.login'))

@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
	if request.method == 'POST':
		email = request.form.get('email')
		first_name = request.form.get('firstName')
		password1 = request.form.get('password1')
		password2 = request.form.get('password2')
		roles = request.form.get('roles')
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
			login_user(new_user, remember=True)
			return redirect(url_for('views.home'))

	return render_template("sign_up.html", user = current_user)


@auth.route('/post_ops', methods=['GET', 'POST'])
@login_required
def post_ops(): 
	flash(current_user.roles)
	if request.method == 'POST':
		title = request.form.get('title')
		deadline = request.form.get('deadline')		
		return redirect(url_for('views.home'))
	return render_template("post_ops.html", user = current_user)
		



