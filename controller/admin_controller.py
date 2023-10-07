from app import app
from functools import wraps
from flask import session
from flask import redirect , url_for , render_template , request , flash ,jsonify
from model.admin_modle import Admin_Modle

import ast
from datetime import datetime, date
from collections import defaultdict

obj = Admin_Modle()

def login_required(role):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            if 'role' not in session or session['role'] != role:
                return redirect(url_for('login_page'))
            return func(*args, **kwargs)
        return wrapper
    return decorator



@app.route('/admin_dashboard' , methods=["GET", "POST"])
@login_required('admin')
def admin_dashboard():
    if request.method == 'GET':
        flash(("Dear Admin you succesfully Login !!!" , 'admim_login_pass'))
        return render_template('//admin_temp//admin_dashboard.html')
    
    
    
@app.route('/add_employee' , methods=["GET", "POST"])
@login_required('admin')
def add_employee():
    if request.method == 'GET':
        # flash(("Dear Admin you succesfully Login !!!" , 'admim_login_pass'))
        return render_template('//admin_temp//add_employee.html')
    if request.method == 'POST':
        data = request.form.to_dict()
        if data['user_type'] == "sale_man":
            obj.add_new_sale_man(data)
        elif data['user_type'] == "dispatcher":
            obj.add_new_dispatcher(data)
        else:
            flash(("Sorry the joining of new Employee Fails !!! " , 'new_employee_add_fails'))
            return render_template('//admin_temp//admin_dashboard.html')
            
        flash(("You Add the new Employee SuccessFully !!! " , 'new_employee_add_success'))
        return render_template('//admin_temp//admin_dashboard.html')
    
    
    
    
@app.route('/popup_content')
def popup_content():
    # You can perform any processing here to generate the content and variable you want to display in the popup
    content = "This is the content of the popup returned from Flask."
    variable_to_return = "This is a variable returned from Flask."
    career_id = request.args.get('careerId')
    career_info = obj.get_carear_data_from_db(career_id)
    print("This is info = " , career_info)
    print("This si carear inf = " , career_info['d_name'])
    # Returning a JSON response
    return jsonify(content=content, variable = variable_to_return ,career_info = career_info)



@app.route('/view_all_sales_of_all_sales_man', methods=["GET", "POST"])
@login_required('admin')  
def view_all_sales_of_all_sales_man():
    if request.method == "GET":
        all_sales_data = obj.get_all_sales_for_db()
        return render_template("//admin_temp//view_all_sales_of_all_sales_man.html" , all_sales_data = all_sales_data)



    
@app.route('/view_first_from_sales', methods=["GET", "POST"])
@login_required('admin')      
def view_first_from_sales():
    if request.method == "GET":
        all_sales_data = obj.get_first_form_sales_for_db()
        return render_template("//admin_temp//view_first_from_sales.html" , all_sales_data = all_sales_data)
    
    
    
@app.route('/transfer_carears_to_dispatcher', methods=["GET", "POST"])
@login_required('admin')     
def transfer_carears_to_dispatcher():
    if request.method == "GET":
        untransfer_sales_data = obj.get_untransfer_sales_data()
        dispatcher_info = obj.get_all_dispater_name_and_pin()
        info_length = len(dispatcher_info)
        print("This is no work")
        return render_template("//admin_temp//view_ustransfer_sales.html" , dispatcher_info = dispatcher_info , untransfer_sales_data = untransfer_sales_data , info_length = info_length)
    
    if request.method == "POST":
        
        dispater_carear_info = request.form.to_dict()

        print("This is check = " , dispater_carear_info)
        check = obj.insert_carear_id_and_dispatcher_pin_in_db(dispater_carear_info)
        untransfer_sales_data = obj.get_untransfer_sales_data()
        dispatcher_info = obj.get_all_dispater_name_and_pin()
        info_length = len(dispatcher_info)
        if check:
            flash(("This Carear is Forward Successfull !!!" , 'career_forward_success'))
            return render_template("//admin_temp//view_ustransfer_sales.html" , dispatcher_info = dispatcher_info , untransfer_sales_data = untransfer_sales_data , info_length = info_length)

        flash(("This Carear is Forward Fail !!!" , 'career_forward_fail'))
        return render_template("//admin_temp//view_ustransfer_sales.html" , dispatcher_info = dispatcher_info , untransfer_sales_data = untransfer_sales_data , info_length = info_length)
        
    


    
@app.route('/view_load_and_carear', methods=["GET", "POST"])
@login_required('admin')     
def view_load_and_carear():
    if request.method == 'GET':
        load_info = obj.get_load_info_from_db_for_admin()
        carear_info = obj.get_carear_info_from_db_for_admin()
        # carear_info = carear_info.reverse()
        zipped_data = zip(carear_info, load_info)
        return render_template("//admin_temp//view_load_and_carear_to_admin.html" , zipped_data = zipped_data)
    
    

            
            
# @app.route('/gernater_url_to_store_card_info', methods=["GET", "POST"])
# @login_required('admin')         
# def gernater_url_to_store_card_info():
#     if request.method == 'GET':
#         print("This card info ")
#         info = obj.get_carear_info_from_db_for_admin()
#         return render_template("//admin_temp//admin_dashboard.html"  , info = info)

from flask import render_template_string




@app.route('/gernater_url_to_store_card_info/<carear_id>', methods=["GET", "POST"])
def gernater_url_to_store_card_info(carear_id):
    if request.method == "GET":
        print("This is carear_id =  " , carear_id)
        return render_template("//admin_temp//add_new_card_info.html" , carear_id = carear_id)
    
    
@app.route('/stored_data', methods=["GET", "POST"]) 
def stored_card_info_in_db():
    if request.method == "POST":
        card_info = request.form.to_dict()
        obj.stored_card_info_in_db(card_info)
        print("card_info =", card_info)
        flash(("You uploaded the CARD Information Successfully!!!" , 'card_upload_success'))
        return render_template("//admin_temp//add_new_card_info.html")



@app.route('/view_card_records', methods=["GET", "POST"])
@login_required('admin')     
def view_card_records():
    if request.method == "GET":
        card_info = obj.get_card_data_from_db_to_display()
        return render_template("//admin_temp//view_card_records.html" , card_info = card_info)
            
        
@app.route('/view_pin_of_all_user', methods=["GET", "POST"])
@login_required('admin')     
def view_pin_of_all_user():
    if request.method == "GET":
        user_pins = obj.get_all_user_pin_from_db()
        print("this is user pin = " , user_pins)
        return render_template("//admin_temp//view_user_pin.html" , user_pins = user_pins)
            
        
# def get_url_for_card_info(self , carear_id):
