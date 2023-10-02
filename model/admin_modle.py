import mysql.connector
from sqlalchemy import create_engine, text
import os



class Admin_Modle():
    engine = None

    def __init__(self):
        try:
            
            db_connection = os.environ.get('subline_db_connection')
            print(f"db_connection: {db_connection}")
            self.engine = create_engine(db_connection, connect_args={
                "ssl": {
                    "ssl_ca": "/etc/ssl/cert.pem"
                }
            })
            print("connection build successfully")
        except:
            print("not work")
            {'f_name': 'Abdul Baseer', 'cnic': '3710471513137', 'password': '5678', 'gender': 'male', 'email': 'abdulbasirqazi@gmail.com', 'phone_number': '3155849052', 'user_type': 'Sale Man', 'salary': '678'}
    def add_new_sale_man(self , data):
        with self.engine.connect() as conn:
            query1 = text(f"INSERT INTO sale_man_table VALUES ('{data['f_name']}' , '{data['cnic']}' , '{data['password']}' , '{data['gender']}' , '{data['email']}'  , '{data['phone_number']}'  , 'sale_man'  , '{data['salary']}' );")
            conn.execute(query1)
            return True
    
    def add_new_dispatcher(self , data):
        with self.engine.connect() as conn:
            query1 = text(f"INSERT INTO dispatcher_table VALUES ('{data['f_name']}' , '{data['cnic']}' , '{data['password']}' , '{data['gender']}' , '{data['email']}'  , '{data['phone_number']}'  , 'dispatcher'  , '{data['salary']}' );")
            conn.execute(query1)
            return True 
        

    def get_all_sales_for_db(self):
        with self.engine.connect() as conn:
            query = text(f"SELECT * from new_sales_first_time;")
            result = conn.execute(query).fetchall()
            return result
        
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
            print("this type = " , type(info['carears_id']))
            print("this data  =  = " , (info['carears_id']))
            querry_to_delete_unfransfer_sales_from_db = text(f"DELETE FROM untransfer_sales WHERE carear_id = {info['carears_id']};")
            conn.execute(querry_to_delete_unfransfer_sales_from_db)
            conn.execute(query1)
            return True 
        
    def get_load_info_from_db_for_admin(self):
        with self.engine.connect() as conn:
            query1 = text(f"SELECT load_number from disptcher_give_load_to_carear;")
            result = conn.execute(query1).fetchall()
            result = [item[0] for item in result]
            
            query2 = text(f"SELECT * from transfer_load_to_carears where load_number in {tuple(result)};")
            result = conn.execute(query2)
            column_names = result.keys()
            result_dict = [dict(zip(column_names, row)) for row in result]
            print("This is re = " , result_dict)
            return result_dict
        

    def get_carear_info_from_db_for_admin(self):
        with self.engine.connect() as conn:
            query1 = text(f"SELECT carear_id from disptcher_give_load_to_carear;")
            result = conn.execute(query1).fetchall()
            result = [item[0] for item in result]
            
            query2 = text(f"SELECT * from new_sales_first_time where carear_id in {tuple(result)};")
            result = conn.execute(query2)
            column_names = result.keys()
            # Assuming 'result' is a CursorResult object
            result_list = list(result)
            result_dict = [dict(zip(column_names, row)) for row in reversed(result_list)]


            print("This is re = " , result_dict)
            return result_dict
        
# obj = Admin_Modle()
# obj.get_all_dispater_name_and_pin()