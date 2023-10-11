from app import app
from functools import wraps
from flask import session
from flask import redirect , url_for , render_template , request , flash , jsonify
from model.dispatcher_modle import Dispatcher
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


obj = Dispatcher()

@app.route('/dispatcher_dashboard' , methods=["GET", "POST"])
@login_required('dispatcher')
def dispatcher_dashboard():
    if request.method == 'GET':
        dispatch_info = session.get('data')
        # flash(("Dear Dispatcher you succesfully Login !!!" , 'dispatcher_login_pass'))
        return render_template('//dispatcher_temp//dispatcher_dashboard.html' , dispatch_info = dispatch_info)



@app.route('/view_all_carear' , methods=["GET", "POST"])
@login_required('dispatcher')
def view_all_carear():
    if request.method == 'GET':
        dispatch_info = session.get('data')
        carear_info = obj.get_carear_info(dispatch_info[0]['user_pin'])
        return render_template('//dispatcher_temp//view_all_carear.html' , carear_info = carear_info , dispatch_info = dispatch_info)



@app.route('/popup_content_for_dispatcher')
def popup_content_for_dispatcher():
    # You can perform any processing here to generate the content and variable you want to display in the popup
    content = "This is the content of the popup returned from Flask."
    variable_to_return = "This is a variable returned from Flask."
    load_number = request.args.get('load_number')
    load_info = obj.get_just_load_from_db_from_form_view(load_number)
    return jsonify(content=content, variable = variable_to_return ,load_info = load_info)
    
    
@app.route('/save_load_info' , methods=["GET", "POST"])
@login_required('dispatcher')  
def save_load_info():
    if request.method == 'GET':
        dispatch_info = session.get('data')
        carear_info = obj.get_carear_info(dispatch_info[0]['user_pin'])
        return render_template('//dispatcher_temp//save_load_info.html' , dispatch_info = dispatch_info , carear_info = carear_info)
    if request.method == "POST":
        dispatch_info = session.get('data')
        load_info = request.form.to_dict()
        print("This is load_info = = " , load_info)
        if obj.store_load_info_in_db( load_info, dispatch_info[0]['user_pin']):
            flash(("your Load Information Saved succesfully !!!" , 'load_save_success'))
            return render_template('//dispatcher_temp//dispatcher_dashboard.html' , dispatch_info = dispatch_info)
        else:
            flash(("your Load Information could not Saved succesfully ERROR Try again !!!" , 'load_save_fail'))
            return render_template('//dispatcher_temp//dispatcher_dashboard.html' , dispatch_info = dispatch_info)
        

 
@app.route('/give_load_to_carear' , methods=["GET", "POST"])
@login_required('dispatcher')     
def display_give_load_to_carear():
    if request.method == 'GET':
        dispatch_info = session.get('data')
        carear_id = request.args.get('carear_id')
        carear_info = obj.get_carear_info_from_db_by_carear_id(carear_id)
        load_info = obj.get_given_load_to_the_carear(dispatch_info[0]['user_pin'] , carear_id )
        print("This is load info = " , load_info)
        return render_template("//dispatcher_temp//give_load_to_carear.html" , carear_info = carear_info , load_info = load_info , dispatch_info = dispatch_info)
    
    if request.method == "POST":
        dispatch_info = session.get('data')
        form_info = request.form.to_dict()
        carear_id = form_info['carear_id']
        load_number = form_info['load_number']
        carear_info = obj.store_load_and_carear_info_in_db(load_number ,carear_id, dispatch_info[0]['user_pin'] )
        flash(("You Deliver the Load Succesfully !!!" , 'load_deliver_success'))
        return render_template("//dispatcher_temp//dispatcher_dashboard.html" ,dispatch_info = dispatch_info)
            

      
@app.route('/display_sides' , methods=["GET", "POST"])
@login_required('dispatcher')              
def display_sides():
    if request.method == "GET":
        dispatch_info = session.get('data')
        return render_template("//dispatcher_temp//display_slides_in_web.html" , dispatch_info = dispatch_info)