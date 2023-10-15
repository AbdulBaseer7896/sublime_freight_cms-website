import mysql.connector
from sqlalchemy import create_engine, text
import os
import random


class Admin_Modle():
    engine = None

    def __init__(self):
        try:
            
            db_connection = os.environ.get('subline_db_connection')
            self.engine = create_engine(db_connection, connect_args={
                "ssl": {
                    "ssl_ca": "/etc/ssl/cert.pem"
                }
            })
            print("connection build successfully admin")
        except:
            print("not work")



    def add_new_sale_man(self , data):
        with self.engine.connect() as conn:
            user_id = self.get_user_id_from_db()
            six_digit_pin = self.gernate_password_for_users()
            query1 = text(f"INSERT INTO sale_man_table VALUES ('{data['f_name']}' , '{data['cnic']}' ,'{user_id}' , '{data['gender']}' , '{data['email']}'  , '{data['phone_number']}'  , 'sale_man'  , 0 , '{six_digit_pin}');")
            conn.execute(query1)
            
            query2 = text(f"INSERT INTO users VALUES ('{user_id}' , '{data['f_name']}' , '{data['phone_number']}' , '{data['email']}' , '{data['user_type']}' , 'active' , '{six_digit_pin}');")
            conn.execute(query2)
            return True
    
    def add_new_dispatcher(self , data):
        with self.engine.connect() as conn:
            user_id = self.get_user_id_from_db()
            six_digit_pin = self.gernate_password_for_users()
            query1 = text(f"INSERT INTO dispatcher_table VALUES ('{data['f_name']}' , '{data['cnic']}' , '{user_id}' , '{data['gender']}' , '{data['email']}'  , '{data['phone_number']}'  , 'dispatcher'  , 0 , '{six_digit_pin}' );")
            conn.execute(query1)
            
            query2 = text(f"INSERT INTO users VALUES ('{user_id}' , '{data['f_name']}' , '{data['phone_number']}' , '{data['email']}' , '{data['user_type']}' , 'active' , '{six_digit_pin}');")
            conn.execute(query2)
            return True 
        

        
    def gernate_password_for_users(self):
        with self.engine.connect() as conn:
            
            query1 = text(f"SELECT user_pin from users;")
            passwords = conn.execute(query1).fetchall()
            six_digit_pin = random.randint(100000, 999999)
            for i in passwords[0]:
                if i == six_digit_pin:
                    self.gernate_password_for_users()
            return six_digit_pin
        
    def get_user_id_from_db(self):
        with self.engine.connect() as conn:
            query1 = text(f"SELECT COALESCE(MAX(user_pin) , 0) FROM users;")
            result = conn.execute(query1).fetchall()
            result = int(result[0][0]) + 1
            print("This = = " , result)
            return result
        
            

        

    def get_all_sales_for_db(self):
        with self.engine.connect() as conn:
            query = text(f"SELECT * from new_sales_first_time;")
            result = conn.execute(query).fetchall()
            return result
        
    def get_carear_data_from_db(self , carears_id):
        with self.engine.connect() as conn:
            query = text(f"SELECT * from new_sales_first_time where carear_id = {carears_id};")
            result = conn.execute(query)
            column_names = result.keys()

            # Fetch all rows as dictionaries
            result_dict = [dict(zip(column_names, row)) for row in result]
            return result_dict[0]
        
    def get_first_form_sales_for_db(self):
        with self.engine.connect() as conn:
            query = text(f"SELECT * from sales_second_time;")
            result = conn.execute(query).fetchall()
            return result
        
        
        
    def get_untransfer_sales_data(self):
        with self.engine.connect() as conn:
            query = text(f"SELECT * from untransfer_sales;")
            result = conn.execute(query).fetchall()
            return result
        
    def get_all_dispater_name_and_pin(self):
        with self.engine.connect() as conn:
            query = text(f"SELECT * from dispatcher_table;")
            result = conn.execute(query)

            # Get the column names from the ResultProxy object
            column_names = result.keys()

            # Fetch all rows as dictionaries
            result_dict = [dict(zip(column_names, row)) for row in result]
            return result_dict
        
        
        
    def insert_carear_id_and_dispatcher_pin_in_db(self , info):
        with self.engine.connect() as conn:
            query1 = text(f"INSERT INTO carear_id_and_dispatcher_pin_table VALUES ('{info['dispatcher_id']}' , '{info['carears_id']}' );")
            
            querry_to_delete_unfransfer_sales_from_db = text(f"DELETE FROM untransfer_sales WHERE carear_id = {info['carears_id']};")

            conn.execute(querry_to_delete_unfransfer_sales_from_db)
            conn.execute(query1)
            return True 
        
    def get_load_info_from_db_for_admin(self):
        with self.engine.connect() as conn:
            query1 = text(f"SELECT load_number from disptcher_give_load_to_carear;")
            result = conn.execute(query1).fetchall()
            result = [item[0] for item in result]
            if result != []:
                query2 = text(f"SELECT * from transfer_load_to_carears where load_number in {tuple(result)};")
                result = conn.execute(query2)
                column_names = result.keys()
                result_dict = [dict(zip(column_names, row)) for row in result]
                return result_dict
            result_dict = ''
            return result_dict
        

    def get_carear_info_from_db_for_admin(self):
        with self.engine.connect() as conn:
            query1 = text(f"SELECT carear_id from disptcher_give_load_to_carear;")
            result = conn.execute(query1).fetchall()
            result = [item[0] for item in result]
            if result != []:
                query2 = text(f"SELECT * from new_sales_first_time where carear_id in {tuple(result)};")
                result = conn.execute(query2)
                column_names = result.keys()
                result_list = list(result)
                result_dict = [dict(zip(column_names, row)) for row in reversed(result_list)]
                return result_dict
            return ""
        
        
        
    def stored_card_info_in_db(self , card_info):
        with self.engine.connect() as conn:
            query = text(f"SELECT carear_name , email , phone_number   from new_sales_first_time where carear_id = '{card_info['carear_id']}';")
            result = conn.execute(query)
            column_names = result.keys()
            result_dict = [dict(zip(column_names, row)) for row in result]
            result_dict = result_dict[0]
            
            query1 = text(f"INSERT INTO atm_card_info VALUES ('{card_info['carear_id']}' , '{result_dict['carear_name']}', '{result_dict['email']}',  '{result_dict['phone_number']}',  '{card_info['care_number']}', '{card_info['card_expiry']}' , '{card_info['card_cvc']}' , '{card_info['card_type']}' , '{card_info['card_holder_name']}' );")
            conn.execute(query1)
            
        
    def get_card_data_from_db_to_display(self):
        with self.engine.connect() as conn:
            query1 = text(f"SELECT * from atm_card_info;")
            result = conn.execute(query1)
            
            column_names = result.keys()
            result_dict = [dict(zip(column_names, row)) for row in result]
            return result_dict
        
        
    def get_all_user_pin_from_db(self):
        with self.engine.connect() as conn:
            query1 = text(f"SELECT * from users where user_states = 'active';")
            result = conn.execute(query1)
            
            column_names = result.keys()
            result_dict = [dict(zip(column_names, row)) for row in result]
            return result_dict
        
    def get_all_disable_user_pin_from_db(self):
        with self.engine.connect() as conn:
            query1 = text(f"SELECT * from users where user_states = 'unactive';")
            result = conn.execute(query1)
            
            column_names = result.keys()
            result_dict = [dict(zip(column_names, row)) for row in result]
            return result_dict
        
        
        
    def get_first_form_sales_for_db_for_admin_search(self , search_text):
        with self.engine.connect() as conn:
            print("This search data  in fun = " , search_text)
            query = text(f"SELECT * from new_sales_first_time;")
            
            
            query = text(f"SELECT * FROM new_sales_first_time WHERE ('{search_text}' IN (carear_id, company_name, usdot, mc,  email , phone_number , carear_name , state ,sale_man_pin , dispatcher_pin));")
            
            result = conn.execute(query).fetchall()
            print("This is result = " , result)
            return result
        
        
        
    def disable_the_user_from_db(self , user_pin):
        with self.engine.connect() as conn:
            query = text(f"UPDATE users SET user_states = 'unactive' WHERE user_pin = {user_pin};")
            conn.execute(query)
            print("The user is disable")
            return True
            
            
            
    def enable_the_user_from_db(self , user_pin):
        with self.engine.connect() as conn:
            query = text(f"UPDATE users SET user_states = 'active' WHERE user_pin = {user_pin};")
            conn.execute(query)
            print("The user is disable")
            return True
            
            
# obj = Admin_Modle()
# obj.get_user_id_from_db()
