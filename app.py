import os
import random

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, lookup, usd

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finalproj.db")

# Make sure API key is set
#if not os.environ.get("API_KEY"):
#    raise RuntimeError("API_KEY not set")


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/")
@login_required
def index():
    return render_template("index.html")

@app.route("/yourgames", methods=["GET", "POST"])
@login_required
def yourgames():
    if request.method == "GET":
        Games = db.execute("SELECT * FROM games WHERE Admin = ?", session["user_id"])
        for row in Games:
            admin_id = row["Admin"]
            admin_name = db.execute("SELECT username FROM users WHERE id = ?", admin_id)
            row["admin_name"] = admin_name[0]["username"]
        GameId = db.execute("SELECT * FROM Games WHERE Admin = ?", admin_id) 
        ids = []
        for game in GameId:
            ids.append(game["game_id"])
        players = []
        for id in ids:
            players += db.execute("SELECT * FROM players WHERE game_id = ?", id)
        for row in players:
            userid = row["user_id"]
            username = db.execute("SELECT username FROM users WHERE id = ?", userid)
            row["username"] = username[0]["username"]
        for row in players:
            GameId = row["game_id"]
            GameName = db.execute("SELECT Name from Games WHERE game_id = ?", GameId)
            row["GameName"] = GameName[0]["Name"]
        
        return render_template("yourgames.html", Games=Games, players=players)

    #to start a game
    else:
        gamename = request.form.get("gamename")
        GameNames = db.execute("SELECT * FROM Games WHERE Admin = ? AND Name = ?", session["user_id"], gamename)
        #make sure they only start a game they've created
        print(GameNames)
        if not GameNames:
            return apology("You can only start games which you've created")
        
        game_id = db.execute("SELECT game_id FROM Games WHERE Name = ?", request.form.get("gamename"))[0]["game_id"]
        game_players = db.execute("SELECT user_id FROM players WHERE game_id = ?", game_id)
        print('game players', game_players)
        random.shuffle(game_players)
        print('shuffled', game_players)

        for i in range(len(game_players)):
            if i == len(game_players)-1:
                exception = db.execute("INSERT INTO targets (game_id, assassin, target) VALUES(?, ?, ?)", game_id, game_players[i]["user_id"], game_players[0]["user_id"])
                print(exception)
            else:
                assignment = db.execute("INSERT INTO targets (game_id, assassin, target) VALUES(?, ?, ?)", game_id, game_players[i]["user_id"], game_players[i+1]["user_id"])
                print(assignment)
        flash("Game Started!")
        return redirect("/viewtarget")

@app.route("/viewtarget", methods=["GET", "POST"])
@login_required
def viewtarget():
    # assassin = db.execute("SELECT username FROM users WHERE id = ?", session["user_id"])[0]["username"]
    # target = db.execute("SELECT target FROM targets WHERE assassin = ?", assassin)
    # if not target:
    #     return render_template("not-started.html")
    if request.method == "GET":
            targets = db.execute("SELECT game_id, target FROM targets WHERE assassin = ?", session["user_id"])
            for row in targets:
                game_id = row["game_id"]
                gamename = db.execute("SELECT Name FROM Games WHERE game_id = ?", game_id)
                row["gamename"] = gamename[0]["Name"]
            for row in targets:
                target_id = row["target"]
                targetname = db.execute("SELECT username FROM Users WHERE id = ?", target_id)
                print('target name', targetname)
                row["targetname"] = targetname[0]["username"]
    return render_template("viewtarget.html", targets=targets)

@app.route("/gamejoined", methods=["GET", "POST"])
@login_required
def gamejoined():
    if request.method == "GET":
        GameId = db.execute("SELECT game_id FROM players WHERE user_id = ?", session["user_id"]) 
        ids = []
        for game in GameId:
            ids.append(game["game_id"])
        Games = []
        for id in ids:
            Games += db.execute("SELECT * FROM Games WHERE game_id = ?", id)
        for row in Games:
            admin_id = row["Admin"]
            admin_name = db.execute("SELECT username FROM users WHERE id = ?", admin_id)
            row["admin_name"] = admin_name[0]["username"]

        return render_template("gamejoined.html", Games=Games)


@app.route("/create", methods=["GET", "POST"])
@login_required
def create():
    if request.method == "POST":
        gamename = request.form.get("gamename")
        Key = request.form.get("key")
        #query database to see if game name exists
        rows = db.execute("SELECT * FROM Games WHERE Name = ?", gamename)
        #if name does exist, bad
        if len(rows) == 1 or not gamename:
            return apology("either you did't enter a name, or game name already exists. try again")
        db.execute("INSERT INTO Games (Admin, Name, Key) VALUES (?, ?, ?)", session["user_id"], gamename, Key)
        return redirect("/yourgames")
    return render_template("create.html")


@app.route("/join", methods=["GET", "POST"])
@login_required
def join():
#display all available games
    if request.method == "GET":
        Games = db.execute("SELECT * FROM games")
        for row in Games:
            admin_id = row["Admin"]
            admin_name = db.execute("SELECT username FROM users WHERE id = ?", admin_id)
            row["admin_name"] = admin_name[0]["username"]
#enter key
    if request.method == "POST":
        #print(request.form.get("key"))
        if not request.form.get("key"):
            return apology("must provide key")
        #query database for key
        rows = db.execute("SELECT * FROM Games WHERE Key = ?", request.form.get("key"))
        # Ensure key is correct
        if len(rows) != 1:
            return apology("invalid key!")
        #make sure user has not already joined game
        Game_Id = db.execute("SELECT game_id FROM Games WHERE Key = ?", request.form.get("key"))[0]["game_id"]
        print(Game_Id)
        users = db.execute("SELECT ? FROM Players WHERE game_id = ?", session["user_id"], Game_Id)
        print(users)
        if users:
            return apology("You have already joined this game!")
        #select name of game that matches the key entered
        GameId = db.execute("SELECT game_id from Games WHERE Key = ?", request.form.get("key"))[0]["game_id"]
        #name the new table after this game's name
        db.execute("INSERT INTO players (game_id, user_id) VALUES (?, ?)", GameId, session["user_id"])

        return redirect("/gamejoined")

    return render_template("join.html", Games=Games)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/intro")


@app.route("/kill", methods=["GET", "POST"])
@login_required
def kill():
    """Get stock quote."""
    if request.method == "POST":
        target = request.form.get("target")
        if not request.form.get("target"):
            return apology("please input a name")
        ls = lookup(users)
        if ls == None:
            return apology("not a valid player/not your target")
        #submit user's input via post to /quote
        return render_template("quoted.html", ls=ls) #WORKING ON THIS RN
    elif request.method == "GET":
        return render_template("kill.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    # prompt user to register for an account
    if request.method == "POST":
        username = request.form.get("username")
        #query database to see if username exists
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))
        #if username does exist, bad
        if len(rows) == 1 or not request.form.get("username"):
            return apology("either you did't enter a username, or username already exists. try again")

        password = request.form.get("password")
        #make sure password was input
        if not request.form.get("password"):
            return apology("please input a password")
        confirmation = request.form.get("confirmation")
        #make sure passwords match
        if request.form.get("password") != request.form.get("confirmation"):
            return apology("passwords do not match")
        password_hash = generate_password_hash(password)
        id = db.execute("INSERT INTO users (username, hash) VALUES (?, ?)", username, password_hash)
        #record user id for future reference
        session["user_id"] = id
        return redirect("/")
    return render_template("register.html")


@app.route("/deregister", methods=["POST"])
def deregister():

    # Forget registrant
    id = request.form.get("username")
    if id:
        db.execute("DELETE FROM users WHERE username = ?", username)
    return redirect("/killconfirm") #page saying congrats. you have officially reported your kill of ___


@app.route("/intro", methods=["GET", "POST"])
def intro():
    
    return render_template("intro.html")

def errorhandler(e):
    #"""Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return apology(e.name, e.code)


# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)

# methods=["GET", "POST"]
# if request.method == "POST":
#     def target():
#         game_id = db.execute("SELECT game_id FROM Games WHERE Name = ?", request.form.get(gamename))
#         game_players = db.execute("SELECT user_id FROM players WHERE game_id = ?", game_id)
#         game_players.shuffle()
#         for i in range(len(game_players)):
#             if i == len(game_players)-1:
#                 exception = db.execute("INSERT INTO targets (game_id, assassin, target) VALUES(?, ?, ?) FROM players", game_id, game_players[i], game_players[0])
#                 print(exception)
#             else:
#                 assignment = db.execute("INSERT INTO targets (game_id, assassin, target) VALUES(?, ?, ?)", game_id, game_players[i], game_players[i+1])
#                 print(assignment)