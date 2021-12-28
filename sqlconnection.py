import mysql.connector
from mysql.connector.constants import ClientFlag
from getpass import getpass

#You need to create your own .connectiondata file with your credentials
connection_data = open('.connectiondata', 'r')
password = connection_data.readline().replace('\n','')
host = connection_data.readline().replace('\n','')
database_name = connection_data.readline().replace('\n','')

config = {
    'user' : 'root',
    'password' : password,
    'host' : host,
    'client_flags' : [ClientFlag.SSL],
    'ssl_ca' : 'server-ca.pem',
    'ssl_cert' : 'client-cert.pem',
    'ssl_key' : 'client-key.pem',
    'database' : database_name
} 

cnxn = mysql.connector.connect(**config)

#Intelisense dont work here
cursor = cnxn.cursor()

db_table_name = "listona"

cursor.execute("SHOW TABLES LIKE '" + db_table_name + "'")
result = cursor.fetchone()

#Create first table. Should only be done one time
if not result:
    create_table = """
    CREATE TABLE """ + db_table_name + """(
        id INT AUTO_INCREMENT PRIMARY KEY,
        nome VARCHAR(100),
        nivel INT,
        xp INT,
        gold INT
    )

    """
    cursor.execute(create_table)
    cnxn.commit()
    
cursor.close()


