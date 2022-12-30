from flask import request, render_template, session, url_for, redirect, flash, Blueprint
from datetime import timedelta

log = Blueprint("log", __name__, static_folder="static",
                template_folder="templates")
log.permanent_session_lifetime = timedelta(minutes=30)
@log.route('/', methods=['GET', 'POST'])

def login():
    if request.method == 'POST':
        session.permanenet = True
        user = request.form['Username']
        password = request.form['Password']
        session['Username'] = user
        session['Password'] = password

        error = None
        if not user:
            error = "This user does not exist."
        elif not password:
            error = "This password is incorrect."
        elif error is None:
            flash('Welcome Back')
            return
        flash(error, 'Error')
    else:
        return render_template('login.html')

@log.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('log.login'))

@log.route('/family_members_database')
def get_family_members_database():
    if 'user' in session:
        user = session['Username']
        return render_template("/family_members.html", user=user)
    else:
        return redirect(url_for('log.login'))