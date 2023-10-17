import mysql.connector
from sqlalchemy import create_engine, text
import pymysql
import os



class UserModel():
    engine = None
    
    def __init__(self):
        try:
            
            db_connection = os.environ.get('subline_db_connection')
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
                return result
        
    def get_user_pin_by_user_id(self , password):
        with self.engine.connect() as conn:
            query = text(f"SELECT user_pin from users where user_id = {password};")
            result = conn.execute(query).fetchall()
            if result != []:
                return result[0][0]
            else:
                return ''
        
    def all_user_pin(self):
        with self.engine.connect() as conn:
            query = text(f"SELECT user_id from users where user_states = 'active';")
            result = conn.execute(query).fetchall()
            return result
        
    def check_pin_for_login(self , pin):
        pin_data = self.all_user_pin()
        for i in pin_data:
            if i[0] == pin:
                return True
        return False
        
    def user_role(self , pin):
        with self.engine.connect() as conn:
            query = text(f"SELECT user_type from users where user_pin = {pin};")
            result = conn.execute(query).fetchall()
            
            if result != []:
                return result[0][0]
            else:
                return ''
        
    def change_password_from_db(self , change_password_data):
        with self.engine.connect() as conn:
            if not self.check_pin_for_login(change_password_data['new_password']):
                query1 = text(f"UPDATE users SET user_id = '{change_password_data['new_password']}' WHERE user_id = {change_password_data['old_password']};")
                query2 = text(f"UPDATE sale_man_table SET user_id = '{change_password_data['new_password']}' WHERE user_id = {change_password_data['old_password']};")
                query3 = text(f"UPDATE dispatcher_table SET user_id = '{change_password_data['new_password']}' WHERE user_id = {change_password_data['old_password']};")
                
                conn.execute(query1)
                conn.execute(query2)
                conn.execute(query3)
                return True
            else:
                return False
            
            
            
# obj =UserModel()    
# obj.change_password_from_db(123);