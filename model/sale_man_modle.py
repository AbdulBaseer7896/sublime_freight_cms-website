import mysql.connector
from sqlalchemy import create_engine, text
import os



class Sale_Man_Modle():
    engine = None

    def __init__(self):
        try:
            
            db_connection = os.environ.get('subline_db_connection')
            self.engine = create_engine(db_connection, connect_args={
                "ssl": {
                    "ssl_ca": "/etc/ssl/cert.pem"
                }
            })
            print("connection build successfully sale man ")
        except:
            print("not work")


    def new_sales_first_time(self , data , sale_man_pin):
        with self.engine.connect() as conn:
            carear_id = data['carear_id']
            print("This is carear id = " , carear_id)
            result = ""
            if carear_id != "":
                print("This is 2")
                query_check = text(f"SELECT carear_id FROM new_sales_first_time where carear_id = {carear_id};")
                result = conn.execute(query_check).fetchall()
                print("This is resutl  = " , result)
                
                # if result == []:
                if result[0][0] == None:
                    print("This is 3")
                    carear_id = 0
                else:
                    query_check = text(f"SELECT * FROM new_sales_first_time where carear_id = {carear_id};")
                    result = conn.execute(query_check)
                    column_names = result.keys()
                    change_data = [dict(zip(column_names, row)) for row in result]
                    change_data = change_data[0]
                    print("This is the change data = " , change_data)
                    print("This is 4")
                    
                    if change_data['carear_id'] == carear_id:
                        print("This is 5")
                    
                        query_insert_update_data = text(f"INSERT INTO sales_second_time VALUES ( {change_data['carear_id']} , '{change_data['company_name']}' ,'{change_data['usdot']}' , '{change_data['email']}' , '{change_data['truck_type_and_number']}' , '{change_data['carear_name']}' , '{change_data['mc']}'  , '{change_data['phone_number']}'   , '{change_data['ein']}' , '{change_data['inc_name']}' , '{change_data['inc_address']}' , '{change_data['inc_fax_number']}' , '{change_data['inc_number']}' , '{change_data['inc_email']}'  , '{change_data['inc_coverges']}'  , '{change_data['fac_name']}' , '{change_data['fac_email']}' , '{change_data['fac_phone_number']}' , '{change_data['fac_address']}' , '{change_data['bank_name']}' , '{change_data['account_number']}'  , '{change_data['sale_type']}'  , '{change_data['routing_number']}' , '{change_data['bank_phone_number']}' , '{change_data['date']}' , '{change_data['state']}' ,  '{change_data['sale_man_pin']}' ,  '' );")
                        insert_in_untransfer_sales  =    text(f"INSERT INTO untransfer_sales VALUES ( {change_data['carear_id']} , '{data['company_name']}' ,'{data['usdot']}' , '{data['email']}' , '{data['truck_type_and_number']}' , '{data['carear_name']}' , '{data['mc']}'  , '{data['phone_number']}'   , '{data['ein']}' , '{data['inc_name']}' , '{data['inc_address']}' , '{data['inc_fax_number']}' , '{data['inc_number']}' , '{data['inc_email']}'  , '{data['inc_coverges']}'  , '{data['fac_name']}' , '{data['fac_email']}' , '{data['fac_phone_number']}' , '{data['fac_address']}' , '{data['bank_name']}' , '{data['account_number']}'  , '{data['sale_type']}'  , '{data['routing_number']}' , '{data['bank_phone_number']}' , '{data['date']}' , '{data['state']}'  ,  {sale_man_pin}, '' );")
                        update_in_to_sales_man_first_time_table = text(f"INSERT INTO new_sales_first_time VALUES ( {change_data['carear_id']} , '{data['company_name']}' ,'{data['usdot']}' , '{data['email']}' , '{data['truck_type_and_number']}' , '{data['carear_name']}' , '{data['mc']}'  , '{data['phone_number']}'   , '{data['ein']}' , '{data['inc_name']}' , '{data['inc_address']}' , '{data['inc_fax_number']}' , '{data['inc_number']}' , '{data['inc_email']}'  , '{data['inc_coverges']}'  , '{data['fac_name']}' , '{data['fac_email']}' , '{data['fac_phone_number']}' , '{data['fac_address']}' , '{data['bank_name']}' , '{data['account_number']}'  , '{data['sale_type']}'  , '{data['routing_number']}' , '{data['bank_phone_number']}'  ,  '{data['date']}' , '{data['state']}' , {sale_man_pin} ,  '' );")

                        query_for_delete_sale_from_first_time = text(f"DELETE FROM new_sales_first_time WHERE carear_id = {change_data['carear_id']};")
                        check = int(change_data['carear_id']) 
                        query_for_delete_sale_untransfer_sales = text(f"DELETE FROM untransfer_sales WHERE carear_id = {check};")
                        
                        conn.execute(query_for_delete_sale_untransfer_sales)
                        conn.execute(query_for_delete_sale_from_first_time)
                        conn.execute(query_insert_update_data)
                        conn.execute(update_in_to_sales_man_first_time_table)
                        conn.execute(insert_in_untransfer_sales)
                        print("This is 6")
            else:
                query = text(f"SELECT MAX(carear_id) FROM new_sales_first_time;")
                result = conn.execute(query).fetchall()
                if result[0][0] == None:
                    print("This is 8")
                    carear_id = 1
                else:
                    print("This is 7")
                    carear_id = int(result[0][0]) + 1
                    
                query1 =  text(f"INSERT INTO new_sales_first_time VALUES ( {carear_id} , '{data['company_name']}' ,'{data['usdot']}' , '{data['email']}' , '{data['truck_type_and_number']}' , '{data['carear_name']}' , '{data['mc']}'  , '{data['phone_number']}'   , '{data['ein']}' , '{data['inc_name']}' , '{data['inc_address']}' , '{data['inc_fax_number']}' , '{data['inc_number']}' , '{data['inc_email']}'  , '{data['inc_coverges']}'  , '{data['fac_name']}' , '{data['fac_email']}' , '{data['fac_phone_number']}' , '{data['fac_address']}' , '{data['bank_name']}' , '{data['account_number']}'  , '{data['sale_type']}'  , '{data['routing_number']}' , '{data['bank_phone_number']}'  , '{data['date']}' , '{data['state']}' ,  {sale_man_pin}, '' );")
                query2 =  text(f"INSERT INTO untransfer_sales VALUES ( {carear_id} , '{data['company_name']}' ,'{data['usdot']}' , '{data['email']}' , '{data['truck_type_and_number']}' , '{data['carear_name']}' , '{data['mc']}'  , '{data['phone_number']}'   , '{data['ein']}' , '{data['inc_name']}' , '{data['inc_address']}' , '{data['inc_fax_number']}' , '{data['inc_number']}' , '{data['inc_email']}'  , '{data['inc_coverges']}'  , '{data['fac_name']}' , '{data['fac_email']}' , '{data['fac_phone_number']}' , '{data['fac_address']}' , '{data['bank_name']}' , '{data['account_number']}'  , '{data['sale_type']}'  , '{data['routing_number']}' , '{data['bank_phone_number']}' , '{data['date']}' , '{data['state']}' ,   {sale_man_pin}, '' );")
                print("This is 6")
                conn.execute(query1)
                conn.execute(query2)
                print("this is one")
                return True
    
        
    def get_sale_man_sales(self, pin):
        with self.engine.connect() as conn:
            query = text(f"SELECT * from new_sales_first_time where sale_man_pin = {pin} ;")
            result = conn.execute(query)

            # Get the column names from the ResultProxy object
            column_names = result.keys()

            # Fetch all rows as dictionaries
            result_dict = [dict(zip(column_names, row)) for row in result]
            return result_dict


    def carear_info_for_carear_id(self , carear_id):
        with self.engine.connect() as conn:
            query = text(f"SELECT * from new_sales_first_time where carear_id = {carear_id} ;")
            result = conn.execute(query)

            # Get the column names from the ResultProxy object
            column_names = result.keys()

            # Fetch all rows as dictionaries
            result_dict = [dict(zip(column_names, row)) for row in result]
            return result_dict[0]




    def add_new_appointment_in_db(self , data , sale_man_pin):
        with self.engine.connect() as conn:
            query = text(f"SELECT MAX(appointment_id) FROM new_appointment;")
            result = conn.execute(query).fetchall()
            if result[0][0] == None:
                print("This is 8")
                carear_id = 1
            else:
                print("This is 7")
                carear_id = int(result[0][0]) + 1
            query1 =  text(f"INSERT INTO new_appointment VALUES ( {carear_id} , '{data['company_name']}' ,'{data['usdot']}' , '{data['email']}' , '{data['truck_or_traler']}' , '{data['comments']}' , '{data['carear_name']}'  , '{data['mc']}'   , '{data['phone_number']}' , '{data['conversations']}' , '{data['appointment_type']}', {sale_man_pin} ,  '{data['state']}' , '{data['date']}' );")
            conn.execute(query1)
            print("new appointment display")
            return True


    def get_sales_man_appointment_from_db(self , appointment_info):
        with self.engine.connect() as conn:
            query = text(f"SELECT * from new_appointment where sales_man_pin = {appointment_info} ;")
            result = conn.execute(query)
            column_names = result.keys()

            # Fetch all rows as dictionaries
            result_dict = [dict(zip(column_names, row)) for row in result]
            return result_dict
        
        
    def appointment_info_for_appointment_id(self ,appointment_id ):
        with self.engine.connect() as conn:
            query = text(f"SELECT * from new_appointment where appointment_id = {appointment_id} ;")
            result = conn.execute(query)

            # Get the column names from the ResultProxy object
            column_names = result.keys()

            # Fetch all rows as dictionaries
            result_dict = [dict(zip(column_names, row)) for row in result]
            return result_dict[0]



    def get_sale_man_sales_for_search_text(self, pin , search_text):
        with self.engine.connect() as conn:
            print("This is text = " , search_text)
            query = text(f"SELECT * from new_sales_first_time where sale_man_pin = {pin} ;")
            
            query = text(f"SELECT * FROM new_sales_first_time WHERE ('{search_text}' IN (carear_id, company_name, usdot, mc,  email , phone_number , carear_name , state) and sale_man_pin = {pin});")
            result = conn.execute(query)

            # Get the column names from the ResultProxy object
            column_names = result.keys()

            # Fetch all rows as dictionaries
            result_dict = [dict(zip(column_names, row)) for row in result]
            print("This is result = " , result_dict)
            return result_dict
        
        
    def get_sales_man_appointment_from_db_for_search(self , pin  , search_text ):
        with self.engine.connect() as conn:
            query = text(f"SELECT * FROM new_appointment WHERE ('{search_text}' IN (appointment_id , company_name, usdot, mc,  email , phone_number , carear_name , state , truck_or_traler) and sales_man_pin = '{pin}');")

            result = conn.execute(query)
            column_names = result.keys()

            # Fetch all rows as dictionaries
            result_dict = [dict(zip(column_names, row)) for row in result]
            return result_dict
        
