from flask import Flask, render_template, redirect, request, session
from cs50 import SQL
from flask_session import Session
from functools import wraps
from tempfile import mkdtemp
from werkzeug.security import check_password_hash, generate_password_hash
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
import random

app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

def login_required(f):
    """
    Decorate routes to require login.

    http://flask.pocoo.org/docs/1.0/patterns/viewdecorators/
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///project.db")


@app.route("/", methods=["GET", "POST"])
@login_required
def index():
    if request.method == "GET":
        return render_template("index.html")
    else:
        return redirect("/time")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
         # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = :username",
                          username=request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return render_template("apology_login.html")

        # Remember which user has logged in
        session["user_id"] =  rows[0]["id"]



        if rows[0]["level"] == "advanced":
            return render_template("advanced.html")
        # Redirect user to home page
        return redirect("/")
    else:
         return render_template("login.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("register.html")
    else:
        password = request.form.get("password")
        username = request.form.get("username")
        confirmation = request.form.get("confirmation")
        level = request.form.get("level")
        password_hash = generate_password_hash(password)
         # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = :username",
                          username=request.form.get("username"))

        # Check if username already exists
        if len(rows) != 0:
            return render_template("apology_register.html")
        db.execute("INSERT INTO users (username, hash, level) VALUES(?, ?, ?)", username, password_hash, level)
        return redirect("/login")

@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/login")

@app.route("/stopwatch")
@login_required
def stopwatch():
    return render_template("stopwatch.html")

@app.route("/timer")
@login_required
def timer():
    return render_template("timer.html")

@app.route("/technique")
@login_required
def technique():
    return render_template("technique.html")


@app.route("/level", methods=["GET", "POST"])
@login_required
def level():
    if request.method == "POST":
        level_user = request.form.get("level")
        username = request.form.get("username")
         # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = :username",
                          username=request.form.get("username"))

        # Check if username exists
        if len(rows) != 1:
            return render_template("apology_level.html")
        db.execute("UPDATE users SET level = ? WHERE username = ?", level_user, username)
        return redirect("/")
    else:
        return render_template("level.html")

@app.route("/time", methods=["GET", "POST"])
@login_required
def time():
    if request.method == "POST":
        session['user_time'] = request.form.get("time")
        return render_template("exercise.html")
    else:
        return render_template("time.html")

# print(session['user_time'])

@app.route("/exercise", methods=["GET", "POST"])
@login_required
def exercise():
    if request.method == "POST":
        categories = request.form.getlist("categories")
        session["categories"] = categories
        user_time = session.get("user_time", None)
        user_id = session.get("user_id", None)
        level = db.execute("SELECT level FROM users WHERE id=?", user_id)
        # db.execute("INSERT INTO workouts (id, time, categories) VALUES(?, ?, ?)", user_id, user_time, categories)
        # category = db.execute("SELECT categories FROM workouts ORDER BY timestamp DESC LIMIT 1")
        # print(category)
        n = len(categories)
        user_time = int(user_time)
        time = user_time
        user_time -= 2
        while time >= 10:
            time -= 10
            user_time -= 2
        # if user_time > 40:
        #     user_time -= 10
        # elif user_time >= 30:
        #     user_time -= 8
        # elif user_time >= 20:
        #     user_time -= 6
        # else:
        #     user_time -= 4
        categories_time = round(user_time / n)
        if level[0]['level'] == 'advanced':
            categories_number = int(categories_time / 2)
        elif level[0]['level'] == 'intermediate':
            categories_number = int(categories_time * 0.75)
        elif level[0]['level'] == 'beginner':
            categories_number = categories_time
        else:
            categories_number = categories_time
        workout = []
        for i in range(n):
            workout_intermediate = db.execute("SELECT exercise FROM ? ORDER BY RANDOM() LIMIT ?", categories[i], categories_number)
            for j in range (len(workout_intermediate)):
                dict_element = workout_intermediate[j]
                workout.append(dict_element['exercise'])
        random.shuffle(workout)
        random.shuffle(workout)
        random.shuffle(workout)

        if level[0]['level'] == 'advanced':
            instruction = "Repeat the above for 2 sets, each exercise-> 1 minute"
        elif level[0]['level'] == 'intermediate':
            instruction = "Repeat the above for 2 sets, each exercise-> 45 seconds"
        elif level[0]['level'] == 'beginner':
            instruction = "Repeat the above for 2 sets, each exercise-> 30 seconds"
        else:
            instruction = "Repeat the above for 2 sets, each exercise-> 30 seconds"
        session["workout"] = workout
        session["instruction"] = instruction
        session["level"] = level[0]["level"]
        s = ", "
        s = s.join(categories)
        p = ", "
        p = p.join(workout)
        db.execute("INSERT INTO workouts (id, categories, time, workout) VALUES(?, ?, ?, ?)", user_id, s, session.get('user_time', None), p)
        return render_template("workout.html", workout=workout, instruction=instruction, level=level[0]['level'], time=session["user_time"])
    else:
        return render_template("exercise.html")

@app.route("/workout")
@login_required
def workout():
    return render_template("workout.html", workout=session.get("workout", None), instruction=session.get("instruction", None), level=session.get("level", None))

@app.route("/warmup", methods=["GET", "POST"])
@login_required
def warmup():
    if request.method == "POST":
        return render_template("workout.html.html")
    else:
        return render_template("warmup.html")

@app.route("/history")
@login_required
def history():
     history = db.execute("SELECT * FROM workouts WHERE id=?",session.get("user_id", None))
     length = len(history)
     return render_template("history.html", history=history, length=length)
