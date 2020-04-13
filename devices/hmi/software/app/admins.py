import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for, jsonify, json
)
from werkzeug.security import check_password_hash, generate_password_hash

from app.db import get_db

admin = Blueprint('admins', __name__, template_folder='templates/admins', static_folder='static')

"""
 This file handles user authentification.
 Methods
    login_required: Decorator to check if user is logged in
 Routes
    admin: no functionality yet
    admin/add_user: Inserts a new user in the database
    reset_password: Will get deleted.
"""

def admin_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None or g.user['user_role'] != 'admin':
            return redirect(url_for('views.view'))

        return view(**kwargs)

    return wrapped_view

@admin.route('/dashboard')
@admin_required
def dashboard():
    """
    Admin view.
    :return: The admin.html view
    Note: Has no functionality yet
    """
    return render_template('admin.html')


@admin.route('/dashboard/add_user', methods=('GET', 'POST'))
@admin_required
def add_user():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        error = None

        if not username:
            error = 'Username is required.'
        elif not password:
            error = 'Password is required.'
        elif db.execute(
            'SELECT id FROM user WHERE username = ?', (username,)
        ).fetchone() is not None:
            error = 'User {} is already registered.'.format(username)

        if error is None:
            db.execute(
                'INSERT INTO user (username, password, user_role) VALUES (?, ?, ?)',
                (username, generate_password_hash(password), "user")
            )
            db.commit()
            return redirect(url_for('auths.login'))

        flash(error)

    return render_template('add_user.html')

@admin.route('/dashboard/add_admin', methods=('GET', 'POST'))
@admin_required
def add_admin():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        error = None

        if not username:
            error = 'Username is required.'
        elif not password:
            error = 'Password is required.'
        elif db.execute(
            'SELECT id FROM user WHERE username = ?', (username,)
        ).fetchone() is not None:
            error = 'User {} is already registered.'.format(username)

        if error is None:
            db.execute(
                'INSERT INTO user (username, password, user_role) VALUES (?, ?, ?)',
                (username, generate_password_hash(password), "admin")
            )
            db.commit()
            return redirect(url_for('auths.login'))

        flash(error)

    return render_template('add_user.html')

@admin.route('/dashboard/reset_password')
@admin_required
def reset_password():
    """
    Password reset view.
    :return: The password_reset.html view
    Note: Has no functionality yet
    """
    return render_template('reset_password.html')