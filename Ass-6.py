from socket import MsgFlag
from flask import Flask, render_template, request, redirect, url_for, session
from numpy import empty, record
import mysql.connector      # import the db and use methods
import time                     # for the timestamp to database
import datetime

ts = time.time() # def time :
timestamp = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S') 

app=Flask(__name__ )
# Change this to your secret key (can be anything, it's for extra protection)
app.secret_key="test your page!"


# database connection details 
mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="rita541982",
  database="website"   # use which database:
)


mycursor = mydb.cursor()


@app.route("/")
def home():
    return render_template("home.html")


@app.route("/register", methods=["POST"])
def register():
    name=request.form["name"] 
    username=request.form["username"]   # get the form name & password
    password=request.form["password"]
    
    mycursor = mydb.cursor() # use the method     
    mycursor.execute('SELECT * FROM `member` WHERE `username` = %s ',(username,)) #execute the select 
    member=mycursor.fetchone() # fetchone = get member table
    if member: #if the member username exists 
                exists="Account already exists!"
                return redirect(url_for("error",msg=exists))
    elif not username or not name or not password:  #if the form empty 
            fill_in="Please fill in the form"
            return redirect(url_for("error",msg=fill_in))
    else:                                               # the value column must same with database  
         mycursor.execute('INSERT INTO member VALUES (NULL, %s, %s, %s,%s,%s)', (name,username, password,0,timestamp))
         mydb.commit()  # push to database 
         return render_template("succeed.html",name=name) # send to succeed page


@app.route("/signin", methods=["POST"])
def signin():
    username=request.form["username"]   # get the form username & password
    password=request.form["password"] 

    mycursor = mydb.cursor() 
    mycursor.execute('SELECT * FROM `member` WHERE `username` = %s AND `password` = %s', (username, password,)) 
# Fetch one record and return result
    member = mycursor.fetchone()
    
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
        mycursor = mydb.cursor()
        query="SELECT `username`, `content` FROM `member` INNER JOIN `message` ON `member`.id = `message`.`member_id`"
        mycursor.execute(query)
        dates=mycursor.fetchall()
        for data in dates:
            return render_template("member.html",sId=sId,dates=dates)


@app.route("/logout")    # set the logout to home.page
def logout():
        session.pop("username",None)
        return redirect(url_for("home"))


@app.route("/error") # receive msg show the query string
def error():
    msgs=request.args.get("msg")
    return render_template("error.html",msgs=msgs)

# @app.route("/message",methods=["POST"])
# def message():




app.run(port=3000)