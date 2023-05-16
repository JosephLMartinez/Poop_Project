from flask_app import app, Flask
from flask import render_template, redirect, session, request, flash
from flask_app.models.picker_upper import Picker_upper
from flask_app.models.puppy_parent import Puppy_parent
from flask_app.models.job import Job

# checks for existing appointments and directs you there or if none starts you on making a new one
@app.route("/puppy_parents")
def puppy_parent_page():
    if not session['user']:
        return redirect('/')
    if not Job.get_one(session['user']):
        return render_template("create_post.html")
    puppy_appointment=[Job.get_one(session['user'])]
    return render_template("status.html", puppy_appointment=puppy_appointment)

# it takes the info and sends it to jobs table in SQL
@app.route("/new_job_available", methods=["POST"])
def make_a_post():
    if not session['user']:
        return redirect('/')
    if not Job.validate_job_posting(request.form):
        print("flash message")
        return redirect('/puppy_parents')
    response="No"
    data={
        "puppy_parent_id":session['user'],
        "dog_name": request.form["dog_name"],
        "instructions": request.form["instructions"],
        "pickup_date": request.form['pickup_date'],
        "picker_upper_id":None,
        "finished":response
    }
    print(data['picker_upper_id'])
    Job.save(data)
    return redirect("/status")

# shows you the appointment you have
@app.route("/status")
def status():
    if not session['user']:
        return redirect('/')
    puppy_appointment= [Job.get_one(session['user'])]
    return render_template("status.html", puppy_appointment=puppy_appointment)

# if you want to change the date or need to change special instructions this is where you do it
@app.route("/edit_appointment/<int:num>")
# num isn't used here so I can delete it
def edit_appointment(num):
    if not session['user']:
        return redirect('/')
    puppy_appointment= [Job.get_one(session['user'])]
    return render_template("edit_appointment.html", puppy_appointment=puppy_appointment)

# takes the new info from the updated appointment and UPDATES IT
@app.route("/edit", methods=['POST'])
def add_appointment_changes():
    if not session['user']:
        return redirect('/')
    if not Job.validate_job_posting(request.form):
        print("flash message")
        puppy_appointment= [Job.get_one(session['user'])]
        return render_template("edit_appointment.html", puppy_appointment=puppy_appointment)
    data={
        "puppy_parent_id":session['user'],
        "dog_name": request.form["dog_name"],
        "instructions": request.form["instructions"],
        "pickup_date": request.form['pickup_date']
    }
    Job.update(data)
    return redirect("/status")
    
# it deletes the appointment when the customer changes their mind
@app.route("/delete_appointment")
def delete():
    if not session['user']:
        return redirect('/')
    Job.delete(session['user'])
    return redirect("/puppy_parents")

# shows them their scheduled appointments
@app.route("/picker_uppers")
def picker_upper_index():
    if not session['user']:
        return redirect('/')
    my_appointments=Job.get_all_of_mine(session['user'])
    return render_template("show_my_appointments.html", my_appointments=my_appointments)


# Where they find unclaimed appointments
@app.route("/appointments/new")
def unclaimed_appointments():
    if not session['user']:
        return redirect('/')
    available_appointments=Job.get_all()
    return render_template("available_appointments.html", available_appointments=available_appointments)

# claims the job and brings you back to your appointments
@app.route("/claim_job/<int:num>")
def claim_appointment(num):
    if not session['user']:
        return redirect('/')
    data={
        "id": num,
        "picker_upper_id":session['user']
    }
    Job.claim(data)
    my_appointments=Job.get_all_of_mine(session['user'])
    return render_template("show_my_appointments.html", my_appointments=my_appointments)

# when a picker_upper unselects an assignment it resposts to the unclaimed board
@app.route("/unselect/<int:num>")
def unselect(num):
    if not session['user']:
        return redirect('/')
    data={
        "id": num,
        # "picker_upper_id":session['user']
        "picker_upper_id":None

    }
    Job.unselect(data)
    my_appointments=Job.get_all_of_mine(session['user'])
    return render_template("show_my_appointments.html", my_appointments=my_appointments)

# when a picker_upper finishes an assignment it should show on the status screen for the client
@app.route("/finished_assignment/<int:num>")
def finished_assignment(num):
    if not session['user']:
        return redirect('/')
    response="Yes"
    data={
        "id": num,
        "finished":response
    }
    Job.finished_assignment(data)
    my_appointments=Job.get_all_of_mine(session['user'])
    return render_template("show_my_appointments.html", my_appointments=my_appointments)


@app.route("/picker_uppers/<int:num>")
def picker_upper_one_picker_upper(num):
    if not session['user']:
        return redirect('/')
    one_picker_upper =[Picker_upper.get_picker_upper(num)]
    return render_template("picker_upper_picker_upper.html", picker_uppers=one_picker_upper)



@app.route("/picker_uppers/<int:num>/edit")
def picker_upper_edit_screen(num):
    if not session['user']:
        return redirect('/')
    one_picker_upper= [Picker_upper.get_one(num)]
    return render_template("edit_picker_upper.html", the_picker_upper=one_picker_upper)

@app.route("/edit/<int:num>", methods=["POST"])
def edit_picker_upper(num):
    if not Picker_upper.validate_picker_upper(request.form):
        print("flash message")
        return redirect('/picker_uppers/new')
    data={
        "id":num,
        "puppy_parent_id":session['user'],
        "picker_upper_name": request.form["picker_upper_name"],
        "description": request.form["description"],
        "network": request.form['network'],
        "release_date": request.form['release_date']
    }
    Picker_upper.update(data)
    return redirect("/picker_uppers")


@app.route("/delete/<int:num>")
def delete_picker_upper(num):
    if not session['user']:
        return redirect('/')
    Picker_upper.delete(num)
    return redirect('/picker_uppers')


