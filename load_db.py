'''This file is used to load the data into database,
'query' lines should be commented if running.
'''
import mysql.connector
from parameter_store import para_store
from extract import extract_main

if __name__ == '__main__':

    PARA_HOST = 'Host_name'
    PARA_DB = 'DB_name'
    PARA_USER = 'User_name'
    PARA_PASSWORD = 'Password'


    connection = mysql.connector.connect(host=para_store(PARA_HOST),
                                            database=para_store(PARA_DB),
                                            user=para_store(PARA_USER),
                                            password=para_store(PARA_PASSWORD))

    if connection.is_connected():
        print('Connected to MySQL database')
        cursor = connection.cursor()
        for rows in extract_main():
            QUERY = '''
                INSERT INTO houses (address,house_type,price,avaliable_date,description)
                VALUES (%s,%s,%s,%s,%s)
                '''
            cursor.execute(QUERY,rows)
        connection.commit()


    if connection.is_connected():
        cursor.close()
        connection.close()
        print('MySQL connection is closed')
