from flask import render_template, flash, redirect, url_for, request
from app import app, db
from flask_login import current_user, login_user, logout_user, login_required
from app.forms import LoginForm, RegistrationForm, CourseRegistrationForm
from app.forms import DropCourseForm
from app.models import User, Course
from werkzeug.urls import url_parse

@app.route('/')
@app.route('/index')
def index():
    user = {'username': 'Grant'}
    courses = [
        {
            'prefix': 'CSCI',
            'number': '675',
            'title': 'Convex and Combinatorial Optimization',
            'description': 'Topics include: Convex sets and functions; ' + \
                           'convex optimization problems; geometric and ' + \
                           'Lagrangian duality; simplex algorithm; ' + \
                           'ellipsoid algorithm and its implications; ' + \
                           'matroid theory; submodular optimization. ',
            'units': 4,
            'prereqs': ['CSCI 570', 'CSCI 670'],
            'value': 9
        },
        {
            'prefix': 'CSCI',
            'number': '670',
            'title': 'Advanced Analysis of Algorithms',
            'description': 'Fundamental techniques for design and analysis ' + \
                           'of algorithms. Dynamic programming; network ' + \
                           'flows; theory of NP-completeness; linear ' + \
                           'programming; approximation, randomized, and ' + \
                           'online algorithms; basic cryptography. ',
            'units': 4,
            'prereqs': ['CSCI 570'],
            'value': 8
        }
    ]
    courses = []
    return render_template('index.html', name='Grant', courses=courses)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('user', username=current_user.username))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('user', username=current_user.username)
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        login_user(user, remember=True)
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

@app.route('/add_Course', methods=['GET', 'POST'])
@login_required
def add_course():
    form = CourseRegistrationForm()
    if form.validate_on_submit():
        course = Course(prefix=form.prefix.data, number=form.number.data,
                       title=form.title.data, description=form.description.data,
                       units=form.units.data, value=form.value.data,
                       user=current_user)

        db.session.add(course)
        db.session.commit()
        flash('Congratulations, you just added a new course!')
        return redirect('user/' + str(current_user.username))
    return render_template('add-course.html', form=form)

@app.route('/user/<username>', methods=['GET', 'POST'])
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    form = DropCourseForm()
    if form.validate_on_submit():
        course = user.courses.filter_by(id=request.form['course_id']).one()
        db.session.delete(course)
        db.session.commit()
        flash('You dropped ' + course.title)
        return redirect('user/' + str(current_user.username))
    return render_template('user.html', user=user, form=form)

@app.route('/users')
def users():
    users = User.query.all()
    return render_template('users.html', users=users)
