from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash

class Appointment:
    def __init__(self, data):
        self.id = data['id']
        self.tasks = data['tasks']
        self.date_task = data['date_task']
        self.status = data['status']
        self.user_id = data['user_id']
        #join con email
        self.email = data['email']

    @staticmethod
    def validate_appointment(form):
        is_valid = True

        if len(form['tasks']) < 3:
            flash('Debes ingresar la tarea a realizar con más de 3 caracteres', 'citas')
            is_valid = False
        
        if len(form['date_task']) == '':
            flash('Debes ingresar una fecha de la tarea', 'citas')
            is_valid = False
        
        if len(form['status']) < 1:
            flash("Debes elegir un estado")
            is_valid = False

        return is_valid
    
    @classmethod
    def save(cls, form):
        query = "INSERT INTO appointments(tasks, date_task, status, user_id) VALUES(%(tasks)s, %(date_task)s, %(status)s, %(user_id)s)"
        results = connectToMySQL('esquema_citas').query_db(query,form)
        return results;

    @classmethod
    def get_my_appointments(cls, form):
        query = "SELECT * FROM appointments JOIN users ON appointments.user_id = users.id WHERE appointments.user_id = %(id)s; "
        results = connectToMySQL('esquema_citas').query_db(query,form)
        my_appointment = []
        for appointment_row in results:
            my_appointment.append(cls(appointment_row))
        return my_appointment
    
    
    @classmethod
    def get_past_appointments(cls, form):
        query = "SELECT appointments.*, users.email FROM appointments JOIN users ON appointments.user_id = users.id  WHERE user_id = %(id)s AND status = 'missed' AND date_task < NOW();"
        results = connectToMySQL('esquema_citas').query_db(query,form)
        appointments_past_list = []
        for appointment_row in results:
            appointments_past_list.append(cls(appointment_row))
        return appointments_past_list
    
    @classmethod
    def update_appointment(cls, data):
        query = "UPDATE appointments SET tasks = %(tasks)s, date_task = %(date_task)s, status = %(status)s WHERE id = %(id)s"
        return connectToMySQL('esquema_citas').query_db(query, data)
    
    @classmethod
    def get_appointment_by_id(cls, data):
        query = "SELECT appointments.*, users.email FROM appointments JOIN users ON appointments.user_id = users.id WHERE appointments.id = %(id)s"
        result = connectToMySQL('esquema_citas').query_db(query, data)
        if result:
            return cls(result[0])
        return None
    
    @classmethod
    def delete_appointment(cls, data):
        query = "DELETE FROM appointments WHERE id = %(id)s"
        return connectToMySQL('esquema_citas').query_db(query, data)
