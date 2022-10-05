# Modul ini untuk koneksi ke server database MySQL
from mysql.connector import Connect, Error

def mysql_conn():
  try:
    conn = Connect(
                host="localhost",
                user="root",
                password="",
                database="kosnaivebayes")
  except Error as e:
    print("Error koneksi ke MySQL", e)
  finally:
    return conn