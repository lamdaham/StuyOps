from flask import Flask
from flask import Blueprint, render_template, request, flash, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager, current_user
from flask_admin import Admin, AdminIndexView
from flask_admin.contrib.sqla import ModelView
from authlib.integrations.flask_client import OAuth




db = SQLAlchemy()
DB_NAME = "database.db"

lis = []

def create_app():
    app = Flask(__name__)
    oauth = OAuth(app)
    google = oauth.register(
        name='google',
        client_id="325251149202-casc1vpu9726i40ss0nipbp556fivl7r.apps.googleusercontent.com",
        client_secret="pGp33QdlfNv1k3uR2aPmOoao",
        access_token_url='https://accounts.google.com/o/oauth2/token',
        access_token_params=None,
        authorize_url='https://accounts.google.com/o/oauth2/auth',
        authorize_params=None,
        api_base_url='https://www.googleapis.com/oauth2/v1/',
        userinfo_endpoint='https://openidconnect.googleapis.com/v1/userinfo',  # This is only needed if using openId to fetch user info
        client_kwargs={'scope': 'openid email profile'},
    )

    lis.append(oauth)

    app.config['SECRET_KEY'] = 'hjshjhdjah kjshkjdhjs'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    db.init_app(app)

    
    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    from .models import User, Ops

    create_database(app)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
    	return User.query.get(int(id))

    class MyModelView(ModelView):
        def is_accessible(self):
            return (session['roles'] == "admin")

        def inaccessible_callback(self, name, *kwargs):
            return redirect(url_for('views.home'))

    class MyAdminIndexView(AdminIndexView):
        def is_accessible(self):
            return (session['roles'] == "admin")
            

    admin = Admin(app, index_view = MyAdminIndexView())
    admin.add_view(MyModelView(User, db.session))
    admin.add_view(MyModelView(Ops, db.session))


    return app


def create_database(app):
    if not path.exists('website/' + DB_NAME):
        db.create_all(app=app)
        print('Created Database!')