from flask import Flask, render_template, request, flash, redirect, url_for, session
import sqlite3 as sql
import datetime, time

app = Flask(__name__)
app.secret_key = 'proje_password'

@app.route('/')
def index():
    if 'logged_in' not in session:
        return redirect("/login")
    else:
        return render_template('index.html')


@app.route('/register', methods=['POST', 'GET'])
def register():
    if 'logged_in' not in session:
        msg = []
        error = False
        registered = False
        if request.method == 'POST':
            with sql.connect("database.db") as con:
                conn = con.cursor()
                conn.execute(
                    "select * from users where username=?", (str(request.form['username']),))
            username_exists = conn.fetchall()

            try:
                if username_exists:
                    msg.append("Existing username")
                    error = True

                if not error:
                    with sql.connect("database.db") as con:
                        cur = con.cursor()
                        cur.execute(
                            "INSERT INTO users (name, username, email, password) VALUES(?, ?, ?, ?)",
                            (request.form['name'], request.form['username'], request.form['email'],
                             str(request.form['password'])))
                        con.commit()
                        registered = True
            except:
                con.rollback()
            finally:
                return render_template("register.html", title="Register", registered=registered, msg=msg)
        if request.method == 'GET':
            return render_template("register.html", title="Register")
    else:
        return redirect("/")


@app.route('/login', methods=['POST', 'GET'])
def login():
    if 'logged_in' not in session:
        msg = []
        login = False
        if request.method == 'POST':
            with sql.connect("database.db") as con:
                cur = con.cursor()
                cur.execute("select * from users where username=? and password=?",
                            (str(request.form['username']),
                             str(request.form['password'])))

                row = cur.fetchone()
                if row is None:
                    msg.append('Username or password is incorrect!')

                else:
                    msg.append('Logged in successfully!')
                    session['logged_in'] = True
                    session['username'] = str(request.form['username'])
                    login = True

                return render_template('login.html', title="Login", msg=msg, login=login)
        if request.method == 'GET':
            return render_template('login.html', title="Login")
    else:
        return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)
