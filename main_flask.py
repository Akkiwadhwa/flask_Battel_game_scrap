from flask import Flask, render_template, redirect, url_for, flash, request
from flask_login import LoginManager, current_user, logout_user, UserMixin, login_user, login_required
import mysql.connector
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from werkzeug.security import generate_password_hash, check_password_hash
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired
from flask_gravatar import Gravatar

app = Flask(__name__)
mydb = mysql.connector.connect(
    host="localhost",
    user="admin",
    password="admin",
    database="db"
)

app.config['SECRET_KEY'] = "vjdvjdfjdfgsjd14"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////blog.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
gravatar = Gravatar(app, size=100, rating='g', default='retro', force_default=False, force_lower=False, use_ssl=False, base_url=None)

class User(UserMixin, db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(100))


with app.app_context():
    db.create_all()


class RegisterForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    name = StringField("Name", validators=[DataRequired()])
    submit = SubmitField("Sign Me Up!")


class LoginForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Log in")


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@app.route('/login', methods=["GET", "POST"])
def login():
    form1 = RegisterForm()
    form = LoginForm()
    print(request.form.get("submit"))
    if request.method == 'POST' and 'name' in request.form:
        if User.query.filter_by(email=form1.email.data).first():
            # User already exists
            flash("You've already signed up with that email, log in instead!")
            return redirect(url_for('login'))

        hash_and_salted_password = generate_password_hash(
            form1.password.data,
            method='pbkdf2:sha256',
            salt_length=8
        )
        new_user = User(
            email=form1.email.data,
            name=form1.name.data,
            password=hash_and_salted_password,
        )
        db.session.add(new_user)
        db.session.commit()
        login_user(new_user)
        return redirect(url_for("index"))
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        user = User.query.filter_by(email=email).first()
        # Email doesn't exist or password incorrect.
        if not user:
            flash("That email does not exist, please try again.")
            return redirect(url_for('login'))
        elif not check_password_hash(user.password, password):
            flash('Password incorrect, please try again.')
            return redirect(url_for('login'))
        else:
            login_user(user)
            return redirect(url_for("index"))
    return render_template('login.html', form=form, form1=form1, current_user=current_user)


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.route('/index')
@login_required
def index():
    return render_template("index.html")


@app.route('/ranking')
def ranking():
    cur = mydb.cursor()
    cur.execute("select * from ranking")
    rv = cur.fetchall()
    cur1 = mydb.cursor()
    cur1.execute(
        "show columns from ranking")
    rv1 = cur1.fetchall()
    li = [i[0] for i in rv1]
    print(rv)
    return render_template("ranking_table.html", table=rv, col=li)


@app.route('/members')
def members():
    cur = mydb.cursor()
    cur.execute("select * from members")
    rv = cur.fetchall()
    cur1 = mydb.cursor()
    cur1.execute(
        "show columns from members")
    rv1 = cur1.fetchall()
    li = [i[0] for i in rv1]
    print(rv)
    return render_template("members_table.html", table=rv, col=li)


@app.route('/alliance')
def alliance():
    cur = mydb.cursor()
    cur.execute("select * from alliance")
    rv = cur.fetchall()
    cur1 = mydb.cursor()
    cur1.execute(
        "show columns from alliance")
    rv1 = cur1.fetchall()
    li = [i[0] for i in rv1]
    return render_template("alliance_table.html", table=rv, col=li)


@app.route('/profile')
def profile():
    return render_template("profile.html")




if __name__ == "__main__":
    app.run(debug=True)
