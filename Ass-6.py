from flask import Flask, render_template, request, redirect, url_for, session
from numpy import record
from flask_mysqldb import MySQL
import MySQLdb.cursors
import time
import datetime

ts = time.time()
timestamp = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')

app=Flask(__name__ )
# Change this to your secret key (can be anything, it's for extra protection)
app.secret_key="test your page!"


# Enter your database connection details below
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'rita541982'
app.config['MYSQL_DB'] = 'website'

# Intial MySQL
mysql = MySQL(app)


@app.route("/")
def home():
    return render_template("home.html")


@app.route("/register", methods=["POST"])
def register():
    name=request.form["name"] 
    username=request.form["username"]   # get the form name & password
    password=request.form["password"] 

    cursor=mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT * FROM `member` WHERE `username` = %s ',(username,))
    member=cursor.fetchone()
    if member:
        exists="Account already exists!"
        return redirect(url_for("error",exists=exists))
    else:
        cursor.execute('INSERT INTO member VALUES (NULL, %s, %s, %s,%s,%s)', (name,username, password,0,timestamp))
        mysql.connection.commit()
        return render_template("succeed.html",name=name)


@app.route("/signin", methods=["POST"])
def signin():
     
    username=request.form["username"]   # get the form name & password
    password=request.form["password"] 

    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT * FROM `member` WHERE `username` = %s AND `password` = %s', (username, password,))
# Fetch one record and return result
    member = cursor.fetchone()
    
    if member:  # if  filter the name &password  
        session['username'] = member['username']
        session['password'] = member['password']
        return redirect(url_for("member"))
    elif username== "" or password == "":          
        #name or password empty
        empty="Please Entry Your Name & Password!!"
        return redirect(url_for("error",empty=empty))
    else:
        wrong_entry="You Got Wrong Entry,Please Try Again!"
        return redirect(url_for("error",wrong_entry=wrong_entry))
        #pass the name=name,password=password to error page

@app.route("/member")
def member():
    sId=session.get("username",None)
     #get method judge have session id or not 
    if not sId:
            return redirect(url_for("home"))
    else:
        return render_template("member.html",sId=sId)


@app.route("/logout")    # set the logout to home.page
def logout():
        session.pop("username",None)
        return redirect(url_for("home"))


@app.route("/error") # receive the name &password and show the query string
def error():
    empty=request.args.get("empty")
    wrong_entry=request.args.get("wrong_entry")
    exists=request.args.get("exists")
    if empty:          
        #name or password empty
        return render_template("error.html",empty=empty)
    elif wrong_entry:
        return render_template("error.html",wrong_entry=wrong_entry)
    else:
        return render_template("error.html",exists=exists)
   


app.run(port=3000)