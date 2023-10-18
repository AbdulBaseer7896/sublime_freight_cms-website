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
        notification_data = obj.get_notification_data_from_db()
        admin_info = session.get('data')
        return render_template('//admin_temp//admin_dashboard.html' , notification_data = notification_data , admin_info = admin_info)

    
@app.route('/add_employee' , methods=["GET", "POST"])
@login_required('admin')
def add_employee():
    if request.method == 'GET':
        admin_info = session.get('data')
        return render_template('//admin_temp//add_employee.html'  , admin_info = admin_info)
    if request.method == 'POST':
        data = request.form.to_dict()
        image_file = request.files['employee_photo']
        folder_name = 'employee_photo_folder'
        image_path = ""
        if image_file and image_file.filename:
            image_path = obj.stored_image_in_file_and_send_path_in_db(image_file , folder_name)
        else:
            image_path = ""
        if data['user_type'] == "sale_man":
            obj.add_new_sale_man(data , image_path)
        elif data['user_type'] == "dispatcher":
            obj.add_new_dispatcher(data  , image_path)
        else:
            flash(("Sorry the joining of new Employee Fails !!! " , 'new_employee_add_fails'))
            return redirect(url_for('admin_dashboard'))
            
        flash(("You Add the new Employee SuccessFully !!! " , 'new_employee_add_success'))
        return redirect(url_for('admin_dashboard'))
    
    
    
    
@app.route('/popup_content')
def popup_content():
    # You can perform any processing here to generate the content and variable you want to display in the popup
    content = "This is the content of the popup returned from Flask."
    variable_to_return = "This is a variable returned from Flask."
    career_id = request.args.get('careerId')
    career_info = obj.get_carear_data_from_db(career_id)
    # Returning a JSON response
    return jsonify(content=content, variable = variable_to_return ,career_info = career_info)



@app.route('/view_all_sales_of_all_sales_man', methods=["GET", "POST"])
@login_required('admin')  
def view_all_sales_of_all_sales_man():
    if request.method == "GET":
        all_sales_data = obj.get_all_sales_for_db()

        
        print("This is all sales data  = " , all_sales_data)

        
        head_light = request.args.get('head_light')
        obj.remore_the_nofiticatin_form_db_for_sales(head_light)
        admin_info = session.get('data')
        return render_template("//admin_temp//view_all_sales_of_all_sales_man.html" , all_sales_data = all_sales_data , head_light = head_light , admin_info = admin_info)



    
@app.route('/view_first_from_sales', methods=["GET", "POST"])
@login_required('admin')      
def view_first_from_sales():
    if request.method == "GET":
        all_sales_data = obj.get_first_form_sales_for_db()
        admin_info = session.get('data')
        return render_template("//admin_temp//view_first_from_sales.html" , all_sales_data = all_sales_data , admin_info = admin_info) 
    
    
    
@app.route('/transfer_carears_to_dispatcher', methods=["GET", "POST"])
@login_required('admin')     
def transfer_carears_to_dispatcher():
    if request.method == "GET":
        admin_info = session.get('data')
        untransfer_sales_data = obj.get_untransfer_sales_data()
        dispatcher_info = obj.get_all_dispater_name_and_pin()
        info_length = len(dispatcher_info)
        return render_template("//admin_temp//view_ustransfer_sales.html" , dispatcher_info = dispatcher_info , untransfer_sales_data = untransfer_sales_data , info_length = info_length , admin_info = admin_info)
    
    if request.method == "POST":
        admin_info = session.get('data')
        
        dispater_carear_info = request.form.to_dict()
        check = obj.insert_carear_id_and_dispatcher_pin_in_db(dispater_carear_info)
        untransfer_sales_data = obj.get_untransfer_sales_data()
        dispatcher_info = obj.get_all_dispater_name_and_pin()
        info_length = len(dispatcher_info)
        if check:
            flash(("This Carear is Forward Successfull !!!" , 'career_forward_success'))
            return render_template("//admin_temp//view_ustransfer_sales.html" , dispatcher_info = dispatcher_info , untransfer_sales_data = untransfer_sales_data , info_length = info_length , admin_info = admin_info)

        flash(("This Carear is Forward Fail !!!" , 'career_forward_fail'))
        return render_template("//admin_temp//view_ustransfer_sales.html" , dispatcher_info = dispatcher_info , untransfer_sales_data = untransfer_sales_data , info_length = info_length , admin_info = admin_info)
        
    


    
@app.route('/view_load_and_carear', methods=["GET", "POST"])
@login_required('admin')     
def view_load_and_carear():
    if request.method == 'GET':
        admin_info = session.get('data')
        load_info = obj.get_load_info_from_db_for_admin()
        carear_info = obj.get_carear_info_from_db_for_admin()
        # carear_info = carear_info.reverse()
        zipped_data = zip(carear_info, load_info)
        return render_template("//admin_temp//view_load_and_carear_to_admin.html" , zipped_data = zipped_data , admin_info = admin_info)
    
    


@app.route('/gernater_url_to_store_card_info/<carear_id>', methods=["GET", "POST"])
def gernater_url_to_store_card_info(carear_id):
    if request.method == "GET":
        admin_info = session.get('data')
        return render_template("//admin_temp//add_new_card_info.html" , carear_id = carear_id , admin_info = admin_info)
    
    
@app.route('/stored_data', methods=["GET", "POST"]) 
def stored_card_info_in_db():
    if request.method == "POST":
        admin_info = session.get('data')
        card_info = request.form.to_dict()
        obj.stored_card_info_in_db(card_info)
        flash(("You uploaded the CARD Information Successfully!!!" , 'card_upload_success'))
        return render_template("//admin_temp//add_new_card_info.html" , admin_info = admin_info)



@app.route('/view_card_records', methods=["GET", "POST"])
@login_required('admin')     
def view_card_records():
    admin_info = session.get('data')
    if request.method == "GET":
        card_info = obj.get_card_data_from_db_to_display()
        return render_template("//admin_temp//view_card_records.html" , card_info = card_info , admin_info = admin_info)
            
        
@app.route('/view_pin_of_all_user', methods=["GET", "POST"])
@login_required('admin')     
def view_pin_of_all_user():
    admin_info = session.get('data')
    if request.method == "GET":
        user_pins = obj.get_all_user_pin_from_db()
        disable_user_pins = obj.get_all_disable_user_pin_from_db()
        return render_template("//admin_temp//view_user_pin.html" , user_pins = user_pins , disable_user_pins = disable_user_pins , admin_info = admin_info)
            




@app.route('/search_carear_for_admin_for_seach' , methods=["GET", "POST"])
@login_required('admin')
def search_carear_for_admin_for_seach():
    if request.method == 'POST':
        admin_info = session.get('data')
        search_text = request.form.get("search_text")
        all_sales_data_for_search = obj.get_first_form_sales_for_db_for_admin_search(search_text)
        return render_template("//admin_temp//view_all_sales_of_all_sales_man.html" , all_sales_data = all_sales_data_for_search , admin_info = admin_info)
    
    
    
    

@app.route('/disable_the_user' , methods=["GET", "POST"])
@login_required('admin')
def disable_the_user():
    if request.method == 'GET':
        user_pin = request.args.get('user_pin')
        if obj.disable_the_user_from_db(user_pin):
            flash(('You Succesfully Disabe The User !!!' , 'disable_success'))
            return redirect(url_for('view_pin_of_all_user'))
        else:
            flash(('Sorry The User Will Not Disable Try Again !!!' , 'disable_fail'))
            return redirect(url_for('view_pin_of_all_user'))
        
        
        

@app.route('/enable_the_user' , methods=["GET", "POST"])
@login_required('admin')
def enable_the_user():
    if request.method == 'GET':
        user_pin = request.args.get('user_pin')
        if obj.enable_the_user_from_db(user_pin):
            flash(('You Succesfully Enable The User !!!' , 'enable_success'))
            return redirect(url_for('view_pin_of_all_user'))
        else:
            flash(('Sorry The User Will Not enable Try Again !!!' , 'enable_fail'))
            return redirect(url_for('view_pin_of_all_user'))
        
        

@app.route('/view_all_appoinments_of_all_sales_man' , methods=["GET", "POST"])
@login_required('admin')
def view_all_appoinments_of_all_sales_man():
    if request.method == 'GET':
        admin_info = session.get('data')
        appointment_data = obj.get_appointment_data_from_db()
        head_light = request.args.get('head_light')
        obj.remore_the_nofiticatin_form_db_for_appointment(head_light)
        return render_template("admin_temp/view_all_appoinments.html" ,appointment_data = appointment_data  , head_light = head_light , admin_info = admin_info)
    
    
    
@app.route('/update_the_appoinments_by_admin' , methods=["GET", "POST"])
@login_required('admin')
def update_the_appoinments_by_admin():
    if request.method == "GET":
        admin_info = session.get('data')
        appointment_id = request.args.get('appointment_id')
        print("This is important = " , appointment_id)
        appointment_info = obj.get_appointment_info_from_db(appointment_id)
        return render_template("admin_temp/up_date_appoiment.html" , appointment_info = appointment_info , admin_info = admin_info)
    
    if request.method == "POST":
        update_data = request.form.to_dict()
        obj.update_the_appoinments_from_db(update_data)
        return redirect(url_for('view_all_appoinments_of_all_sales_man'))
        
    
@app.route('/delete_the_appoinments_by_admin' , methods=["GET", "POST"])
@login_required('admin')  
def delete_the_appoinments_by_admin():
    if request.method == "GET":
        appointment_id = request.args.get("appointment_id")
        obj.delete_the_appointment_from_db(appointment_id)
        return redirect(url_for("view_all_appoinments_of_all_sales_man"))
    
    
    
    
@app.route('/delete_the_sales_by_admin' , methods=["GET", "POST"])
@login_required('admin')  
def delete_the_sales_by_admin():
    if request.method == "GET":
        carear_id = request.args.get("carear_id")
        obj.delete_the_sales_from_db(carear_id)
        return redirect(url_for("view_all_sales_of_all_sales_man"))