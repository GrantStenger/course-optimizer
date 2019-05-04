from flask import render_template, flash, redirect, url_for, request
from app import app, db
from flask_login import current_user, login_user, logout_user, login_required
from datetime import datetime
from app.forms import LoginForm, RegistrationForm, CourseRegistrationForm
from app.forms import DropCourseForm, EditProfileForm, UpdateCourseValForm
from app.forms import DepartmentsForm
from app.models import User, Course, Department
from werkzeug.urls import url_parse

@app.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()

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


def add_departments(user, departments):
    for dept in departments:
        dept_obj = Department(title=dept.title, user=user)
        db.session.add(dept_obj)
    db.session.commit()

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
    return render_template('add_course.html', form=form)

@app.route('/user/<username>', methods=['GET', 'POST'])
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    if user.courses.first() == None:
        return redirect('new_user/' + str(current_user.username))
    drop_form = DropCourseForm()
    val_form = UpdateCourseValForm()
    if drop_form.validate_on_submit() and 'drop_course' in request.form:
        course = user.courses.filter_by(id=request.form['drop_course_id']).one()
        db.session.delete(course)
        db.session.commit()
        flash('You dropped ' + course.title)
        return redirect('user/' + str(current_user.username))
    elif val_form.validate_on_submit() and 'value' in request.form:
        course = user.courses.filter_by(id=request.form['val_course_id']).one()
        course.value = val_form.value.data
        db.session.commit()
        flash('Course value has been updated.')
        return redirect(url_for('user', username=current_user.username))
    return render_template('user.html', user=user, drop_form=drop_form,
                           val_form=val_form)

@app.route('/new_user/<username>', methods=['GET', 'POST'])
@login_required
def new_user(username):
    user = User.query.filter_by(username=username).first_or_404()
    dept_form = DepartmentsForm()
    if dept_form.validate_on_submit():
        print(request)
        print(request.form)
        print(request.form['dept_id'])
        department = user.departments.filter_by(id=request.form['dept_id']).one()
        department.value = dept_form.value.data
        db.session.commit()
        flash('Department value has been updated.')
        return redirect(url_for('user', username=current_user.username))

    return render_template('new_user.html', user=user,
                           dept_form=dept_form)

@app.route('/users')
def users():
    users = User.query.all()
    return render_template('users.html', users=users)

@app.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm(current_user.username)
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.about_me = form.about_me.data
        db.session.commit()
        flash('Your changes have been saved.')
        return redirect(url_for('user', username=current_user.username))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.about_me.data = current_user.about_me
    return render_template('edit_profile.html', title='Edit Profile',
                           form=form)
