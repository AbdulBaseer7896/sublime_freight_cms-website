
from flask import redirect , url_for , render_template , request , flash , app ,session
from flask_login import LoginManager, login_required, current_user , login_user ,logout_user
# from model.users_modles import users_modles
from app import app
from model.users_modles import UserModel
from flask import jsonify

obj = UserModel()


app.secret_key = "your_secret_key_here"
# create a LoginManager object
login_manager = LoginManager(app)


# define a User class with required methods for Flask-Login
class User:
    def __init__(self, user_id):
        self.id = user_id
    def get_type(self):
        return self.type
    def is_authenticated(self):
        return True
    def is_active(self):
        return True
    def is_anonymous(self):
        return False
    def get_id(self):
        return str(self.id)





@app.route('/home/login_page' , methods=["GET", "POST"])
def login_page():
    if request.method == "GET":
        return render_template("login_page.html")
    if request.method == "POST":
        

        password = request.form.get('user_pin')
        
        if obj.check_pin_for_login(password):
            pin = obj.get_user_pin_by_user_id(password)
            user_data_list = obj.user_data(pin)
            user_data = ''
            if user_data_list:
                user_data = [item._asdict() for item in user_data_list]
                # Now user_data is a list of dictionaries
            else:
                print("This is an error or empty")
            
            session['role'] = obj.user_role(pin)
            session['data'] = user_data
            
            if session['role'] == 'admin':
                return redirect(url_for('admin_dashboard'))
            elif session['role'] == 'sale_man':
                return redirect(url_for('sale_dashboard'))
            elif session['role'] == 'dispatcher':
                return redirect(url_for('dispatcher_dashboard'))
        
                # return render_template('index.html')
        flash(('Sorry you pin could not Match !!!' , 'login_fail'))
        # return render_template('login_page.html')
        return render_template('login_page.html')
    
    


# # create a dashboard route and view function for student
@login_manager.user_loader
def load_user(user_id):
    return User(int(user_id))


@app.route('/logout')
def logout():
    # Remove the user's role from the session variable
    session.pop('role', None)

    # Redirect to the login page
    return redirect(url_for('login_page'))



# @app.route('/changed_password' , methods=["GET", "POST"])
# def changed_password():
#     if request.method == "post":
#         changed_password_data = request.form.to_dict()
#         if obj.change_password_from_db(changed_password_data):
#             flash(("You successfully Changed the password !!!" , 'changed_password_success'))
#             return redirect(url_for('login_page'))
        
#     flash(("Sorry your pasword will not change. Kindly try Again !!!" , 'changed_password_fail'))
#     return render_template('changed_password.html')


@app.route('/changed_password', methods=["GET", "POST"])
def changed_password():
    if request. method == "GET":
        return render_template('changed_password.html')
    
    if request.method == "POST":
        changed_password_data = request.form.to_dict()
        if obj.change_password_from_db(changed_password_data):
            flash(("You successfully Changed the password !!!", 'changed_password_success'))
            return redirect(url_for('login_page'))
        else:
            flash(("Sorry your password will not change. Kindly Enter Strong PIn !!!", 'changed_password_fail'))
            return render_template('changed_password.html')


