from extract import extract_main 
import mysql.connector
from mysql.connector import Error
from parameter_store import para_store 

para_host = 'HOST'
para_db = 'database_name'
para_user = 'USER'
para_password = 'PASSWORD'


connection = mysql.connector.connect(host=para_store(para_host), 
                                        database=para_store(para_db),
                                        user=para_store(para_user),
                                        password=para_store(para_password))

if connection.is_connected():
    print('Connected to MySQL database')
    cursor = connection.cursor()
    for rows in extract_main():
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
