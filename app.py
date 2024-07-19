"""
I've created an admin login for this application, however normal users can be created also.
The admin username is admin, and the admin password is adminpassword

The admin user and normal users differ. The admin user, once logged in gains access to the admin dashboard,
where all users and their bookings are listed. From here any booking in the database can be cancelled

The regular user, once logged in, can book a session by selecting a time slot and a date. The users booking
is then saved to the database. The user has the option to view their booked sessions, and cancel them if they
choose. A user can only view their own bookings when they're logged in.
"""

from flask import Flask, render_template, session, redirect, url_for, g, request
from database import get_db, close_db
from flask_session import Session
from werkzeug.security import generate_password_hash, check_password_hash
from forms import RegistrationForm, LoginForm, BookingForm
from functools import wraps
from datetime import datetime, date

app = Flask(__name__)
app.teardown_appcontext(close_db)
app.config["SECRET_KEY"] = "123456789"
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)



@app.before_request
def logged_in_user():
    g.user = session.get("user_id", None)

def login_required(view):
    @wraps(view)
    def wrapped_view(*args, **kwargs):
        if g.user is None:
         return redirect(url_for("login", next=request.url))
        return view(*args, **kwargs)
    return wrapped_view

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/register", methods = ["GET", "POST"])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user_id = form.user_id.data
        password = form.password.data
        password2 = form.password2.data
        db = get_db()
        possible_clashing_user = db.execute("""SELECT * FROM users WHERE user_id = ?;""", (user_id,)).fetchone()
        if possible_clashing_user is not None:
            form.user_id.errors.append("Username already taken!")
        else:
            db.execute("""INSERT INTO users (user_id, password) VALUES (?, ?);""", (user_id, generate_password_hash(password)))
            db.commit()
            return redirect( url_for("login") )
    return render_template("register.html", form=form)

@app.route("/login", methods = ["GET", "POST"]) 
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user_id = form.user_id.data
        password = form.password.data
        db = get_db()
        possible_clashing_user = db.execute("""SELECT * FROM users WHERE user_id = ?;""", (user_id,)).fetchone()
        if possible_clashing_user is None:
            form.user_id.errors.append("No such user!")
        elif not check_password_hash(possible_clashing_user["password"], password):
            form.password.errors.append("Incorrect password!")
        else:
            session.clear()
            session["user_id"] = user_id
            next_page = request.args.get("next")
            if user_id == 'admin':
                    next_page = url_for("admin")
                    return redirect(next_page)
            elif not next_page:
                next_page = url_for("index")
                return redirect(next_page)
            else:
                next_page = url_for("index")
                return redirect(next_page)
    return render_template("login.html", form=form)


@app.route("/logout")
def logout():
    session.clear()
    return redirect( url_for("index") )

@app.route("/book", methods = ["GET", "POST"])
@login_required
def book():
    form = BookingForm()
    confirmation=""
    if form.validate_on_submit():
        booking = form.booking.data
        date = form.date.data
        my_date1 = datetime.strftime(date, "%Y-%m-%d")
        user_id = session["user_id"]
        db = get_db()
        db.execute("""INSERT INTO bookings (user_id, booking, date) VALUES (?, ?, ?);""", (user_id, booking, my_date1))
        db.commit()
        confirmation = "Session booked successfully"
    return render_template("booking.html", form=form, confirmation=confirmation)

@app.route("/dashboard", methods = ["GET"])
@login_required
def dashboard():
    user_id = session["user_id"]
    db = get_db()
    rows = db.execute("""SELECT * FROM bookings WHERE user_id = ?;""", (user_id,) ).fetchall()
    db.commit()
    return render_template("dashboard.html", rows=rows)


@app.route("/dashboard/cancel/<int:id>", methods = ["GET", "POST"])
@login_required
def cancel_booking(id):
    user_id = session["user_id"]
    booking_id = id
    db = get_db()
    db.execute("""DELETE FROM bookings WHERE id = ?;""", (booking_id,))
    db.commit()
    next_page = request.args.get("next")
    if user_id == 'admin':
        next_page = url_for("admin")
        return redirect(next_page)
    else:
        next_page = url_for("dashboard")
        return redirect(next_page)
    

@app.route("/admin", methods = ["GET", "POST"])
@login_required
def admin():
    db = get_db()
    rows = db.execute("""SELECT * FROM bookings;""").fetchall()
    db.commit()
    return render_template("admin.html", rows = rows)

