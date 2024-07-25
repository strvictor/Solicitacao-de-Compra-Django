import mysql.connector
from mysql.connector import Error

def create_connection(host_name, user_name, user_password, db_name, port):

    connection = mysql.connector.connect(
        host=host_name,
        user=user_name,
        passwd=user_password,
        database=db_name,
        port=port
    )

    return connection


# Informações da conexão
host_name = "192.168.0.108"
user_name = "cabana.ti"
user_password = "Cabana@Ti"
db_name = "cbo"
port = 4000

# Criação da conexão
connection = create_connection(host_name, user_name, user_password, db_name, port)

