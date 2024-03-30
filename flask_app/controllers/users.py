from flask import Flask, render_template, redirect, request, session, flash
from flask_app import app
#importamos todos los modelos
from flask_app.models.user import User
from flask_app.models.appointment import Appointment
# importar contraseña
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/register', methods = ['POST'])
def register():
    if not User.validate_user(request.form):
        return redirect("/")
    
# encriptar de una contraseña
    pass_encrypt = bcrypt.generate_password_hash(request.form['password'])
    form ={
    "email" : request.form['email'],
    "password": pass_encrypt
    }
    new_id = User.save(form)
    session['user_id'] = new_id
    return redirect("/success")

@app.route('/success')
def success():
    if 'user_id' not in session:
        return redirect("/")
    form = {"id": session['user_id']}
    #guardar 
    user = User.get_by_id(form)
    
    return render_template("success.html", user=user)

@app.route("/login", methods=['POST'])
def login():
    user = User.get_by_email(request.form)
    if not user:
        flash("Email no registrado", "login")
        return redirect("/")
    
    if not bcrypt.check_password_hash(user.password, request.form['password']):
        flash("Password incorrecto", "login")
        return redirect("/")
    session['user_id'] = user.id
    return redirect("/success")

@app.route('/appointments')
def appointments():
    if 'user_id' not in session:
        return redirect("/")
    form = {"id": session['user_id']}
    user = User.get_by_id(form)
    #ACÁ
    my_appointments = Appointment.get_my_appointments(form)
    pass_appointments = Appointment.get_past_appointments(form)
    return render_template("appointments.html", user=user, my_appointments =my_appointments, pass_appointments = pass_appointments )

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")    