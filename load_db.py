from extract import extract_main 
import mysql.connector
from mysql.connector import Error
from parameter_store import para_store 

if __name__ == '__main__':

    para_host = 'Host_name'
    para_db = 'DB_name'
    para_user = 'User_name'
    para_password = 'Password'


    connection = mysql.connector.connect(host=para_store(para_host), 
                                            database=para_store(para_db),
                                            user=para_store(para_user),
                                            password=para_store(para_password))

    if connection.is_connected():
        print('Connected to MySQL database')
        cursor = connection.cursor()
        for rows in extract_main():    ## Make this 'for' loop as comment if trying to test this script.
            query = '''
                INSERT INTO houses (address,house_type,price,avaliable_date,description)
                VALUES (%s,%s,%s,%s,%s)
                '''
            cursor.execute(query,rows)
        connection.commit() 


    if connection.is_connected():
        cursor.close()
        connection.close()
        print('MySQL connection is closed')
