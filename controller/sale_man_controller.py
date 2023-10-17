from app import app
from functools import wraps
from flask import session
from flask import redirect , url_for , render_template , request , flash , jsonify
from model.sale_man_modle import Sale_Man_Modle
import json

import ast
from datetime import datetime, date
from collections import defaultdict


def login_required(role):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            if 'role' not in session or session['role'] != role:
                return redirect(url_for('login_page'))
            return func(*args, **kwargs)
        return wrapper
    return decorator


obj = Sale_Man_Modle()

@app.route('/sale_dashboard' , methods=["GET", "POST"])
@login_required('sale_man')
def sale_dashboard():
    if request.method == 'GET':
        sale_man_info = session.get('data')
        # flash(("Dear Sale Man you succesfully Login !!!" , 'sale_login_pass'))
        return render_template('//sale_temp//sale_dashboard.html' ,sale_man_info = sale_man_info)



@app.route('/new_sale' , methods=["GET", "POST"])
@login_required('sale_man')
def new_sale():
    if request.method == 'GET':
        sale_man_info = session.get('data')
        return render_template("//sale_temp//new_sale.html" , carear_info = "" , sale_man_info = sale_man_info)
    if request.method == 'POST':
        form_data = request.form.to_dict()
        sale_man_info = session.get('data')
        print("This is form_data = " , form_data)
        print("This is id = " , sale_man_info[0]['user_pin'])
        obj.new_sales_first_time(form_data , sale_man_info[0]['user_pin'])
        flash(("congratulations you Done new Sale!!!" , 'new_sale_success'))
        return redirect(url_for("sale_dashboard"))
    
    
    
@app.route('/popup_content_for_sale_man')
def popup_content_for_sale_man():
    # You can perform any processing here to generate the content and variable you want to display in the popup
    content = "This is the content of the popup returned from Flask."
    variable_to_return = "This is a variable returned from Flask."
    career_id = request.args.get('careerId')
    career_info = obj.carear_info_for_carear_id(career_id)
    # Returning a JSON response
    return jsonify(content=content, variable = variable_to_return ,career_info = career_info)

@app.route('/view_all_sales' , methods=["GET", "POST"])
@login_required('sale_man')
def view_all_sales():
    if request.method == "GET":
        sale_man_info = session.get('data')
        sales_data = obj.get_sale_man_sales(sale_man_info[0]['user_pin'])
        return render_template("//sale_temp//view_all_sales.html" , sales_data = sales_data , sale_man_info = sale_man_info)
    
    
@app.route('/update_carear_info', methods=["GET", "POST"])
@login_required('sale_man')
def update_carear_info():
    if request.method == "GET":
        carear_id = request.args.get('carear_id')
        sale_man_info = session.get('data')
        carear_info = obj.carear_info_for_carear_id(carear_id)
        return render_template("//sale_temp//new_sale.html", carear_info=carear_info , sale_man_info = sale_man_info)
    
    
    


@app.route('/new_appointment' , methods=["GET", "POST"])
@login_required('sale_man')
def new_appointment():
    if request.method == 'GET':
        sale_man_info = session.get('data')
        return render_template("//sale_temp//new_appointment.html" , appointment_info = "" , sale_man_info = sale_man_info)
    if request.method == 'POST':
        form_data = request.form.to_dict()
        sale_man_info = session.get('data')
        print("This is form_data = " , form_data)
        obj.add_new_appointment_in_db(form_data , sale_man_info[0]['user_pin'])
        flash(("congratulations your new appointment Added!!!" , 'new_appointment_success'))
        return redirect(url_for("sale_dashboard"))
    
    
    
@app.route('/view_all_appointments' , methods=["GET", "POST"])
@login_required('sale_man')
def view_all_appointments():
    if request.method == "GET":
        sale_man_info = session.get('data')
        appointment_data = obj.get_sales_man_appointment_from_db(sale_man_info[0]['user_pin'])
        print("this data = " , appointment_data)
        return render_template("//sale_temp//view_all_appointment.html" , appointment_data = appointment_data , sale_man_info = sale_man_info)
    

@app.route('/popup_content_for_sale_man_to_display_appointments')
def popup_content_for_sale_man_to_display_appointments():
    # You can perform any processing here to generate the content and variable you want to display in the popup
    content = "This is the content of the popup returned from Flask."
    variable_to_return = "This is a variable returned from Flask."
    career_id = request.args.get('careerId')
    appointment_info = obj.appointment_info_for_appointment_id(career_id)
    # Returning a JSON response
    return jsonify(content=content, variable = variable_to_return ,appointment_info = appointment_info)




@app.route('/search_carear_for_sales_man' , methods=["GET", "POST"])
@login_required('sale_man')
def search_carear_for_sales_man():
    if request.method == 'POST':
        sale_man_info = session.get('data')
        search_text = request.form.get("search_text")
        print("This is search = " , search_text)
        sales_data = obj.get_sale_man_sales_for_search_text(sale_man_info[0]['user_pin'] , search_text)
        return render_template("//sale_temp//view_all_sales.html" , sales_data = sales_data , sale_man_info = sale_man_info)
    
    
    
    
@app.route('/view_all_appointments_for_search' , methods=["GET", "POST"])
@login_required('sale_man')
def view_all_appointments_for_search():
    if request.method == "POST":
        sale_man_info = session.get('data')
        search_text = request.form.get("search_text")
        print("This is search text = " , search_text)
        appointment_data = obj.get_sales_man_appointment_from_db_for_search(sale_man_info[0]['user_pin'] , search_text)
        print("this data = " , appointment_data)
        return render_template("//sale_temp//view_all_appointment.html" , appointment_data = appointment_data , sale_man_info = sale_man_info)
    
    
    
    
    
@app.route('/update_the_appoinment' , methods=["GET", "POST"])
@login_required('sale_man')              
def update_the_appoinment():
    if request.method == "GET":
        appointment_id = request.args.get('appointment_id')
        sale_man_info = session.get('data')
        appointment_info = obj.get_appointment_data_from_db_by_appointment_id(appointment_id)
        print("This is appo id = " , appointment_info)
        return render_template("//sale_temp//new_appointment.html" , appointment_info = appointment_info , sale_man_info = sale_man_info)
    if request.method == "POST":
        form_data = request.form.to_dict()
        print("This is form data = " , form_data)
        sale_man_info = session.get('data')
        flash(("you Successfully Update The Appointment!!!" , 'appointment_update_success'))
        return redirect(url_for("sale_dashboard"))
    
    