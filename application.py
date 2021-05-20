from types import new_class
from flask import Flask, render_template, flash, redirect, url_for
from flask_login.utils import login_required
from form import registration, login, Property, Property_login
from models import user, db, Properties
from flask_login import login_manager, login_user, logout_user, LoginManager
import datetime, random

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = ('mssql://KEVINKAGWIMA/sympatico?driver=sql server?trusted_connection=yes')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'f6ceyh5fad0d4cde6af126894'

db.init_app(app)
login_manager = LoginManager()
login_manager.login_view = 'signin'
login_manager.login_message_category = "danger"
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return user.query.get(int(user_id))

@app.route("/")
@app.route("/home")
def index():
  return render_template('index.html')

@app.route("/registration", methods=["POST", "GET"])
def signup():
  form = registration()
  if form.validate_on_submit():
    date = datetime.datetime.now()
    member = user(
      first_name = form.first_name.data,
      second_name = form.second_name.data,
      last_name = form.last_name.data,
      email = form.email_address.data,
      phone = form.phone_number.data,
      date = date,
      username = form.username.data,
      passwords = form.password.data
      )
    db.session.add(member)
    db.session.commit()
    flash(f'User registered successfully', category='success')
    return redirect(url_for('signin'))
  
  if form.errors != {}:
    for err_msg in form.errors.values():
      flash(f'There was an error creating the user: {err_msg}', category='danger')

  return render_template('signup.html', form=form)

@app.route("/signin", methods=["POST", "GET"])
def signin():
  form = login()
  if form.validate_on_submit():
    member = user.query.filter_by(username=form.username.data).first()
    if member and member.check_password_correction(attempted_password=form.password.data):
      login_user(member)
      flash(f"Success! you are logged in: welcome {member.username}", category='success')
      return redirect(url_for('index'))
    else:
      flash(f"Invalid login credentials", category='danger')
  return render_template('signin.html', form=form)

@app.route("/logout")
def logout():
  logout_user()
  flash(f"Logged out successfully", category='success')
  return redirect(url_for('signin'))

@app.route("/Landlord_portal", methods=["POST", "GET"])
@login_required
def landlord():
  form = Property()
  Unique_number = random.randint(100000, 999999)
  date = datetime.datetime.now()
  if form.validate_on_submit():
    new_property = Properties(
      name = form.name.data,
      address = form.Address.data,
      floors = form.floors.data,
      rooms = form.rooms.data,
      Type = form.Type.data,
      unique_id = Unique_number,
      date = date,
    )
    db.session.add(new_property)
    db.session.commit()
    flash(f"Property: {new_property.name}  was created successfully", category='success')
    return redirect(url_for('property_login'))

  if form.errors != {}:
    for err_msg in form.errors.values():
      flash(f'There was an error creating the property: {err_msg}', category='danger')
  return render_template('landlord.html', form=form)

@app.route("/property_login", methods=["POST", "GET"])
def property_login():
  form = Property_login()
  if form.validate_on_submit():
    new_property = Properties.query.filter_by(name=form.name.data).first()
    if new_property and new_property.unique_id == form.unique_code.data:
      login_user(new_property)
      flash(f"Authentication complete", category="success")
      return redirect(url_for('dashboard'))
    else:
      flash(f"Invalid Property Details", category="danger")
  return render_template("property_login.html", form=form)

@app.route("/dashboard")
def dashboard():
  return render_template('dashboard.html')
