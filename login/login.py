# LOGIN AND DATABASE ACCESS.

from flask import request, render_template, session, url_for, redirect, flash, Blueprint
from datetime import timedelta

# Create a blueprint.
log = Blueprint("log", __name__, static_folder="static",
                template_folder="templates")

# Store session.

# session.permanent = True <--- only for active http
log.permanent_session_lifetime = timedelta(minutes=30)

# Login.
@log.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # set session
        session.permanenet = True
        # get username and password from the form
        user = request.form['nm']
        password = request.form['psw']
        # store them in session
        session['user'] = user
        session['password'] = password

        error = None
        if not user:
            error = "Username is required"
        elif not password:
            error = "Password is required"
        elif error is None:
            flash('Successfully logged in', 'success')
            return redirect(url_for('home'))
        flash(error, 'error')
    else:
        if 'user' in session:
            flash('Already logged in', 'info')
            return redirect(request.referrer)
        return render_template('login.html')

# Logout.
@log.route('/logout')
def logout():
    session.pop('user', None)
    # Only display the message if user is in the session
    flash(f'You have been logged out', 'info')
    return redirect(url_for('log.login'))

# Access the dentist database.
@log.route('/dentist_database')
def get_dentist_database():
    # check if user is in session
    if 'user' in session:
        user = session['user']
        return render_template("/dentists.html", user=user)
    else:
        flash('Please login to access this page', 'warning')
        return redirect(url_for('log.login'))

# Access the patient database.
@log.route('/patient_database')
def get_patient_database():
    if 'user' in session:
        user = session['user']
        return render_template("/patients.html", user=user)
    else:
        flash('Please login to access this page', 'warning')
        return redirect(url_for('log.login'))