from flask import Flask, render_template, redirect, request, session
from flask_sqlalchemy import SQLAlchemy
from flask_session import Session
from functools import wraps
from tempfile import mkdtemp
from werkzeug.security import check_password_hash, generate_password_hash
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
import random
import os
from datetime import datetime
from sqlalchemy import text, Column, Integer, String, DateTime, func

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

# Configure SQLAlchemy
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///project.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

# Define database models that match the existing schema
class User(db.Model):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String, nullable=False, unique=True)
    hash = Column(String, nullable=False)
    level = Column(String, nullable=False)

class Arms(db.Model):
    __tablename__ = 'arms'
    exercise = Column(String, primary_key=True)

class Legs(db.Model):
    __tablename__ = 'legs'
    exercise = Column(String, primary_key=True)

class Abs(db.Model):
    __tablename__ = 'abs'
    exercise = Column(String, primary_key=True)

class Cardio(db.Model):
    __tablename__ = 'cardio'
    exercise = Column(String, primary_key=True)

class Workout(db.Model):
    __tablename__ = 'workouts'
    # Using a combination of fields that should be unique
    id = Column(Integer, nullable=False)
    time = Column(Integer, nullable=False)
    categories = Column(String)
    workout = Column(String)
    timestamp = Column(DateTime, default=func.current_timestamp())
    # Since the original table doesn't have a primary key, we'll add a virtual one
    # This won't be reflected in the actual database schema
    __mapper_args__ = {
        'primary_key': [id, timestamp]
    }

# Initialize database
def init_db():
    # Check if database is initialized
    try:
        db.session.execute(text("SELECT 1 FROM users"))
        print("Database schema already exists")
    except:
        print("Creating database schema")
        # Create database schema directly using SQL to match existing structure
        db.session.execute(text("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                username TEXT NOT NULL,
                hash TEXT NOT NULL,
                level TEXT NOT NULL
            )
        """))
        
        db.session.execute(text("CREATE TABLE IF NOT EXISTS arms (exercise TEXT NOT NULL)"))
        db.session.execute(text("CREATE TABLE IF NOT EXISTS legs (exercise TEXT NOT NULL)"))
        db.session.execute(text("CREATE TABLE IF NOT EXISTS abs (exercise TEXT NOT NULL)"))
        db.session.execute(text("CREATE TABLE IF NOT EXISTS cardio (exercise TEXT NOT NULL)"))
        
        db.session.execute(text("""
            CREATE TABLE IF NOT EXISTS workouts (
                id INTEGER NOT NULL,
                time NUMERIC NOT NULL,
                categories TEXT,
                workout TEXT,
                timestamp DATETIME DEFAULT CURRENT_DATE
            )
        """))
        
        db.session.commit()
    
    # Check if exercises tables are populated
    if db.session.execute(text("SELECT COUNT(*) FROM arms")).fetchone()[0] == 0:
        # Populate arms exercises
        arms_exercises = [
            "Push Ups", "Bicep Curls", "Overhead Triceps", "Metabolism Booster", 
            "Side step with weight", "Lateral Raise", "Overhead Press", "Tricep Box Dip", 
            "Hammer Curls", "Alternate toe touch"
        ]
        for exercise in arms_exercises:
            db.session.execute(text("INSERT INTO arms (exercise) VALUES (:exercise)"), {"exercise": exercise})
    
    if db.session.execute(text("SELECT COUNT(*) FROM legs")).fetchone()[0] == 0:
        # Populate legs exercises
        legs_exercises = [
            "Lunges", "Side Lunges", "Squats", "Jump Squats", "Single leg calf raises", 
            "Side leg raises", "Plank Ski-Hops", "Sit Ups", "4-dip Lunges", 
            "Mountain Climbers", "Dumbell Lunge"
        ]
        for exercise in legs_exercises:
            db.session.execute(text("INSERT INTO legs (exercise) VALUES (:exercise)"), {"exercise": exercise})
    
    if db.session.execute(text("SELECT COUNT(*) FROM abs")).fetchone()[0] == 0:
        # Populate abs exercises
        abs_exercises = [
            "Low Plank", "High Plank", "Bicycles", "Scissors", "Crunches", 
            "Crab Walk", "Side Plank on Forearm-both sides", "Side Plank on Palm-both sides", 
            "Burpees", "Jumping Jacks", "In and Out"
        ]
        for exercise in abs_exercises:
            db.session.execute(text("INSERT INTO abs (exercise) VALUES (:exercise)"), {"exercise": exercise})
    
    if db.session.execute(text("SELECT COUNT(*) FROM cardio")).fetchone()[0] == 0:
        # Populate cardio exercises
        cardio_exercises = [
            "Pendulum Swings", "Knee Ups", "Butt Kicks", "Staircase", 
            "Sliding", "Shuttle Run", "Toe Taps", "Fast Jog in place"
        ]
        for exercise in cardio_exercises:
            db.session.execute(text("INSERT INTO cardio (exercise) VALUES (:exercise)"), {"exercise": exercise})
    
    # Commit changes
    db.session.commit()
    print("Database initialization complete")

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
        result = db.session.execute(text("SELECT * FROM users WHERE username = :username"), 
                                 {"username": request.form.get("username")})
        rows = result.fetchall()

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0][2], request.form.get("password")):
            return render_template("apology_login.html")

        # Remember which user has logged in
        session["user_id"] = rows[0][0]

        if rows[0][3] == "advanced":
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
        result = db.session.execute(text("SELECT * FROM users WHERE username = :username"), 
                                 {"username": request.form.get("username")})
        rows = result.fetchall()

        # Check if username already exists
        if len(rows) != 0:
            return render_template("apology_register.html")
        
        db.session.execute(text("INSERT INTO users (username, hash, level) VALUES(:username, :password_hash, :level)"), 
                        {"username": username, "password_hash": password_hash, "level": level})
        db.session.commit()
        
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
        result = db.session.execute(text("SELECT * FROM users WHERE username = :username"), 
                                 {"username": request.form.get("username")})
        rows = result.fetchall()

        # Check if username exists
        if len(rows) != 1:
            return render_template("apology_level.html")
        
        db.session.execute(text("UPDATE users SET level = :level_user WHERE username = :username"), 
                        {"level_user": level_user, "username": username})
        db.session.commit()
        
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

@app.route("/exercise", methods=["GET", "POST"])
@login_required
def exercise():
    if request.method == "POST":
        categories = request.form.getlist("categories")
        session["categories"] = categories
        user_time = session.get("user_time", None)
        user_id = session.get("user_id", None)
        
        result = db.session.execute(text("SELECT level FROM users WHERE id=:user_id"), 
                                 {"user_id": user_id})
        level = result.fetchall()
        
        n = len(categories)
        user_time = int(user_time)
        time = user_time
        user_time -= 2
        while time >= 10:
            time -= 10
            user_time -= 2
            
        categories_time = round(user_time / n)
        if level[0][0] == 'advanced':
            categories_number = int(categories_time / 2)
        elif level[0][0] == 'intermediate':
            categories_number = int(categories_time * 0.75)
        elif level[0][0] == 'beginner':
            categories_number = categories_time
        else:
            categories_number = categories_time
        workout = []
        for i in range(n):
            result = db.session.execute(text(f"SELECT exercise FROM {categories[i]} ORDER BY RANDOM() LIMIT :limit"), 
                                     {"limit": categories_number})
            workout_intermediate = result.fetchall()
            for j in range(len(workout_intermediate)):
                workout.append(workout_intermediate[j][0])
                
        random.shuffle(workout)
        random.shuffle(workout)
        random.shuffle(workout)

        if level[0][0] == 'advanced':
            instruction = "Repeat the above for 2 sets, each exercise-> 1 minute"
        elif level[0][0] == 'intermediate':
            instruction = "Repeat the above for 2 sets, each exercise-> 45 seconds"
        elif level[0][0] == 'beginner':
            instruction = "Repeat the above for 2 sets, each exercise-> 30 seconds"
        else:
            instruction = "Repeat the above for 2 sets, each exercise-> 30 seconds"
        session["workout"] = workout
        session["instruction"] = instruction
        session["level"] = level[0][0]
        s = ", "
        s = s.join(categories)
        p = ", "
        p = p.join(workout)
        
        db.session.execute(text("INSERT INTO workouts (id, categories, time, workout) VALUES(:user_id, :categories, :user_time, :workout)"), 
                        {"user_id": user_id, "categories": s, "user_time": session.get('user_time', None), "workout": p})
        db.session.commit()
        
        return render_template("workout.html", workout=workout, instruction=instruction, level=level[0][0], time=session["user_time"])
    else:
        return render_template("exercise.html")

@app.route("/workout")
@login_required
def workout():
    return render_template("workout.html", workout=session.get("workout", None), instruction=session.get("instruction", None), level=session.get("level", None), time=session.get("user_time", None))

@app.route("/warmup", methods=["GET", "POST"])
@login_required
def warmup():
    if request.method == "POST":
        return render_template("workout.html")
    else:
        return render_template("warmup.html")

@app.route("/history")
@login_required
def history():
     result = db.session.execute(text("SELECT * FROM workouts WHERE id=:user_id ORDER BY timestamp DESC"), 
                             {"user_id": session.get("user_id", None)})
     history = result.fetchall()
     length = len(history)
     return render_template("history.html", history=history, length=length)

if __name__ == "__main__":
    # Initialize the database before running the app
    with app.app_context():
        init_db()
    app.run(debug=True)
