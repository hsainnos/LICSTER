import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for, jsonify, json
)
from werkzeug.security import check_password_hash, generate_password_hash

from app.db import get_db

auth = Blueprint('auths', __name__, template_folder='templates/auths', static_folder='static')

"""
 This file handles user authentification.
 Methods
    login_required: Decorator to check if user is logged in
    logout_required: Decorator to check if user is logged out
    load_logged_in_user: Loads the current user if he exists
 Routes
    login: login for user
    logout: Logout for user
"""

def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auths.login'))

        return view(**kwargs)

    return wrapped_view

def logout_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user:
            return redirect(url_for('auths.logout'))

        return view(**kwargs)

    return wrapped_view

@auth.before_app_request
def load_logged_in_user():
    """
    Checks if client was logged in with every request
    """
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        g.user = get_db().execute(
            'SELECT * FROM user WHERE id = ?', (user_id,)
        ).fetchone()

@auth.route('/login', methods=['GET', 'POST'])
@logout_required
def login():
    """
    Login view.
    :return: The login.html view
    :return after form validation: the index.html
    """
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        error = None
        user = db.execute(
            'SELECT * FROM user WHERE username = ?', (username,)
        ).fetchone()

        if user is None:
            error = 'Incorrect username.'
        elif not check_password_hash(user['password'], password):
            error = 'Incorrect password.'

        if error is None:
            session.clear()
            session['user_id'] = user['id']
            session['user_role'] = user['user_role']
            return redirect(url_for('views.index'))

        flash(error)
    return render_template('login.html')


@auth.route('/logout')
@login_required
def logout():
    session.clear()
    return redirect(url_for('views.index'))

