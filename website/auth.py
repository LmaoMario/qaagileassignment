# Import the Flask modules we will need again.
from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User, Post
# Import module for password hashing.
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
# Use flask_login for managing logged in users.
from flask_login import login_user, login_required, logout_user, current_user

# Create Auth blueprint to add routes to.
auth = Blueprint('auth', __name__)

# Login route to handle login event.
@auth.route('/login', methods=["POST", "GET"])
def login():
    # Only do login code when request is a POST.
    if request.method == 'POST':
        # Get the data we need from the HTML form.
        email = request.form.get("email")
        password = request.form.get("password")
        
        # Filter for the User object from the database.
        user = User.query.filter_by(email=email).first()
        # If the user exists, attempt to login.
        if user:
            # Use the werkzeug.security module to verify the password hash.
            if check_password_hash(user.password, password):
                # If the user is an admin, allow them to see all posts.
                if user.permission == 'admin':
                    # Tell the user that you've logged in as an admin.
                    flash('Logged in successfully as an administrator.', category='success')
                    # Update the posts to get all of them, not just ones created by that user.
                    user.posts = Post.query.all()
                    # Pass user to flask_login to manage
                    login_user(user, remember=True)
                    # Go back to the home page.
                    return render_template('/home.html', user=current_user)
                else:
                    #Login as a normal user.
                    flash('Logged in successfully.', category='success')
                    login_user(user, remember=True)
                    # Simple redirect as we don't need to modify the data before returning the view.
                    return redirect(url_for('views.home'))
            else:
                # If password hashes do not match, tell the user.
                flash('Incorrect password.', category='error')
        else:
            # If the user doesn't exist, the email isn't registered. Tell the user.
            flash('Email does not exist.', category='error')
    # Go to the login page.
    return render_template("login.html", user=current_user)

# Add route for logout.
@auth.route('/logout')
# Require login
@login_required
# Define function for logout route.
def logout():
    # Do some flask_login user management stuff to logout.
    logout_user()
    return redirect(url_for('auth.login'))

# Add route for sign up.
@auth.route('/sign-up', methods=["POST", "GET"])
# Define function for sign up endpoint.
def sign_up():
    # Only do the following if request is a POST.
    if request.method == 'POST':
        # Get required data from HTML form.
        email = request.form.get("email")
        firstName = request.form.get("firstname")
        password = request.form.get("password")
        confirmpassword = request.form.get("confirmpassword")
        # Grab the user object by email address.
        user = User.query.filter_by(email=email).first()
        # To make email addresses unique, If the user exists, tell the user and go back to the sign up page.
        if user:
            flash('Email already exists.', category='error')
            return render_template("sign_up.html")
        # Some validation on the sign up values to ensure that data is somewhat valid, then tell the user.
        if len(email) < 4:
            flash("Email does not meet the minimum length requirement.", category="error")
        elif len(firstName) < 2:
            flash("First name does not meet the minimum length requirement.", category="error")
        elif password != confirmpassword:
            flash("Passwords do not match.", category="error")
        elif len(password) < 7:
            flash("Password does not meet the minimum length requirement.", category="error")
        else:
            # Sign user up if all requirements are met.
            new_user = User(email=email, name=firstName, password=generate_password_hash(password, method='sha256')) # Use Sha256 hashing.
            # Store new user in database.
            db.session.add(new_user)
            db.session.commit()
            # Tell user that account is created, log them in and go to the home page.
            flash("Account created", category="success")
            login_user(new_user, remember=True)
            return redirect(url_for('views.home'))

            #Add user
    return render_template("sign_up.html", user=current_user)