from flask import Flask,redirect,url_for,render_template,request,flash,session
from datetime import timedelta
from flask_sqlalchemy import SQLAlchemy

app=Flask(__name__)
app.secret_key="Neo123"
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///users.sqlite3'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"]=False
app.permanent_session_lifetime=timedelta(minutes=5)

db=SQLAlchemy(app)
class users(db.Model):
    _id=db.Column("id",db.Integer,primary_key=True)
    name=db.Column(db.String(100))
    email=db.Column(db.String(100))

    def __init__(self,name,email):#get variables we need to create objects
        self.name=name
        self.email=email


@app.route("/home")
def home():
    return render_template("index.html")

@app.route("/login",methods=["POST","GET"])
def login():
    if request.method=="POST":
        session.permanent=True
        user=request.form["nm"]
        session["user"]=user
        flash("Loging Succesful!")
        return redirect(url_for("user"))
    else:
        if "user" in session:
            flash("You are already login!")
            return  redirect(url_for("user"))
        return render_template("login.html")

@app.route("/user",methods=["POST","GET"])
def user():
    email=None
    if "user" in session:
        user=session["user"]
        if request.method=="POST":
            email=request.form["email"]
            session["email"]=email
            flash("your email was saved!")
        else:
            if "email" in session:
                email=session["email"]
        return render_template("user.html",email=email)
    else:
        flash("You are not logg in!")
        return redirect(url_for("login"))

@app.route("/logout")
def logout():
    flash("You have been logout!,{user}", "info")
    session.pop("user",None)
    session.pop("email",None)

    return redirect(url_for("login"))

if __name__=="__main__":
    db.create_all()
    app.run(debug=True)



