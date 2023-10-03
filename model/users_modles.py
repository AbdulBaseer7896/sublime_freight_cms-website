import mysql.connector
from sqlalchemy import create_engine, text
import os



class UserModel():
    engine = None
    
    # mysql+pymysql://nsescdh3nzt27p54y5sy:pscale_pw_mag9h24liZdIJpcLCFWmXYa9u7Wrx4AtKWAPuv41Ule@aws.connect.psdb.cloud/sublime_freight_data_base?charset=utf8mb4

    def __init__(self):
        try:
            
            db_connection = os.environ.get('subline_db_connection')
            # print("This is connection  = " , db_connection)
            # db_connection = "mysql+pymysql://nsescdh3nzt27p54y5sy:pscale_pw_mag9h24liZdIJpcLCFWmXYa9u7Wrx4AtKWAPuv41Ule@aws.connect.psdb.cloud/sublime_freight_data_base?charset=utf8mb4"
            print(f"db_connection: {db_connection}")
            self.engine = create_engine(db_connection, connect_args={
                "ssl": {
                    "ssl_ca": "/etc/ssl/cert.pem"
                }
            })
            print("connection build successfully user ")
        except:
            print("not work")
            
    def user_data(self , pin):
        with self.engine.connect() as conn:
            query = text(f"SELECT * from users where user_pin = {pin};")
            result = conn.execute(query).fetchall()
            print("user data is 4 == " , result)
            return result
        
    def all_user_pin(self):
        with self.engine.connect() as conn:
            query = text(f"SELECT user_pin from users;")
            result = conn.execute(query).fetchall()
            print("user data is  5 == " , result)
            return result
        
    def check_pin_for_login(self , pin):
        pin_data = self.all_user_pin()
        for i in pin_data:
            if int(i[0]) == pin:
                print("This pin match")
                return True
        return False
        
    def user_role(self , pin):
        with self.engine.connect() as conn:
            query = text(f"SELECT user_type from users where user_pin = {pin};")
            result = conn.execute(query).fetchall()
            result = result[0][0]
            return result



obj = UserModel()
obj.check_pin_for_login(1234)