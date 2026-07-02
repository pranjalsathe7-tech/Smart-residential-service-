from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__,template_folder="template")

users = []


#home page
@app.route("/")
def home():
    return render_template("home.html")


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        role = request.form.get('role')

        # Demo check
        if email == "admin@gmail.com" and password == "1234":
            return f"Login Success as {role}"
        else:
            return "Invalid Login"

    return render_template('login.html')


# REGISTER PAGE (GET + POST)
@app.route("/Registration", methods=["GET", "POST"])
def register():

    if request.method == "POST":
        first_name = request.form.get("first_name")
        last_name = request.form.get("last_name")
        email = request.form.get("email")
        password = request.form.get("password")

        # just print (you can save to DB later)
        print(first_name, last_name, email, password)

        return redirect(url_for("login"))

    return render_template("Registration.html")

# SERVICES
services_list = ["Plumbing", "Electrician", "Cleaning", "Security"]

@app.route("/services")
def services():
    return render_template("services.html", services=services_list)

#  AVAILABLE SERVICES
@app.route("/available")
def availabl():
    return render_template("available.html", services=services)


#USER DASHBOARD
@app.route("/user")
def user():
    return render_template("user_dashboard.html")


#  ADMIN DASHBOARD 
@app.route("/admin")
def admin():
    return render_template("admin.html", users=users)


# PROFILE
@app.route("/profile")
def profile():
    return render_template("profile.html")


# SERVICE MANAGEMENT
@app.route("/Service_Management")
def Servicem():
   return render_template("Service_Management.html")


#  RESULT PAGE 
@app.route("/result")
def result():
    return render_template("result.html")



if __name__ == "__main__":
    app.run(debug=True)