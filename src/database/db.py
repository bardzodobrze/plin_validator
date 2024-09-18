import pyodbc
from werkzeug.security import check_password_hash, generate_password_hash


def get_connection():
    server = r"DESKTOP-QB2OF27\SQLEXPRESS"
    database = "prueba_plin"
    conn_str = (
        f'DRIVER={{ODBC Driver 17 for SQL Server}};'
        f'SERVER={server};'
        f'DATABASE={database};'
        f'Trusted_Connection=yes;'
    )

    conn = pyodbc.connect(conn_str)
    return conn


"""
server = r"DESKTOP-QB2OF27\SQLEXPRESS"
database = "prueba_plin"
connection = get_connection(server, database)
with connection.cursor() as cursor:
    cursor.execute("SELECT id, title, duration_m, released FROM movies ORDER BY title ASC")
    resultset = cursor.fetchall()
    for x in resultset:
        print(x)
connection.close()
"""

"""
# INSERT USER
connection = get_connection()

pwd = "estaeslamasrica"
print(generate_password_hash(pwd))
pwd_hashed = "scrypt:32768:8:1$iftHyZzykLYx4ek5$ae8ccd4d0406e7bbb0d3188870a4867296c77a28f1798398eec2809da13e2ce5e0c6bf2d93e8c5293b878e43b8308214a03bdeb434387f02fd594119a0a73c02"
print(check_password_hash(pwd_hashed, pwd))
with connection.cursor() as cursor:
    cursor.execute("INSERT INTO user (username, password, fullname) VALUES (?, ?, ?)",
        ("dominos_plin", generate_password_hash(pwd), "Mr Dominos")
    )
    cursor.commit()
connection.close()
"""

