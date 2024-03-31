from extract import list_total # Call list_total from other file
import mysql.connector
from mysql.connector import Error

connection = mysql.connector.connect(host='practice-database.mysql.database.azure.com', 
                                        database='website',
                                        user='shared_user',
                                        password='Awanpassword!')

if connection.is_connected():
    print('Connected to MySQL database')
    cursor = connection.cursor()
    for rows in list_total:
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
