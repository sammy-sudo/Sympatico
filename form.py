from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, PasswordField
from wtforms.validators import Length, EqualTo, Email, DataRequired, NumberRange, ValidationError
from models import user

class registration(FlaskForm):
  first_name = StringField(label='First Name', validators=[DataRequired()])
  second_name = StringField(label='Second Name', validators=[DataRequired()])
  last_name = StringField(label='Last Name', validators=[DataRequired()])
  email_address = StringField(label='Email Address', validators=[Email(), DataRequired()])
  phone_number = IntegerField(label='Phone number', validators=[NumberRange(min=11), DataRequired()])
  username = StringField(label='Username', validators=[Length(min=5, max=25), DataRequired()])
  password = PasswordField(label='Password', validators=[Length(min=5), DataRequired()])
  password1 = PasswordField(label='Confirm Password', validators=[EqualTo('password'), DataRequired()])

  def validate_username(self, username_to_validate):
    username = user.query.filter_by(username=username_to_validate.data).first()
    if username:
      raise ValidationError("Username already exists, Please try anotherone")

  def validate_phone_number(self, phone_number_to_validate):
    phone_number = user.query.filter_by(phone=phone_number_to_validate.data).first()
    if phone_number:
      raise ValidationError("Phone Number already exists, Please try another one")

  def validate_email_address(self, email_to_validate):
    email = user.query.filter_by(email=email_to_validate.data).first()
    if email:
      raise ValidationError("Email Address already exists, Please try another one")

class login(FlaskForm):
  username = StringField(label='Username', validators=[DataRequired()])
  password = PasswordField(label='Password', validators=[DataRequired()])

class Property(FlaskForm):
  name = StringField(label="Enter Property Name", validators=[DataRequired()])
  Address = StringField(label="Enter Property Address", validators=[DataRequired()])
  floors = IntegerField(label="Enter Number of Floors", validators=[DataRequired()])
  rooms = IntegerField(label="Enter Total Number of rooms", validators=[DataRequired()])
  Type = StringField(label="Enter type of property", validators=[DataRequired()])

class Property_login(FlaskForm):
  name = StringField(label="Property Name", validators=[DataRequired()])
  unique_code = IntegerField(label="Unique Code", validators=[DataRequired()])
