from socket import MsgFlag
from unittest import result
from flask import Flask, render_template, request, redirect, url_for, session
from numpy import record
from flask_mysqldb import MySQL
import MySQLdb.cursors          # import the db and use methods
import time                     # for the timestamp to database
import datetime

ts = time.time() # def time :
timestamp = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S') 

app=Flask(__name__ )
# Change this to your secret key (can be anything, it's for extra protection)
app.secret_key="test your page!"


# Enter database connection details 
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'website' # use the database

#  let = mysql , Intial MySQL (class)
mysql = MySQL(app)


@app.route("/")
def home():
    return render_template("home.html")


@app.route("/register", methods=["POST"])
def register():
    name=request.form["name"] 
    username=request.form["username"]   # get the form name & password
    password=request.form["password"] 

    cursor=mysql.connection.cursor(MySQLdb.cursors.DictCursor) # use the method     
    cursor.execute('SELECT * FROM `member` WHERE `username` = %s ',(username,)) #execute the select 
    member=cursor.fetchone() # fetchone = get member table
    if member: #if the member username exists 
        exists="Account already exists!"
        return redirect(url_for("error",msg=exists))
    else:                                               # the value column must same with database  
        cursor.execute('INSERT INTO member VALUES (NULL, %s, %s, %s,%s,%s)', (name,username, password,0,timestamp))
        mysql.connection.commit()  # push to database 
        return render_template("succeed.html",name=name) # send to succeed page


@app.route("/signin", methods=["POST"])
def signin():
     
    username=request.form["username"]   # get the form username & password
    password=request.form["password"] 

    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT * FROM `member` WHERE `username` = %s AND `password` = %s', (username, password,)) 
# Fetch one record and return result
    member = cursor.fetchone()
    
    if member:  # if  filter the username & password  
        session['username'] = member['username'] # Create session data,can access this data in other routes
        session['password'] = member['password']
        return redirect(url_for("member"))
    elif username== "" or password == "":          
        #name or password empty
        empty="Please Entry Your Name & Password!!"
        return redirect(url_for("error",msg=empty))
    else:
        wrong_entry="You Got Wrong Entry,Please Try Again!"
        return redirect(url_for("error",msg=wrong_entry))
        #pass the name=name,password=password to error page

@app.route("/member")
def member():
    sId=session.get("username",None) # use session 
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
    msgs=request.args.get("msg")
    return render_template("error.html",msgs=msgs)

   


app.run(port=3000)