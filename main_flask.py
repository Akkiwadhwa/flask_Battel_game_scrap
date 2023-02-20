from flask import Flask, render_template, redirect, url_for, flash, request
from flask_login import LoginManager, current_user, logout_user, UserMixin, login_user, login_required
import mysql.connector
from flask_paginate import get_page_parameter, Pagination, get_page_args
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

app.config['SECRET_KEY'] = "1s25c8tph256vlfQ25454sfbgfbgbfbs54ff5f56sfg4g"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////project.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
gravatar = Gravatar(app, size=200, rating='g', default='retro', force_default=False, force_lower=False, use_ssl=False,
                    base_url=None)


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


@app.route('/', methods=["GET", "POST"])
def login():
    form1 = RegisterForm()
    form = LoginForm()
    print1 = request.method
    print(print1)
    if request.method == 'POST' and 'name' in request.form:
        if User.query.filter_by(email=request.form.get("email")).first():
            # User already exists
            flash("You've already signed up with that email, log in instead!")
            return redirect(url_for('login'))

        hash_and_salted_password = generate_password_hash(
            request.form.get("password"),
            method='pbkdf2:sha256',
            salt_length=8
        )
        new_user = User(
            email=request.form.get("email"),
            name=request.form.get("name"),
            password=hash_and_salted_password,
        )
        db.session.add(new_user)
        db.session.commit()
        login_user(new_user)
        return redirect(url_for("index"))
    if request.method == 'POST' and request.form.get("submit") == "Log in":
        email = request.form.get("email")
        password = request.form.get("password")
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


@app.route('/dashboard')
@login_required
def index():
    return render_template("index.html")


# @app.route('/')
# def main():
#     return render_template("index1.html")


@app.route('/alliance')
@login_required
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


@app.route('/alliance_progress')
@login_required
def alliance_progress():
    cur = mydb.cursor()
    cur.execute("select * from alliance_progress")
    rv = cur.fetchall()
    cur1 = mydb.cursor()
    cur1.execute(
        "show columns from alliance_progress")
    rv1 = cur1.fetchall()
    li = [i[0] for i in rv1]
    return render_template("alliance_progress.html", table=rv, col=li)


@app.route('/ranking')
@login_required
def ranking():
    cur = mydb.cursor()
    cur.execute("select * from ranking")
    rv = cur.fetchall()
    cur1 = mydb.cursor()
    cur1.execute(
        "show columns from ranking")
    rv1 = cur1.fetchall()
    li = [i[0] for i in rv1]
    return render_template("ranking_table.html", table=rv, col=li)


@app.route('/members')
@login_required
def members():
    cur = mydb.cursor()
    cur.execute("select * from members")
    rv = cur.fetchall()
    cur1 = mydb.cursor()
    cur1.execute(
        "show columns from members")
    rv1 = cur1.fetchall()
    li = [i[0] for i in rv1]
    return render_template("members_table.html", table=rv, col=li)


@app.route('/members_progress')
@login_required
def members_progress():
    cur = mydb.cursor()
    cur.execute("select * from members_progress")
    rv = cur.fetchall()
    cur1 = mydb.cursor()
    cur1.execute(
        "show columns from members_progress")
    rv1 = cur1.fetchall()
    li = [i[0] for i in rv1]
    return render_template("members_progress.html", table=rv, col=li)


@app.route('/battles')
@login_required
def battles():
    cur = mydb.cursor()
    cur.execute("select * from battles")
    rv = cur.fetchall()
    cur1 = mydb.cursor()
    cur1.execute(
        "show columns from battles")
    rv1 = cur1.fetchall()
    li = [i[0] for i in rv1]
    return render_template("battles.html", table=rv, col=li)


@app.route('/alliance_protocal')
@login_required
def alliance_protocal():
    cur = mydb.cursor()
    cur.execute("select * from alliance_protocal")
    rv = cur.fetchall()
    cur1 = mydb.cursor()
    cur1.execute(
        "show columns from alliance_protocal")
    rv1 = cur1.fetchall()
    li = [i[0] for i in rv1]
    return render_template("alliance_protocal.html", table=rv, col=li)


@app.route('/alliance_rundmails')
@login_required
def alliance_rundmails():
    cur = mydb.cursor()
    cur.execute("select * from alliance_rundmails")
    rv = cur.fetchall()
    cur1 = mydb.cursor()
    cur1.execute(
        "show columns from alliance_rundmails")
    rv1 = cur1.fetchall()
    li = [i[0] for i in rv1]
    return render_template("alliance_rundmails.html", table=rv, col=li)


@app.route('/maps')
@login_required
def maps():
    cur = mydb.cursor()
    cur.execute("select * from maps")
    rv = cur.fetchall()
    cur1 = mydb.cursor()
    cur1.execute(
        "show columns from maps")
    rv1 = cur1.fetchall()
    li = [i[0] for i in rv1]
    return render_template("maps.html", table=rv, col=li)


@app.route('/lost_units')
@login_required
def lost_units():
    cur = mydb.cursor()
    cur.execute("select * from Lost_units")
    rv = cur.fetchall()
    cur1 = mydb.cursor()
    cur1.execute(
        "show columns from Lost_units")
    rv1 = cur1.fetchall()
    li = [i[0] for i in rv1]
    page = request.args.get(get_page_parameter(), type=int, default=1)
    print(page)
    limit = 20
    offset = page*limit - limit
    cur1.execute("""select * from Lost_units
                            limit %s offset %s""", (limit, offset))
    data = cur1.fetchall()
    print(data)

    search = False
    q = request.args.get('q')
    if q:
        search = True
    pagination = Pagination(page=page, total=len(rv),per_page=limit,search=search, record_name='Lost_units')
    return render_template("lost_units.html", table=rv, col=li,pagination=pagination,data = data)


@app.route('/profile')
@login_required
def profile():
    return render_template("profile.html", current_user=current_user)


if __name__ == "__main__":
    app.run(debug=True)
