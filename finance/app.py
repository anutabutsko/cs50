import datetime
import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, lookup, usd

# Configure application
app = Flask(__name__)

# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")

# Make sure API key is set
if not os.environ.get("API_KEY"):
    raise RuntimeError("API_KEY not set")


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
    """Show portfolio of stocks"""
    user_id = session["user_id"]

    purchases_db = db.execute(
        "SELECT symbol, SUM(shares) AS shares, price FROM transactions WHERE user_id = ? GROUP BY symbol", user_id)
    money_db = db.execute("SELECT cash FROM users WHERE id = ?", user_id)
    money = money_db[0]["cash"]

    return render_template("index.html", database=purchases_db, money=money, usd=usd)


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""
    if request.method == "GET":
        return render_template("buy.html")
    else:
        symbol = request.form.get("symbol").upper()
        shares = request.form.get("shares")

        if not symbol:
            return apology("Please enter Symbol")

        sl = lookup(symbol.upper())
        if not sl:
            return apology("Please provide Valid Symbol")

        if not shares.isdigit() or int(shares) <= 0:
            return apology("Unacceptable Share")

        share_price = int(shares) * sl["price"]

        user_id = session["user_id"]
        money_db = db.execute("SELECT cash FROM users WHERE id = ?", user_id)
        money = money_db[0]["cash"]

        if money < share_price:
            return apology("Not enough money in your wallet:(")

        db.execute("UPDATE users SET cash = ? WHERE id = ?", money - share_price, user_id)

        date = datetime.datetime.now()
        db.execute("INSERT INTO transactions (user_id, symbol, shares, price, date) VALUES(?, ?, ?, ?, ?)", user_id,
                   sl["symbol"], shares, sl["price"], date)
        flash("Congratulations on your purchase!")
        return redirect("/")


@app.route("/history")
@login_required
def history():
    """Show history of transactions"""
    user_id = session["user_id"]
    transactions_db = db.execute("SELECT * FROM transactions WHERE user_id = ?", user_id)
    return render_template("history.html", transactions=transactions_db)


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
    return redirect("/")


@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    """Get stock quote."""
    if request.method == "GET":
        return render_template("quote.html")
    else:
        symbol = request.form.get("symbol")

        if not symbol:
            return apology("Please enter Symbol")

        sl = lookup(symbol.upper())
        if not sl:
            return apology("Please provide Valid Symbol")

        return render_template("quoted.html", sl=sl, usd=usd)


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    if request.method == "GET":
        return render_template("register.html")
    else:
        username = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")

        if not username:
            return apology("Please provide a valid Username")
        if not password:
            return apology("Please enter a valid Password")
        if not confirmation or confirmation != password:
            return apology("Confirmation must match the Password")

        secure_password = generate_password_hash(password)
        try:
            user_register = db.execute("INSERT INTO users (username, hash) VALUES (?, ?)", username, secure_password)
        except:
            return apology("Username already exists. Please go to login page")

        session["user_id"] = user_register
        return redirect("/")


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""
    if request.method == "GET":
        user_id = session["user_id"]
        symbols_db = db.execute(
            "SELECT symbol FROM transactions WHERE user_id = ? GROUP BY symbol HAVING SUM(shares) > 0", user_id)
        return render_template("sell.html", symbols=[i["symbol"] for i in symbols_db])

    else:
        symbol = request.form.get("symbol")
        shares = request.form.get("shares")

        if not symbol:
            return apology("Please enter Symbol")

        sl = lookup(symbol.upper())
        if sl is None:
            return apology("Please provide Valid Symbol")

        if int(shares) <= 0:
            return apology("Unacceptable Share")

        share_price = int(shares) * sl["price"]

        user_id = session["user_id"]
        money_db = db.execute("SELECT cash FROM users WHERE id = ?", user_id)
        money = money_db[0]["cash"]

        shares_db = db.execute("SELECT shares FROM transactions WHERE user_id = ? AND symbol = ? GROUP BY symbol",
                               user_id, symbol)
        user_shares = shares_db[0]["shares"]

        if int(shares) > user_shares:
            return apology("Not enough shares to sell")

        money += share_price
        db.execute("UPDATE users SET cash = ? WHERE id = ?", money, user_id)

        date = datetime.datetime.now()
        db.execute("INSERT INTO transactions (user_id, symbol, shares, price, date) VALUES(?, ?, ?, ?, ?)", user_id,
                   sl["symbol"], (-1) * int(shares), sl["price"], date)
        flash("Thank you for selling your stock!")
        return redirect("/")


@app.route("/add", methods=["GET", "POST"])
@login_required
def add():
    """Add money to the account"""
    if request.method == "GET":
        return render_template("add.html")
    else:
        amount = request.form.get("amount")

        if amount is None:
            return apology("Please enter valid amount")

        user_id = session["user_id"]
        money_db = db.execute("SELECT cash FROM users WHERE id = ?", user_id)
        money = money_db[0]["cash"]

        money += int(amount)
        db.execute("UPDATE users SET cash = ? WHERE id = ?", money, user_id)

        return redirect("/")
