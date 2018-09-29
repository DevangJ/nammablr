from flask import Flask, render_template, request, redirect, session, url_for, flash
import pyrebase # For firebase connectivity

config = {
    "apiKey": "AIzaSyCF8tAp52fwp1bYg0vc4Tgc_17NpTJLqzo",
    "authDomain": "nammablrfb.firebaseapp.com",
    "databaseURL": "https://nammablrfb.firebaseio.com",
    "storageBucket": "nammablrfb.appspot.com",
}
firebase = pyrebase.initialize_app(config)
db = firebase.database()
auth = firebase.auth()


app = Flask(__name__)
app.secret_key = 'nammablrsecretkey'


@app.route("/")
def main_page():
    return render_template("goto_resp_apps.html")

@app.route("/login", methods=["POST","GET"])
def user_login_page():
    if request.method=="GET":
        return render_template("login.html")
    else:
        username = request.form["username"]
        password = request.form["password"]
        try:
            user = auth.sign_in_with_email_and_password(username, password)
        except:
            return render_template("login.html",msg="Wrong Credentials Pal!")
        # print(user)
        session["user"] = user
        return redirect("/ua")

@app.route('/logout')
def user_logout():
    session.clear()
    return redirect("/login")


@app.route("/signup", methods=["POST", "GET"])
def signup_page():
    if request.method=="GET":
        return render_template("signup.html")
    else:
        username = request.form["username"]
        if request.form["password"] != request.form["password2"]:
            return render_template("signup.html",msg="Please Enter Same Passwords")
        password = request.form["password"]
        auth.create_user_with_email_and_password(username, password)
        return redirect("/login")

@app.route('/ua')
def home_user_page():
    if "user" in session:
        req = db.child("requests").get().val()
        return render_template("ua/home.html",user = session["user"], markers=req)
    else:
        return redirect("/login")

@app.route("/request_truck", methods=["GET","POST"])
def request_truck_page():
    if request.method=="GET":
        return render_template("ua/request_truck_page.html")
    else:
        lat = request.form["lat"]
        lng = request.form["lng"]
        user_email = session["user"]["email"]
        db.child("requests").push({"lat":lat,"lng":lng,"user":user_email})
        # add to db
        return redirect('/ua')

@app.route("/ua/profile")
def profile_page():
	req = db.child("requests").get().val()
	return render_template("ua/profile.html", user = session["user"], req=req)






@app.route('/aa')
def home_admin_page():
    req = db.child("requests").get().val()
    return render_template("aa/main-view.html",markers=req)


@app.route("/aa/rlist")
def requests_admin_page():
    return render_template("aa/rlist.html",req = db.child("requests").get().val())

@app.route('/aa/stats')
def stats():
	req = db.child("requests").get().val()
	return render_template("aa/stat.html", req=req)
# Admin app ends
@app.route('/aa/visual', methods=["GET","POST"])
def visual():
	if request.method == "POST":
		flash('hello', 'success')
	return render_template("visual.html")



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)
