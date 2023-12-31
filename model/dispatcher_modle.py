import mysql.connector
from sqlalchemy import create_engine, text
import os
from datetime import datetime
import pytz


class Dispatcher():
    engine = None
    

    def __init__(self):
        try:
            
            db_connection = os.environ.get('subline_db_connection')

            self.engine = create_engine(db_connection, connect_args={
                "ssl": {
                    "ssl_ca": "/etc/ssl/cert.pem"
                }
            })
            print("connection build successfully dispatcher")
        except:
            print("not work")
            


    def get_carear_info(self, pin):
        with self.engine.connect() as conn:
            query1 = text(f"SELECT carears_id from carear_id_and_dispatcher_pin_table where dispatcher_id = {pin};")
            result = conn.execute(query1).fetchall()
            int_result = [item[0] for item in result]
            if int_result != []:
                query2 = text(f"SELECT * from new_sales_first_time where carear_id IN ({', '.join(map(str, int_result))});")

                result = conn.execute(query2)
                result = conn.execute(query2)
                column_names = result.keys()
                result_dict = [dict(zip(column_names, row)) for row in result]
                return result_dict
            return ""
        

    def get_carear_info_from_db_by_carear_id(self , carear_id):
        with self.engine.connect() as conn:
            query = text(f"SELECT * from new_sales_first_time where carear_id = {carear_id};")
            result = conn.execute(query)
            column_names = result.keys()
            result_dict = [dict(zip(column_names, row)) for row in result]
            return result_dict
        
        
    def store_load_info_in_db(self , load_info , pin):
        with self.engine.connect() as conn:
            query  = text(f"select * from load_details where load_id = '{load_info['load_id']}'  and carear_id = '{load_info['carear_id']}'   and dispatcher_pin = '{pin}'; ")
            result1 = conn.execute(query).fetchall()
            if result1 != []:
                query = text(f" UPDATE load_details SET pick_up_location = '{load_info['pick_up_location']}', miles = '{load_info['miles']}', load_number = '{load_info['load_number']}', load_date = '{load_info['load_date']}', drop_location = '{load_info['drop_location']}', load_rate = '{load_info['load_rate']}', load_description = '{load_info['load_description']}' WHERE (load_id = '{load_info['load_id']}'  and carear_id  = '{load_info['carear_id']}'  and dispatcher_pin = '{pin}' );")
                conn.execute(query)
                return True
            
            query1 = text(f"SELECT COALESCE(MAX(CAST(load_id AS SIGNED)) , 0) FROM load_details;")
            result1 = conn.execute(query1).fetchall()

            load_id = 0
            if result1[0][0] == 0:
                load_id = 1
            else:
                load_id = int(result1[0][0]) + 1
                
            query = text(f"""INSERT INTO load_details VALUES ( "{load_id}" , "{load_info['carear_id']}" , "{load_info['pick_up_location']}" , "{load_info['miles']}" , "{load_info['load_number']}" , "{load_info['load_date']}"  , "{load_info['drop_location']}"   , "{load_info['load_rate']}" , "{load_info['load_description']}" , "{pin}" );""")
            conn.execute(query)
            return True


    def get_given_load_to_the_carear(self , pin , carear_id):
        with self.engine.connect() as conn:
            query1 = text(f"SELECT * from load_details where (dispatcher_pin = {pin} and carear_id = {carear_id});")

            result = conn.execute(query1)
            column_names = result.keys()
            result_dict = [dict(zip(column_names, row)) for row in result]
            return result_dict
        
    def get_local_time_ampm(self):
        lahore_timezone = pytz.timezone('Asia/Karachi')

        # Get the current time in Lahore
        lahore_time = datetime.now(lahore_timezone)

        # Format the local time in AM/PM format
        local_time_ampm = lahore_time.strftime('%Y-%m-%d %I:%M:%S %p')
        return local_time_ampm
        
        
    def store_load_and_carear_info_in_db(self , load_number , carear_id , dispatcher_pin):
        with self.engine.connect() as conn:
            query1 = text(f"""INSERT INTO disptcher_give_load_to_carear VALUES ( "{dispatcher_pin}" , "{load_number}" , "{carear_id}");""")
            conn.execute(query1)

            query2 = text(f"SELECT * from load_details where load_number = {load_number};")
            result = conn.execute(query2)
            column_names = result.keys()
            # Fetch all rows as dictionaries
            load_info = [dict(zip(column_names, row)) for row in result]
            load_info = load_info[0]
            
            local_time_ampm = self.get_local_time_ampm()
            
            query3= text(f"""INSERT INTO transfer_load_to_carears VALUES ( "{load_info['load_number']}" , "{local_time_ampm}" , "{load_info['load_date']}" , "{load_info['load_rate']}" , "{load_info['load_location']}" , "{load_info['distance']}" , "{load_info['weight']}"  , "{load_info['pick_up_time']}"   , "{load_info['delivery_time']}" , "{load_info['carrier_name']}" , "{load_info['agent_name']}" , "{load_info['agent_email_number']}" , "{load_info['carrier_email_number']}" , "{load_info['load_description']}" , "{dispatcher_pin}");""")
            conn.execute(query3)
            
            query4 =  text(f"DELETE FROM load_details WHERE load_number = {load_number};")
            conn.execute(query4)

            return True
        
        
        
    def get_just_load_from_db_from_form_view(self , load_id):
        with self.engine.connect() as conn:
            query1 = text(f"SELECT * from load_details where load_number = {load_id};")
            result = conn.execute(query1)
            column_names = result.keys()
            result_dict = [dict(zip(column_names, row)) for row in result]
            if result_dict != []:
                return result_dict[0]
            result_dict = ''
            return result_dict

        
    
    def get_carear_info_from_db(self , dispatcher_pin):
        with self.engine.connect() as conn:
            query1 = text(f"SELECT carear_id from disptcher_give_load_to_carear where dispatcher_pin = {dispatcher_pin};")
            result = conn.execute(query1).fetchall()
            result = [item[0] for item in result]
            if result != []:
                # query2 = text(f"SELECT * from new_sales_first_time where carear_id in {tuple(result) if len(result) > 1 else (result[0],)};")
                query2 = text(f"SELECT * from new_sales_first_time where carear_id IN ({', '.join(map(str, result))});")
                result = conn.execute(query2)
                column_names = result.keys()
                result_dict = [dict(zip(column_names, row)) for row in result]
                return result_dict
            result_dict = ""
            return result_dict
    

    def get_load_info_from_db_by_load_id(self , load_id):
        with self.engine.connect() as conn:
            query1 = text(f"SELECT * from load_details where load_id = {load_id};")
            result = conn.execute(query1)
            column_names = result.keys()
            result_dict = [dict(zip(column_names, row)) for row in result]
            if result_dict != []:
                return result_dict[0]
            result_dict = ''
            return result_dict