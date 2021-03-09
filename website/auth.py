from flask import Blueprint, render_template, request, flash

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
	data = request.form
	print(data)
	return render_template("login.html")

@auth.route('/logout')
def logout():
	return "<p>logout</p>"

@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
	if request.method == 'POST':
		email = request.form.get('email')
		firstName = request.form.get('firstName')
		password1 = request.form.get('password1')
		password2 = request.form.get('password2')

		if len(email) < 4:
			flash('email is too short')
		elif len(firstName)<2:
			flash('firstName is too short', category='error')
		elif password1 != password2:
			flash('password aint match', category='error')
		elif len(password1) < 7:
			flash('password too short', category='error')
		else:
			flash('success', category='success')

	return render_template("sign_up.html")