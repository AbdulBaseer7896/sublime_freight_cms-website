from app import app
from functools import wraps
from flask import session
from flask import redirect , url_for , render_template , request , flash
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
    print("This is check 3")
    if request.method == 'GET':
        sale_man_info = session.get('data')
        
        flash(("Dear Sale Man you succesfully Login !!!" , 'sale_login_pass'))
        return render_template('//sale_temp//sale_dashboard.html' ,sale_man_info = sale_man_info)



@app.route('/new_sale' , methods=["GET", "POST"])
@login_required('sale_man')
def new_sale():
    print("This is new_sale")
    if request.method == 'GET':
        sale_man_info = session.get('data')
        return render_template("//sale_temp//new_sale.html" , carear_info = "" , sale_man_info = sale_man_info)
    if request.method == 'POST':
        form_data = request.form.to_dict()
        sale_man_info = session.get('data')
        obj.new_sales_first_time(form_data , sale_man_info[0]['user_pin'])
        flash(("congratulations you Done new Sale!!!" , 'new_sale_success'))
        return render_template("//sale_temp//sale_dashboard.html" , sale_man_info= sale_man_info)
    
    
    

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
        print("this is type = " , type(carear_info))
        print("this is important = = " , carear_info)
        return render_template("//sale_temp//new_sale.html", carear_info=carear_info , sale_man_info = sale_man_info)
    
    
    



