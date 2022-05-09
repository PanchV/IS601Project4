from flask import Blueprint, render_template, redirect, url_for, flash,current_app, request
from flask_login import login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash

from app.auth.decorators import admin_required
from app.auth.forms import login_form, register_form, profile_form, security_form, user_edit_form
from app.db import db
from app.db.models import User

import logging

auth = Blueprint('auth', __name__, template_folder='templates')


@auth.route('/register', methods=['POST', 'GET'])
def register():
    log1 = logging.getLogger("info.log")
    log1.info("register inside")
    if current_user.is_authenticated:
        return redirect(url_for('auth.dashboard'))
    form = register_form()
    if form.validate_on_submit():
        email = request.form.get('email')
        password = request.form.get('password')
        user = User.query.filter_by(email=email).first()
        #if user is registered previously, request to create with different account details.
        if user:
            flash('Found an Already Registered Account. Please Try Again with Different Email')
            return redirect(url_for('auth.register'), 302)
        #create a new user and add it to the database
        new_user = User(email=email, password=generate_password_hash(password))
        db.session.add(new_user)
        db.session.commit()
        if new_user.id == 1:
            new_user.is_admin = 1
            db.session.add(new_user)
            db.session.commit()
        flash('Congratulations, Your Account is Registered and Ready for Login', "success")
        return redirect(url_for('auth.login'), 302)
    return render_template('register.html', form=form)


@auth.route('/login', methods=['POST', 'GET'])
def login():
    #log = logging.getLogger("eachRequestResponse")
    #log.info("user login ")
    form = login_form()
    if current_user.is_authenticated:
        #log.info("user is authenticated")
        return redirect(url_for('auth.dashboard'))
    if form.validate_on_submit():
        #log.info("user validate on submit")
        email = request.form.get('email')
        password = request.form.get('password')
        user = User.query.filter_by(email=email).first()
        if not user or not user.check_password(password):
            #log.info("Invalid username or password mistake")
            flash('Invalid username or password. Please check your login details and try again.')
            return redirect(url_for('auth.login'))
        #log.info("user is authenticated")
        user.authenticated = True
        user.active = 1
        db.session.add(user)
        db.session.commit()
        login_user(user)
        flash("Welcome to your Dashboard", 'success')
        return redirect(url_for('auth.dashboard'))
    return render_template('login.html', title='Sign In', form=form)


@auth.route("/logout")
@login_required
def logout():
    """Logout the current user."""
    #log = logging.getLogger("eachRequestResponse")
    #log.info("user logout()")
    user = current_user
    user.active = 0
    user.authenticated = False
    db.session.add(user)
    db.session.commit()
    logout_user()
    flash("You Logged Out Successfully!", 'success')
    return redirect(url_for('simple_pages.index'))



@auth.route('/dashboard')
@login_required
def dashboard():
    #log = logging.getLogger("eachRequestResponse")
    #log.info("user dashboard")
    return render_template('dashboard.html')


@auth.route('/profile', methods=['POST', 'GET'])
def edit_profile():
    #log = logging.getLogger("eachRequestResponse")
    #log.info("edit profile")
    updated_user = User.query.get(current_user.get_id())
    form = profile_form(obj=updated_user)
    if form.validate_on_submit():
        updated_user.about = request.form.get('about')
        updated_user.hobbies = request.form.get('hobbies')
        updated_user.education = request.form.get('education')
        updated_user.skills = request.form.get('skills')
        db.session.add(updated_user)
        db.session.commit()
        flash('You Successfully Updated Your Profile', 'success')
        return redirect(url_for('auth.dashboard'))
    return render_template('profile_edit.html', form=form)





@auth.route('/account', methods=['POST', 'GET'])
def edit_account():
    #log = logging.getLogger("eachRequestResponse")
    #log.info("edit account")
    updated_user = User.query.get(current_user.get_id())
    email_updated = False
    password_updated = False
    email = updated_user.email
    password = updated_user.password
    form = security_form(obj=updated_user)
    if form.validate_on_submit():
        updated_user.email = request.form.get('email')
        updated_user.password = request.form.get('password')
        if email != updated_user.email:
            #log.info('email updated!')
            email_updated = True
        if password != updated_user.password:
            #log.info('password updated!')
            password_updated = True
        db.session.add(updated_user)
        db.session.commit()
        if email_updated and password_updated:
            flash('You Successfully Updated your Email and Password', 'success')
        elif email_updated:
            flash('You Successfully Updated your Email', 'success')
        elif password_updated:
            flash('You Successfully Updated your Password', 'success')
        else:
            flash('You Should Not Submit Same Credentials for Changing Your Account Details. Please Try Again with Different Credentials')
            return render_template('manage_account.html', form=form)
        return redirect(url_for('auth.dashboard'))
    return render_template('manage_account.html', form=form)



#You should probably move these to a new Blueprint to clean this up.  These functions below are for user management

@auth.route('/users')
@login_required
@admin_required
def browse_users():
    #log = logging.getLogger("eachRequestResponse")
    #log.info("browse user")
    user_information = User.query.all()
    headers = [('id', 'User ID'),('email', 'Email'), ('registered_on', 'Registered On'), ('active', 'Active Status'), ('skills', 'Skills')]
    add_url = url_for('auth.add_user')
    retrieve_url = ('auth.retrieve_user', [('user_id', ':id')])
    edit_url = ('auth.edit_user', [('user_id', ':id')])
    delete_url = ('auth.delete_user', [('user_id', ':id')])

    current_app.logger.info("Browse page loading")

    return render_template('browse.html', titles=headers, add_url=add_url, edit_url=edit_url, delete_url=delete_url,
                           retrieve_url=retrieve_url, data=user_information, User=User, record_type="Users")


@auth.route('/users/<int:user_id>')
@login_required
def retrieve_user(user_id):
    #log = logging.getLogger("eachRequestResponse")
    #log.info("Retrieve user")
    user = User.query.get(user_id)
    return render_template('profile_view.html', user=user)


@auth.route('/users/<int:user_id>/edit', methods=['POST', 'GET'])
@login_required
def edit_user(user_id):
    #log = logging.getLogger("eachRequestResponse")
    #log.info("Edit user")
    edit_user = User.query.get(user_id)
    about_updated = False
    hobbies_updated = False
    education_updated = False
    skills_updated = False
    about = edit_user.about
    hobbies = edit_user.hobbies
    education = edit_user.education
    skills = edit_user.skills
    form = user_edit_form(obj=edit_user)
    if form.validate_on_submit():
        edit_user.about = request.form.get('about')
        edit_user.hobbies = request.form.get('hobbies')
        edit_user.education = request.form.get('education')
        edit_user.skills = request.form.get('skills')
        edit_user.is_admin = int(form.is_admin.data)
        if about != edit_user.about:
            #log.info('Admin Updated User About Info!')
            about_updated = True
        if hobbies != edit_user.hobbies:
            #log.info('Admin Updated User Hobbies Info!')
            hobbies_updated = True
        if education != edit_user.education:
            #log.info('Admin Updated User Education Info!')
            education_updated = True
        if skills != edit_user.skills:
            #log.info('Admin Updated User Skills Info!')
            skills_updated = True
        db.session.add(edit_user)
        db.session.commit()
        if about_updated or hobbies_updated or education_updated or skills_updated:
            flash('User: ' + edit_user.email + ' Edited Successfully!', 'success')
            current_app.logger.info("edited a user")
            return redirect(url_for('auth.browse_users'))
        else:
            flash('You Did Not Change a Field, or Form Submission Faces a Validation Error. Please Try Again!')
    return render_template('user_edit.html', form=form)


@auth.route('/users/new', methods=['POST', 'GET'])
@login_required
def add_user():
    #log = logging.getLogger("eachRequestResponse")
    #log.info("add user")
    form = register_form()
    if form.validate_on_submit():
        email = request.form.get('email')
        password = request.form.get('password')
        user = User.query.filter_by(email=email).first()
        # if user is registered previously, request to create with different account details.
        if user:
            flash('Found an Already Registered Account. Please Try Again with Different Account Details')
            return redirect(url_for('auth.add_user'), 302)
        #add a new user and add it to the database
        new_user = User(email=email, password=generate_password_hash(password))
        new_user.active = 1
        db.session.add(new_user)
        db.session.commit()
        flash('Congratulations, You Added a New User: ' + new_user.email + ' and It is Now Ready for Login', "success")
        return redirect(url_for('auth.browse_users'), 302)
    return render_template('user_new.html', form=form)


@auth.route('/users/<int:user_id>/delete', methods=['POST'])
@login_required
def delete_user(user_id):
    #log = logging.getLogger("eachRequestResponse")
    #log.info("delete user")
    deleting_user = User.query.get(user_id)
    if deleting_user.id == current_user.id:
        flash("You Are Not Allowed to Delete Yourself!")
        return redirect(url_for('auth.browse_users'), 302)
    email = deleting_user.email
    db.session.delete(deleting_user)
    db.session.commit()
    flash('You Deleted the User: '+ email  + ' Successfully!', 'success')
    return redirect(url_for('auth.browse_users'), 302)