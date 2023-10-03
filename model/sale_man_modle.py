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
            print("connection build successfully sale man")
        except:
            print("not work")


    def new_sales_first_time(self , data , sale_man_pin):
        with self.engine.connect() as conn:
            
            print("this is data = " , data)
            carear_id = data['carear_id']
            result = ""
            if carear_id != "":
                query_check = text(f"SELECT carear_id FROM new_sales_first_time where carear_id = {carear_id};")
                result = conn.execute(query_check).fetchall()
                if result[0][0] == None:
                    carear_id = 0
                else:
                    query_check = text(f"SELECT * FROM new_sales_first_time where carear_id = {carear_id};")
                    result = conn.execute(query_check)
                    print("This is = = " , result)
                    column_names = result.keys()
                    change_data = [dict(zip(column_names, row)) for row in result]
                    change_data = change_data[0]
                    
                    if change_data['carear_id'] == carear_id:
                    
                        query_insert_update_data = text(f"INSERT INTO sales_second_time VALUES ( {change_data['carear_id']} , '{change_data['d_name']}' , '{change_data['driver']}' , '{change_data['mc_usdot']}' , '{change_data['company_name']}' , '{change_data['email']}'  , '{change_data['phone_number']}'   , '{change_data['charges']}' , '{change_data['t_number']}' , '{change_data['date']}' , '{change_data['ein']}' , '{change_data['physical_address']}' , '{change_data['factoring_address']}'  , '{change_data['factoring_num_email']}'  , '{change_data['bank_name']}' , '{change_data['account_number']}' , '{change_data['routing_number']}' , '{change_data['refrence']}' , '{change_data['comments']}' , '{change_data['factoring_name']}'  , '{change_data['insurance_details']}'  , '{change_data['equipments']}' , '{change_data['sale_man_pin']}' , '' );")

                        insert_in_untransfer_sales  =  text(f"INSERT INTO untransfer_sales VALUES ( {change_data['carear_id']} , '{data['d_name']}' , '{data['driver']}' , '{data['mc_usdot']}' , '{data['company_name']}' , '{data['email']}'  , '{data['phone_number']}'   , '{data['charges']}' , '{data['t_number']}' , '{data['date']}' , '{data['ein']}' , '{data['physical_address']}' , '{data['factoring_address']}'  , '{data['factoring_num_email']}'  , '{data['bank_name']}' , '{data['account_number']}' , '{data['routing_number']}' , '{data['refrence']}' , '{data['comments']}' , '{data['factoring_name']}'  , '{data['insurance_details']}'  , '{data['equipments']}' , '{sale_man_pin}' , '' );")
                        update_in_to_sales_man_first_time_table = text(f"INSERT INTO new_sales_first_time VALUES ( {change_data['carear_id']} , '{data['d_name']}' , '{data['driver']}' , '{data['mc_usdot']}' , '{data['company_name']}' , '{data['email']}'  , '{data['phone_number']}'   , '{data['charges']}' , '{data['t_number']}' , '{data['date']}' , '{data['ein']}' , '{data['physical_address']}' , '{data['factoring_address']}'  , '{data['factoring_num_email']}'  , '{data['bank_name']}' , '{data['account_number']}' , '{data['routing_number']}' , '{data['refrence']}' , '{data['comments']}' , '{data['factoring_name']}'  , '{data['insurance_details']}'  , '{data['equipments']}' , '{sale_man_pin}' , '' );")
                

                        
                        
                        # Remove the extra closing parenthesis
                        query_for_delete_sale_from_first_time = text(f"DELETE FROM new_sales_first_time WHERE carear_id = {change_data['carear_id']};")
                        print("This is important = " ,change_data['carear_id'] )
                        check = int(change_data['carear_id']) 
                        query_for_delete_sale_untransfer_sales = text(f"DELETE FROM untransfer_sales WHERE carear_id = {check};")
                        
                        conn.execute(query_for_delete_sale_untransfer_sales)
                        conn.execute(query_for_delete_sale_from_first_time)
                        print("The row is deleated")
                        conn.execute(query_insert_update_data)
                        conn.execute(update_in_to_sales_man_first_time_table)
                        conn.execute(insert_in_untransfer_sales)
                        print("This row in inserted update")
            else:
                query = text(f"SELECT MAX(carear_id) FROM new_sales_first_time;")
                result = conn.execute(query).fetchall()
                if result[0][0] == None:
                    carear_id = 1
                else:
                    carear_id = int(result[0][0]) + 1
                query1 = text(f"INSERT INTO new_sales_first_time VALUES ( {carear_id} , '{data['d_name']}' , '{data['driver']}' , '{data['mc_usdot']}' , '{data['company_name']}' , '{data['email']}'  , '{data['phone_number']}'   , '{data['charges']}' , '{data['t_number']}' , '{data['date']}' , '{data['ein']}' , '{data['physical_address']}' , '{data['factoring_address']}'  , '{data['factoring_num_email']}'  , '{data['bank_name']}' , '{data['account_number']}' , '{data['routing_number']}' , '{data['refrence']}' , '{data['comments']}' , '{data['factoring_name']}'  , '{data['insurance_details']}'  , '{data['equipments']}' , '{sale_man_pin}' , '' );")
                query2 = text(f"INSERT INTO untransfer_sales VALUES ( {carear_id} , '{data['d_name']}' , '{data['driver']}' , '{data['mc_usdot']}' , '{data['company_name']}' , '{data['email']}'  , '{data['phone_number']}'   , '{data['charges']}' , '{data['t_number']}' , '{data['date']}' , '{data['ein']}' , '{data['physical_address']}' , '{data['factoring_address']}'  , '{data['factoring_num_email']}'  , '{data['bank_name']}' , '{data['account_number']}' , '{data['routing_number']}' , '{data['refrence']}' , '{data['comments']}' , '{data['factoring_name']}'  , '{data['insurance_details']}'  , '{data['equipments']}' , '{sale_man_pin}' , '' );")

                conn.execute(query1)
                conn.execute(query2)
                return True
    
        
    def get_sale_man_sales(self, pin):
        with self.engine.connect() as conn:
            query = text(f"SELECT * from new_sales_first_time where sale_man_pin = {pin} ;")
            result = conn.execute(query)

            # Get the column names from the ResultProxy object
            column_names = result.keys()

            # Fetch all rows as dictionaries
            result_dict = [dict(zip(column_names, row)) for row in result]
            print("user data is 5 == ", result_dict)

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








# obj = Sale_Man_Modle()
# obj.new_sales_first_time(1 , 3)