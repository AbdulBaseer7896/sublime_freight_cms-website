from app import app
from functools import wraps
from flask import session
from flask import redirect , url_for , render_template , request , flash ,jsonify
from model.admin_modle import Admin_Modle
import json
import ast
from datetime import datetime, date ,  timedelta
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
        data = obj.get_all_invoice_data_from_db()
        admin_info = session.get('data')
        income_data = calculate_data_for_dashboard()
        return render_template('//admin_temp//admin_dashboard.html' , notification_data = notification_data , income_data= income_data , invoice_info = data,  admin_info = admin_info)
    
    
    
from datetime import date, datetime, timedelta

def calculate_data_for_dashboard():
    data = obj.get_all_invoice_data_from_db()
    result = {}

    # Calculate today's income
    today = date.today()
    today_data = [entry for entry in data if 'load_rate' in entry and 'invoic_input_date' in entry and entry['invoic_input_date'].date() == today]
    today_income = sum(int(entry['load_rate'].replace('$', '').replace(',', '')) for entry in today_data)

    result['today_income'] = today_income

    # Calculate this week's income
    start_of_week = today - timedelta(days=today.weekday())
    end_of_week = start_of_week + timedelta(days=6)
    this_week_data = [entry for entry in data if 'load_rate' in entry and 'invoic_input_date' in entry and start_of_week <= entry['invoic_input_date'].date() <= end_of_week]
    total_income_this_week = sum(int(entry['load_rate'].replace('$', '').replace(',', '')) for entry in this_week_data)
    result['this_week_income'] = total_income_this_week

    # Calculate this month's income
    start_of_month = today.replace(day=1)
    end_of_month = (today.replace(day=28) + timedelta(days=4)).replace(day=1) - timedelta(days=1)
    this_month_data = [entry for entry in data if 'load_rate' in entry and 'invoic_input_date' in entry and start_of_month <= entry['invoic_input_date'].date() <= end_of_month]
    total_income_this_month = sum(int(entry['load_rate'].replace('$', '').replace(',', '')) for entry in this_month_data)
    result['this_month_income'] = total_income_this_month

    # Calculate this year's income
    start_of_year = today.replace(month=1, day=1)
    end_of_year = today.replace(month=12, day=31)
    this_year_data = [entry for entry in data if 'load_rate' in entry and 'invoic_input_date' in entry and start_of_year <= entry['invoic_input_date'].date() <= end_of_year]
    total_income_this_year = sum(int(entry['load_rate'].replace('$', '').replace(',', '')) for entry in this_year_data)
    result['this_year_income'] = total_income_this_year

    return result

    
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
            return redirect(url_for('transfer_carears_to_dispatcher'))
        flash(("This Carear is Forward Fail !!!" , 'career_forward_fail'))
        return redirect(url_for('transfer_carears_to_dispatcher'))
    
    

    
    


    
@app.route('/view_load_and_carear', methods=["GET", "POST"])
@login_required('admin')     
def view_load_and_carear():
    if request.method == 'GET':
        admin_info = session.get('data')
        load_info = obj.get_load_info_from_db_for_admin()
        return render_template("//admin_temp//view_load_and_carear_to_admin.html" , load_info = load_info , admin_info = admin_info)
    
    


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
            







    
@app.route('/search_appoimtment_for_admin_for_seach' , methods=["GET", "POST"])
@login_required('admin')
def search_appoimtment_for_admin_for_seach():
    if request.method == 'POST':
        admin_info = session.get('data')
        search_text = request.form.get("search_text")
        if search_text == '':
            return redirect(url_for('view_all_appoinments_of_all_sales_man'))
        appointment_data = obj.get_appoiments_for_db_for_admin_search(search_text)
        head_light = ""
        return render_template("admin_temp/view_all_appoinments.html" ,appointment_data = appointment_data  , head_light = head_light , admin_info = admin_info)
    
    
    
@app.route('/search_carear_for_admin_for_seach' , methods=["GET", "POST"])
@login_required('admin')
def search_carear_for_admin_for_seach():
    if request.method == 'POST':
        admin_info = session.get('data')
        search_text = request.form.get("search_text")
        if search_text == '':
            return redirect(url_for('view_all_sales_of_all_sales_man'))
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
    
    
    
@app.route('/search_mc_number_for_admin' , methods=["GET", "POST"])
@login_required('admin')     
def search_mc_number_for_admin():
    if request.method == "POST":
        admin_info = session.get('data')
        notification_data = obj.get_notification_data_from_db()

        ms_number = request.form.to_dict()
        ms_number = ms_number['mc_for_search']
        return render_template('//admin_temp//admin_dashboard.html' , notification_data = notification_data , admin_info = admin_info , ms_number = ms_number)


@app.route('/admin_view_all_notifications' , methods=["GET", "POST"])
@login_required('admin')     
def admin_view_all_notifications():
    if request.method == "GET":
        mark_all_notification = obj.mark_all_notification_readed()
        if mark_all_notification:
            return redirect(url_for('admin_dashboard'))
        else:
            return redirect(url_for('admin_dashboard'))
            
            


    
@app.route('/search_load_for_admin_seach' , methods=["GET", "POST"])
@login_required('admin')
def search_load_for_admin_seach():
    if request.method == 'POST':
        admin_info = session.get('data')
        search_text = request.form.get("search_text")
        if search_text == '':
            return redirect(url_for('view_load_and_carear'))
        load_info = obj.get_load_from_search_data_for_admin(search_text)
        return render_template("//admin_temp//view_load_and_carear_to_admin.html" , load_info = load_info , admin_info = admin_info)



@app.route('/show_dispatcher_and_there_load' , methods=["GET", "POST"])
@login_required('admin')
def show_dispatcher_and_there_load():
    if request.method == 'GET':
        admin_info = session.get('data')
        dispatcher_info = obj.get_load_info_from_db_for_admin()
        return render_template("/admin_temp/dispatcher_and_there_load.html" , dispatcher_info = dispatcher_info ,  admin_info = admin_info)






@app.route('/show_all_invoicess' , methods=["GET", "POST"])
@login_required('admin')
def show_all_invoicess():
    if request.method == 'GET':
        admin_info = session.get('data')
        invoic_info = obj.get_all_invoice_data_from_db()
        return render_template("/admin_temp/view_invoice_record.html" , invoic_info = invoic_info ,  admin_info = admin_info)





@app.route('/your-flask-route', methods=['POST'])
@login_required('admin')
def handle_post_request():
    # Retrieve data from the POST request
    invoice_data = request.json
    obj.stored_invoic_data_in_db(invoice_data)
    return redirect(url_for('admin_dashboard'))