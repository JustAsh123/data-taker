from flask import Flask, render_template, redirect, url_for, session,request, flash
from flask_sqlalchemy import SQLAlchemy

app =Flask(__name__)
app.secret_key = "Sup"
app.config['SQLAlchemy_DATABASE_URI'] = 'sqlite:///users.sqlite3'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

class users(db.Model):
	_id = db.Column("id",db.Integer, primary_key = True)
	name = db.Column(db.String(100))
	email = db.Column(db.String(100))     

	def __init__(self, name,email):
		self.name = name
		self.email = email

@app.route("/")
def home():
	return render_template("index.html")

@app.route("/view")
def view():
	return render_template("view.html", values=users.query.all())

@app.route("/login", methods=["GET","POST"])
def login():
	if request.method == "POST":
		user = request.form['nm']
		session["user"] = user
		found_user = users.query.filter_by(name=user).first()
		if found_user:
			session["email"] = found_user.email
		else:
			usr = users(user,"")
			db.session.add(usr)
			db.session.commit()

		flash("Logged in successfully!","info")
		return redirect(url_for("user"))
	else:
		if "user" in session:
			flash("You are already logged in!","info")
			return redirect(url_for("user"))
		return render_template("login.html")

@app.route("/user", methods=["POST","GET"])
def user():
	email = None
	if "user" in session:
		user = session["user"]
		if request.method == "POST":
			email = request.form["email"]
			session["email"] = email
			found_user = users.query.filter_by(name=user).first()
			found_user.email = email
			db.session.commit()
			flash("Email saved!","info")
		else:
			if "email" in session:
				email = session["email"]
		return render_template("user.html", email=email)
	else:
		flash("You need to login first!",None)
		return redirect(url_for("login"))

@app.route("/logout")
def logout():
	if "user" in session:
		user = session["user"]
		flash("You have been logged out!","info")
	else:
		flash("You are not logged in!",None)
	session.pop("user",None)
	session.pop("email",None)
	return redirect(url_for("login"))

if __name__ == '__main__':
	db.create_all()
	app.run(debug=True)