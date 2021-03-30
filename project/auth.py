from flask import Blueprint, render_template, redirect, url_for, request,flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user
from .models import User
from . import db
from flask_login import login_user, logout_user, login_required
from flask_mail import Mail, Message
import uuid


auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        remember = True if request.form.get('remember') else False
        user = User.query.filter_by(email=email).first()
        # check if the user actually exists
        # take the user-supplied password, hash it, and compare it to the hashed password in the database
        if not user or not check_password_hash(user.password, password):
            flash('Please check your login details and try again.')
            return redirect(url_for('auth.login')) # if the user doesn't exist or password is wrong, reload the page

        # if the above check passes, then we know the user has the right credentials
        login_user(user, remember=remember)
        return redirect(url_for('main.dashboard'))
    return render_template('login.html')

@auth.route('/signup',methods=['GET','POST'])
def signup():
    if request.method == 'POST':
        email = request.form.get('email')
        name = request.form.get('name')
        password = request.form.get('password')
        user = User.query.filter_by(email=email).first() # if this returns a user, then the email already exists in database
        if user: # if a user is found, we want to redirect back to signup page so user can try again
            flash('Email address already exists')
            return redirect(url_for('auth.signup'))

        # create a new user with the form data. Hash the password so the plaintext version isn't saved.
        new_user = User(email=email, name=name, password=generate_password_hash(password, method='sha256'))

        # add the new user to the database
        db.session.add(new_user)
        db.session.commit()

        return redirect(url_for('auth.login'))

    return render_template('signup.html')

@auth.route('/changepassword',methods=['GET','POST'])
def changepassword():
    if request.method == 'POST':
        email = request.form.get('email')
        user = User.query.filter_by(email=email).first() # if this returns a user, then the email already exists in database
        if user: # if a user is found, we want to redirect back to signup page so user can try again
            # msg = Message('Hello', sender = 'testusr5055@gmail.com', recipients = [email])
            # msg.body = "This is the email body"
            # mail.send(msg)
            uniquecode = uuid.uuid4()
            flash('Functionality Work soon!!')
            # flash(f'Go to this link {uniquecode}')
        else:
            flash('Enter email no associated user.')
        # # create a new user with the form data. Hash the password so the plaintext version isn't saved.
        # new_user = User(email=email, name=name, password=generate_password_hash(password, method='sha256'))

        # # add the new user to the database
        # db.session.add(new_user)
        # db.session.commit()

        # return redirect(url_for('auth.login'))
    return render_template('changepassword.html')

# @auth.route('/forgetpassword',methods=['GET','POST'])
# def forgotpassword():
#     pass


@auth.route('/logout',methods=['GET','POST'])
@login_required
def logout():
    if request.method == "POST":
        logout_user()
        return redirect(url_for('main.index'))
    return render_template('logout.html')