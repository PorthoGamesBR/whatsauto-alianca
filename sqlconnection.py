import mysql.connector
from mysql.connector.constants import ClientFlag
from getpass import getpass

#You need to create your own .connectiondata file with your credentials
connection_data = open('.connectiondata', 'r')
password = connection_data.readline().replace('\n','')
host = connection_data.readline().replace('\n','')

config = {
    'user' : 'root',
    'password' : password,
    'host' : host,
    'client_flags' : [ClientFlag.SSL],
    'ssl_ca' : 'server-ca.pem',
    'ssl_cert' : 'client-cert.pem',
    'ssl_key' : 'client-key.pem'
    
} 

cnxn = mysql.connector.connect(**config)

