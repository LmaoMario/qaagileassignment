# Import some Flask modules for use later.
from flask import Blueprint, render_template, flash, request, jsonify, redirect, url_for
from flask_login import login_required, current_user

# Import some modules we setup.
from website.auth import login
from .models import User, Post
from . import db

# Imprt json library.
import json

# Allows us to setup a collection of routes.
views = Blueprint('views', __name__)

# Route Setup home page route, allow both GET and POST.
@views.route('/', methods=['GET', 'POST'])
# Only logged in users can see this page.
@login_required
#Define function for when this route is accessed.
def home():
    #Only do the following if we get a POST request, i.e. a request to create a new support ticket.
    if request.method == 'POST':
        # Grab the data from the HTML form.
        title = request.form.get('title')
        desc = request.form.get('desc')
        #Do some basic validation to ensure data will be somewhat useful.
        if len(title) < 5:
            flash('Title is too short.', category='error')
        if len(desc) < 10:
            flash('Description is too short', category='error')
        #If everything is fine, go on to submit the ticket.
        else:
            #Add the new ticket to the database using SQLAlchemy.
            new_post = Post(title=title, desc=desc, user_id=current_user.id)
            db.session.add(new_post)
            db.session.commit()
            #Tell the user that this happened.
            flash('Ticket Submitted', category='success')
    # If the user is an admin, we let them read, update and delete all posts.
    if current_user.permission == 'admin':
        current_user.posts = Post.query.all() 
    #Return the home page with the post data.
    return render_template("home.html", user=current_user)

# Setup a new route for whenever we delete a post.
@views.route('/deletePost', methods=['POST'])
# Require login just in case.
@login_required
# Define function for the /deletePost route.
def delete_post():
    # Get the JSON data from the request and store the values we need in variables.
    post = json.loads(request.data)
    postId = post['postId']
    # Get post
    post = Post.query.get(postId)
    if post:
        # Allow user to delete post only if they created, OR if they're an admin.
        if post.user_id == current_user.id or current_user.permission == 'admin':
            # Delete post and commit back to DB.
            db.session.delete(post)
            db.session.commit()
            flash('Ticket deleted.', category='success')
            return jsonify()

# Setup a new route for updating posts.
@views.route('/updatePost', methods=['POST'])
# Require login just in case.
@login_required
# Define function for updatePost endpoint.
def edit_post():
    # Get the JSON data from the request and store it in variables.
    post = json.loads(request.data)
    postId = post['postId']
    newBody = post['newbody']
    # Get the post in a way that we can update it later.
    sessionpost = db.session.query(Post).filter_by(id=postId).first()
    if sessionpost:
        # Set the description attribute of the post to the updated body.
        setattr(sessionpost, 'desc', newBody)
        # Save the new body.
        db.session.commit()
        # Tell the user that the operation has succeeded.
        flash('Updated Ticket.', category="success")
        return jsonify()

@views.route('/admin', methods=['GET', 'POST'])
# Only logged in users can see this page.
@login_required
#Define function for when this route is accessed.
def admin():
    if current_user.permission == 'admin':
        users = User.query.all()
        return render_template("admin.html", user=current_user, users=users)

# Add route to delete user.
@views.route('/deleteUser', methods=['POST'])
# Require login just in case.
@login_required
# Define function for the /deletePost route.
def delete_user():
    # Get the JSON data from the request and store the values we need in variables.
    user = json.loads(request.data)
    userId = user['userId']
    User.query.filter(User.id == userId).delete()
    db.session.commit()
    # Re-get all users for admin view.
    allusers = User.query.all()
    flash('Deleted user.', category='error')
    return jsonify()