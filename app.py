import datetime
import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, g, session, jsonify
from flask_session import Session
from dotenv import load_dotenv
from werkzeug.security import check_password_hash, generate_password_hash
from scrapper import user_query
from forms import CreateUserForm, LoginForm
from helpers import login_required


# Configure application
app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv("app_secret_key")


# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///movie_lib.db")


@app.before_request
def before_request():
    g.db = db


@app.route("/")
# add login required
@login_required
def index():
    return render_template("index.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    print("Login route")
    login_form = LoginForm()
    print(login_form)

    #Ensure login info is validated and login form is submitted via POST request method
    if login_form.validate_on_submit():
        print("Login form validated")
        return render_template("index.html")

    return render_template("login.html", login_form=login_form, current_route="/login")


@app.route("/create_account", methods=["GET","POST"])
def create_account():
    #print("Reg form submitted")
    reg_form = CreateUserForm()
   
    # Ensure all user account registration is validated and account reg form is submitted via POST request method
    if reg_form.validate_on_submit():
        firstname = reg_form.first_name.data
        lastname = reg_form.last_name.data
        username = reg_form.user_name.data
        password = reg_form.password.data
        hash = generate_password_hash(password)

        # user registration data stored in users table in movie_lib db
        db.execute("INSERT INTO users (first_name, last_name, user_name, hash) VALUES (?,?,?,?)", firstname, lastname, username, hash)

        # user is then redirected to the login page
        return redirect('/')
    return render_template("create_account.html", reg_form=reg_form, current_route="/create_account")


@app.route("/signedin")
def signedin():
    return render_template("signedin.html")    


@app.route("/search_page")
def search_page():
    search_page = True
    print("search page")
    return render_template("index.html", search_page=search_page)

@app.route("/search")
def search():
    q = request.args.get("q")
    if q:
        movies = user_query(q)
        #print(movies)
        print("movies receieved by flask function")
        for movie in movies:
            print(movie['title'])
    
    else:  
        movies = []
    return jsonify(movies)  


@app.route("/watch", methods=["POST"])
def watch():
    title = request.get_json()
    print(title)
    
    return jsonify(title)      



