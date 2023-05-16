from flask_app import app, Flask
from flask import render_template, redirect, session, request, flash
from flask_app.models.puppy_parent import Puppy_parent
from flask_app.models.picker_upper import Picker_upper
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

#everyton starts here
@app.route("/")
def puppy_parent_index():
    # going back to first page automatically logs you out
    session['user']=False
    session['my_name']=False
    return render_template("first_page.html")

# preexisting users
@app.route("/sign_in")
def sign_in():
    # going to sign_in page automatically logs you out
    session['user']=False
    session['my_name']=False
    return render_template("sign_in.html")

# what kind of new user?
@app.route("/new_user")
def new_user():
    return render_template("new_user.html")

# new customer
@app.route("/new_puppy_parent")
def new_puppy_parent():
    return render_template("create_puppy_parent.html")

# new employee
@app.route("/new_picker_upper")
def new_picker_upper():
    return render_template("create_picker_upper.html")

# adds customer to the system
@app.route("/create_puppy_parent", methods= ['POST'])
def create_puppy_parent():
    if not Puppy_parent.validate_puppy_parent(request.form):
        print("flash message")
        return redirect('/new_puppy_parent')
    puppy_parent_in_system= Puppy_parent.get_by_email(request.form['email'])
    if puppy_parent_in_system:
        flash('Account already exists please sign in')
        return redirect('/sign_in')
    data={
        "first_name":request.form['first_name'],
        "last_name":request.form['last_name'],
        "email":request.form['email'],
        "password": bcrypt.generate_password_hash(request.form['password'])
    }
    puppy_parent=Puppy_parent.save(data)
    session['user']=puppy_parent
    puppy_parent_name=Puppy_parent.get_one(puppy_parent)
    session['my_name']=puppy_parent_name[0]['first_name']
    print(puppy_parent)
    return redirect("/puppy_parents")


# adds employee to the system
@app.route("/create_picker_upper", methods= ['POST'])
def create_picker_upper():
    if not Picker_upper.validate_picker_upper(request.form):
        print("flash message")
        return redirect('/new_picker_upper')
    picker_upper_in_system= Picker_upper.get_by_email(request.form['email'])
    if picker_upper_in_system:
        flash('Account already exists please sign in')
        return redirect('/sign_in')
    data={
        "first_name":request.form['first_name'],
        "last_name":request.form['last_name'],
        "email":request.form['email'],
        "password": bcrypt.generate_password_hash(request.form['password'])
    }
    picker_upper=Picker_upper.save(data)
    session['user']=picker_upper
    picker_upper_name=Picker_upper.get_one(picker_upper)
    session['my_name']=picker_upper_name[0]['first_name']
    print(picker_upper)
    return redirect("/picker_uppers")


# login for both
@app.route('/login', methods=['POST'])
def login():
    puppy_parent_in_system= Puppy_parent.get_by_email(request.form['email'])

    if not puppy_parent_in_system:
        picker_upper_in_system=Picker_upper.get_by_email(request.form['email'])
        if not picker_upper_in_system:
            flash('Invalid Email/Password')
            return redirect('/sign_in')
        if not bcrypt.check_password_hash(picker_upper_in_system.password, request.form['password']):
            flash("Invalid Email/Password")
            return redirect('/sign_in')
        picker_upper_name=Picker_upper.get_one(picker_upper_in_system.id)
        session['my_name']=picker_upper_name[0]['first_name']
        session['user']=picker_upper_in_system.id
        return redirect("/picker_uppers")
    if not bcrypt.check_password_hash(puppy_parent_in_system.password, request.form['password']):
        flash("Invalid Email/Password")
        return redirect('/login')
    puppy_parent_name=Puppy_parent.get_one(puppy_parent_in_system.id)
    session['my_name']=puppy_parent_name[0]['first_name']
    session['user']= puppy_parent_in_system.id
    return redirect("/puppy_parents")


# logout
@app.route('/logout')
def logout():
    session['user']=False
    session['my_name']=False
    return redirect('/')

