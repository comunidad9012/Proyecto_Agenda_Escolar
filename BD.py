import mysql.connector


config = {
    "user": "root",
    "password": "Joaco322",
    "host": "localhost",
    "database": "agenda",
}


def conexion():
    connection = mysql.connector.connect(**config)
    return connection


def conexion_cursor(dictionary=False, named_tuple=False):
    connection = conexion()

    if dictionary:
        cursor = connection.cursor(dictionary=True)
    elif named_tuple:
        cursor = connection.cursor(named_tuple=True)

    return connection, cursor
