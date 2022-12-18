from flask import Flask  , render_template , request , redirect , session , url_for
from markupsafe import escape
import mysql.connector as ms
from datetime import date 



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

@app.route("/add_book" , methods = ["POST" , "GET"])
def add_book() : 

    #ADDing a book only if the user is logged in by checking whether the session contains a user
    try : 
        if request.method == "POST" : 
            
            name , author = request.form.get("Name") , request.form.get("Author") 
            date_added , ownerid  = str(date.today()) , int(session["id"])
            print(name , author , date_added , ownerid)
            cr.execute(f'INSERT INTO book(Name , Author , Date_Added , OwnerId) VALUES("{name}" , "{author}" ,"{date_added}" , {ownerid})')
            db.commit()
            return redirect(url_for("home"))
    except :  
        return "It seems that you are not logged in <a href = '/login'>login</a>"
    return render_template("ADD.html")


@app.route("/books")
def books() :

    #Getting all books :: 
    cr.execute("SELECT Name , Author , Date_Added , OwnerId FROM book WHERE done=0")
    all = list(cr.fetchall())
    todos = []

    #changing the id of the owner to his first and last Name

    for i in all : 
        temp = []
        for j in range(len(i)) : 
            if(j == 2) : 
                temp.append(str(i[j]))
            elif j ==3 : 
                cr.execute(f'SELECT First_Name , Last_Name FROM users WHERE Id = {int(i[j])}')
                user = cr.fetchone()
                user = str(user[0] + user[1])
                temp.append(user)
            else : 
                temp.append(i[j])
        todos.append(temp)

    
    return render_template("books.html" , todos = todos)