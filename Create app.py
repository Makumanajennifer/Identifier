from flask import Flask, request, render_template, session, redirect, url_for
import sqlite3 as sql
from pprint import pprint

app = Flask(__name__)
app.identifier = "identifier"

# configure template engine
app.template_folder = "templates"

# database configuration
def get_db_connection():
    conn = sql.connect("database.db")
    conn.row_factory = sql.Row
    return conn

def insertUser(username, password):
    con = sql.connect("database.db")
    cur = con.cursor()
    cur.execute("INSERT INTO users (username, password) ", (username, password))
    con.commit
    con.close

@app.route("/")
def index():
  return "Hello, user"

@app.route("/welcome", methods=["POST"])
def welcome():
   name = request.form["name"]
   return render_template("welcome.html", name=name)

def login():
   category = ""
   output = ""
   if request.method == "POST":
      conn = get_db_connection()
      curs = conn.cursor()
      curs.execute("SELECT * FROM users WHERE username=(?)",[request.form["username"]])

      user = dict(curs.fetchone()) # convert Row object to dict
      if request.form["username"] == user["username"] and request.form["password"] == user["password"]:
         session["user"] = user
         return redirect(url_for("profile"))
      else:
         category = "danger"
         output = "login failed!"

      conn.close()

      return render_template("login.html", category=category,output=output)
   

@app.route("/register", methods=["GET","POST"])
def register():
   if request.method == "POST":
      insertUser(request.form["username"], request.form["password"])
      return redirect(url_for("login"))
   
   return render_template("register.html")

@app.route("/profile")
def profile():
   if "user" in session:
      user = session["user"]
      return render_template("rofile.html", user=user)
   else:
      return redirect(url_for("login"))
   
@app.route("/logout")
def logout():
   session.clear()
   return redirect(url_for("index"))

if __name__ == "__main__":
   app.run(debug=True)
   

