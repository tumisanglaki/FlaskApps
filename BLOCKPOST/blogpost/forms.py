from flask_wtf import FlaskForm
from flask_wtf.file import FileField,FileAllowed
from flask_login import current_user
from wtforms import StringField,PasswordField,SubmitField,BooleanField,TextAreaField
from wtforms.validators import DataRequired,Length,Email,EqualTo,ValidationError
from blogpost.datamodel import User

class RegistrationForm(FlaskForm):
    username = StringField('Username',validators=[DataRequired(),Length(min=3,max=20)])
    fname = StringField('FirstName',validators=[DataRequired(),Length(min=3,max=20)])
    lname = StringField('Surname',validators=[DataRequired(),Length(min=3,max=20)])
    email = StringField('EmailAddress',validators=[DataRequired(),Email()])
    passwd = PasswordField('Password',validators=[DataRequired(),Length(min=6,max=24)])
    confirm_passwd = PasswordField('Confirm Password',validators=[DataRequired(),EqualTo('passwd')])
    submit = SubmitField('Sign Up')

    def validate_username(self,username):
        user = User.query.filter_by(username=username.data).first()
        if(user):
            raise ValidationError("UserName Already Taken Please Choose Another!")
    def validate_email(self,email):
        user = User.query.filter_by(email=email.data).first()
        if(user):
            raise ValidationError("Email Already Taken Please Choose Another!")

class LoginForm(FlaskForm):
    email = StringField('EmailAddress',validators=[DataRequired(),Email()])
    passwd = PasswordField('Password',validators=[DataRequired(),Length(min=6,max=24)])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')

class RequestResetForm(FlaskForm):
    email = StringField('EmailAddress',validators = [DataRequired(),Email()])
    submit = SubmitField('RequestPassword Reset')

    def validate_email(self,email):
        user = User.query.filter_by(email=email.data).first()
        if(user is None):
            raise ValidationError('No Account For That Field')

class ResetPasswordForm(FlaskForm):
    passwd = PasswordField('New Password', validators = [DataRequired(),Length(min=8,max=24)])
    confirm_passwd = PasswordField('Confirm Password', validators = [DataRequired(),EqualTo('passwd')])
    submit = SubmitField('Reset Password')

class PostForm(FlaskForm):
    post_img = FileField("Post Image",validators=[FileAllowed(['jpg','jpeg','png'])])
    title = StringField("Post Title",validators=[DataRequired()])
    content = TextAreaField("Post Content",validators=[DataRequired()])
    submit = SubmitField("POST")

class UpdateAccountForm(FlaskForm):
    pic = FileField("Update Profile Picture",validators=[FileAllowed(['jpg','jpeg','png'])])
    username = StringField('Username',validators=[DataRequired(),Length(min=4,max=20)])
    fname = StringField('FirstName',validators=[DataRequired(),Length(min=3,max=20)])
    lname = StringField('Surname',validators=[DataRequired(),Length(min=3,max=20)])
    email = StringField('Email',validators=[DataRequired(),Email()])
    submit = SubmitField("Update")

    def validate_username(self,username):
        if(username.data != current_user.username):
            user = User.query.filter_by(username=username.data).first()
            if(user):
                raise ValidationError("Username Already Taken Please Choose Another Username")

    def validate_email(self,email):
        if(email.data != current_user.email):
            user = User.query.filter_by(email=email.data).first()
            if(user):
                raise ValidationError("Email Already Taken Please Choose Another Username")

class CommentForm(FlaskForm):
    content = TextAreaField("Comment",validators=[DataRequired()])
    submit = SubmitField("comment")