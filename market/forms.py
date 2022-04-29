from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import Length, EqualTo, Email, DataRequired, ValidationError
from market.models import User

class RegisterForm(FlaskForm):
    
    def validate_username(self, username_to_check):
        user = User.query.filter_by(username=username_to_check.data).first()
        if user:
            raise ValidationError("Entered username already exists! Enter new user name")
        
    def validate_email_address(self, email_address_to_check):
        emailAddress = User.query.filter_by(emailAddress=email_address_to_check.data).first()
        if emailAddress:
            raise ValidationError("Entered email address already exists! Enter new email id.")
        
    username=StringField(label='User Name', validators=[Length(min=2, max=30), DataRequired()])
    email_address=StringField(label='Email Address', validators=[Email(), DataRequired()])
    password1=PasswordField(label='Password:', validators=[Length(min=6), DataRequired()])
    password2=PasswordField(label='Confirm Password:', validators=[EqualTo('password1'), DataRequired()])
    submit=SubmitField(label='Create Account')

class LoginForm(FlaskForm):
    
    username=StringField(label='User Name:', validators=[DataRequired()])
    password=PasswordField(label='Password:', validators=[DataRequired()])
    submit=SubmitField(label='Sign In')
    
class purchasedForm(FlaskForm):
    submit=SubmitField(label="Purchase item!")
    
class sellForm(FlaskForm):
    submit=SubmitField(label="Sell item!")