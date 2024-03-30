from flask import render_template, redirect, session, request
from flask_app import app
#import models de ambas tablas
from flask_app.models.user import User
from flask_app.models.appointment import Appointment

@app.route('/add')
def add_appointments():
    if 'user_id' not in session:
        return redirect('/')
    viaje = {"id" : session['user_id']}
    user = User.get_by_id(viaje)
    return render_template('add_appointments.html', user=user)

@app.route('/new/appointment', methods =['POST'])
def appointment_add():
    if 'user_id' not in session: #comprobar inicio de sesión
        return redirect('/')
    
    #validacion del registro de viajes
    if not Appointment.validate_appointment(request.form):
        return redirect('/new/appointment')
    
    # guardar viaje
    Appointment.save(request.form)
    return redirect('/appointments')

@app.route('/edit/<int:id>')
def edit_appointment(id):
    if 'user_id' not in session:
        return redirect('/')
    data = {
        "id": id
    }
    appointment = Appointment.get_appointment_by_id(data)
    if not appointment:
        return redirect('/appointments')
    # Formatear la fecha antes de pasarla a la plantilla
    appointment.date_task = appointment.date_task.strftime('%Y-%m-%d')
    return render_template('edit_appointments.html', appointment=appointment)

@app.route('/update/appointment/<int:id>', methods=['POST'])
def update_appointment(id):
    if 'user_id' not in session:
        return redirect('/')
    if not Appointment.validate_appointment(request.form):
        return redirect(f'/edit/{id}')
    if 'tasks' in request.form and 'date_task' in request.form and 'status' in request.form:
        data = {
            "id": id,
            "tasks": request.form['tasks'],
            "date_task": request.form['date_task'],
            "status": request.form['status']
        }
        Appointment.update_appointment(data)
    return redirect('/appointments')

@app.route('/delete/<int:id>')
def delete_appointment(id):
    if 'user_id' not in session:
        return redirect('/')
    data = {
        "id": id
    }
    Appointment.delete_appointment(data)
    return redirect('/appointments')
