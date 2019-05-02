from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms import TextAreaField, IntegerField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo
from wtforms.validators import Length
from app.models import User

class LoginForm(FlaskForm):
    username    = StringField('Username', validators=[DataRequired()])
    password    = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit      = SubmitField('Sign In')

class RegistrationForm(FlaskForm):
    username  = StringField('Username', validators=[DataRequired()])
    email     = StringField('Email', validators=[DataRequired(), Email()])
    password  = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit    = SubmitField('Register')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Please use a different username.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please use a different email address.')

class CourseRegistrationForm(FlaskForm):
    prefix      = StringField('Prefix', validators=[DataRequired()])
    number      = StringField('Number', validators=[DataRequired()])
    title       = StringField('Title', validators=[DataRequired()])
    description = TextAreaField('Description', validators=[DataRequired()])
    units       = StringField('Units', validators=[DataRequired()])
    value       = StringField('Value', validators=[DataRequired()])
    submit      = SubmitField('Register')

class EditProfileForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    about_me = TextAreaField('About me', validators=[Length(min=0, max=140)])
    submit   = SubmitField('Submit')

    def __init__(self, original_username, *args, **kwargs):
        super(EditProfileForm, self).__init__(*args, **kwargs)
        self.original_username = original_username

    def validate_username(self, username):
        if username.data != self.original_username:
            user = User.query.filter_by(username=self.username.data).first()
            if user is not None:
                raise ValidationError('Please use a different username.')

class DropCourseForm(FlaskForm):
    drop_course = SubmitField('Drop Course')
    course_id   = "" # plz delete this line

class UpdateCourseValForm(FlaskForm):
    value = IntegerField('Value', validators=[DataRequired()])
    title = StringField('Title', validators=[DataRequired()])
