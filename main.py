from flask import Flask  , render_template , request , redirect , session , url_for
from markupsafe import escape
import mysql.connector as ms

db = ms.connect(
    host = "localhost" , 
    user = 'root' , 
    password = "" , 
    database = "book"
)

cr = db.cursor()

app = Flask(__name__) 

app.secret_key = "i live for this shit"

@app.route("/")
def home() :
    print(session['id'])
    return f"<h1> hello</h1> "


#SignUp Page
@app.route("/signup" , methods=[ "GET","POST"])
def SignUp(): 
    if request.method == 'POST' :
        #reciving data from form and inserting it to the database
        f , l , email , phone , city , P = request.form.get("First_Name") , request.form.get("Last_Name") , request.form.get("Email") , request.form.get("Phone_Number") , request.form.get("City") , request.form.get("Password")
        if len(l)==0 or len(f)==0 or len(email)==0 or len(phone)==0 or len(city)==0 or len(P)==0 : 
            return "404 Not Found"
        else :
            cr.execute(f'INSERT INTO `users` (`First_Name`, `Last_Name`, `Email`, `Phone_Number`, `City` , `Password`) Values ("{f}", "{l}", "{email}", "{phone}", "{city}" , "{P}" ) ')
            db.commit() 
            return redirect("/")
    return render_template("signup.html"  )

#Login Page 
@app.route("/login" , methods = ["GET" , "POST"])
def LogIn() :
    msg = ""
    if request.method =="POST" :
        Email , Password = request.form.get("Email") , request.form.get("Password")
        #Checking if the user exists and the email , password are correct
        cr.execute(f'SELECT * FROM users WHERE Email ="{Email}" AND Password = "{Password}" ')
        user = cr.fetchone()
        #logging IN
        print(user)
        if user : 
            session['loggedin'] = True
            session['id'] = user[0] 
            session['username'] = str(user[1])+"."+str(user[2])+str(user[0])
            print(session)
            return redirect(url_for("home"))
        else : 
            msg = "Email or Password Incorrect ! "
    return render_template("login.html"  , msg = msg )

@app.route('/logout')
def logout():
    # Remove session data, this will log the user out
   session.pop('loggedin', None)
   session.pop('id', None)
   session.pop('username', None)
   # Redirect to login page
   return redirect(url_for('LogIn'))
