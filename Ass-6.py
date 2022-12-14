
from flask import Flask, render_template, request, redirect, url_for,session
import mysql.connector      # import the db and use connector                   
import datetime



app=Flask(__name__ )
# Change this to your secret key 
app.secret_key="test your page!"


# database connection details 
mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="",
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
    
    mycursor = mydb.cursor(dictionary=True) # use the method  - result  dictionary=True
    mycursor.execute('SELECT * FROM `member` WHERE `username` = %s ',(username,)) #execute the select 
    member=mycursor.fetchone() # fetchone = get member table
    if member: #if the member username exists 
                exists="Account already exists!"
                return redirect(url_for("error",msg=exists))
    elif not username or not name or not password:  #if the form empty 
            fill_in="Please fill in the form"
            return redirect(url_for("error",msg=fill_in))
    else:
         mycursor = mydb.cursor()
        #  now = datetime.datetime.now()   #def datetime now()
         sql="INSERT INTO member(`name`,`username`,`password`)VALUES(%s,%s,%s)"
         val=(name,username,password)               
         # the value column must same with database  #insert now time
         mycursor.execute(sql,val)
         mydb.commit()  # push to database 
         return render_template("succeed.html",name=name) # send to succeed page


@app.route("/signin", methods=["POST"])
def signin():
    username=request.form["username"]   # get the form username & password
    password=request.form["password"] 

    mycursor = mydb.cursor(dictionary=True) 
    mycursor.execute('SELECT * FROM `member` WHERE `username` = %s AND `password` = %s AND `id` = id' , (username, password,)) 
# Fetch one record and return result
    member = mycursor.fetchone()
    if member:  # if  filter the username & password  
        session["username"] = member["username"]
        session["password"] = member["password"]
        session["id"]=member["id"]
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
    s_name=session.get("username",None) # use session s_name
     #get method judge have session id or not 
    if not s_name:
            return redirect(url_for("home"))
    else:
        mycursor = mydb.cursor()
        mycursor.execute("SELECT `username`, `content` FROM `member` INNER JOIN `message` ON `member`.id = `message`.`member_id`")
        dates=mycursor.fetchall()
        for data in dates:
            return render_template("member.html",s_name=s_name,dates=dates)


@app.route("/logout")    # set the logout to home.page
def logout():
        session.pop("username",None)
        return redirect(url_for("home"))


@app.route("/error") # receive msg show the query string
def error():
    msgs=request.args.get("msg")
    return render_template("error.html",msgs=msgs)


@app.route("/message",methods=["POST"])#msg blog
def message():
    msg_content=request.form ["message"]
    s_Id=session.get("id",None)
    s_name=session.get("username",None)

    mycursor=mydb.cursor()
    sql="INSERT INTO `message` (`member_id`,`content`) VALUE (%s,%s)"
    val=(s_Id,msg_content)
    mycursor.execute(sql,val)
    mydb.commit()

    mycursor.execute("SELECT `username`, `content` FROM `member` INNER JOIN `message` ON `member`.id = `message`.`member_id`")
    dates=mycursor.fetchall()
        
    for data in dates:
        return render_template("member.html",s_name=s_name,dates=dates)
        


app.run(port=3000)