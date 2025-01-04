import pymysql
from pymysql import cursors
import pandas as pd


config = {
        'host': 'localhost',
        'user': 'root',
        'port':3306,
        'password': 'Xsq031124',
        'db': 'sensor',
        'charset': 'utf8mb4',
        'cursorclass': pymysql.cursors.DictCursor
    }
#数据库用的是本地的 db_name:sensor| 反馈表:infoBack 检测记录表: detectionRecord
def local_b_connect():
    connection = pymysql.connect(**config)

def fetch_mysql(table="detectionRecord"):
    connection = pymysql.connect(**config)
    try:
        with connection.cursor() as cursor:
            sql = f"SELECT * FROM {table} ORDER BY time DESC"
            cursor.execute(sql)
            result = cursor.fetchall()
            return result
    except Exception as e:
        print(f"遇到错误:{e}")
        return False



def insert_mysql(sensor,filename,username,BPM,IBI,Pulse,threshold,is_normal,table="detectionRecord"):
    data = (sensor,filename,username,BPM,IBI,Pulse,threshold,is_normal)
    connection = pymysql.connect(**config)
    try:
        with connection.cursor() as cursor:
            sql = f"INSERT INTO {table}(sensor,filename,username,BPM,IBI,Pulse,threshold,is_normal) VALUES (%s, %s, %s,%s, %s, %s,%s, %s)"
            cursor.execute(sql, data)
            connection.commit()
            return True
    except Exception as e:
        print(f"遇到错误: {e}")
        return False
    finally:
        connection.close()

def get_latest_record(table_name="detectionRecord"):
    print("ok")
    try:
        connection = pymysql.connect(**config)
        with connection.cursor() as cursor:
            sql = "SELECT filename,BPM,IBI,Pulse,is_normal FROM detectionRecord ORDER BY time DESC LIMIT 1"
            cursor.execute(sql)
            result = cursor.fetchone()
            if result:
                print(result)
                print(type(result))
                print([result['filename'],result['BPM'],result['IBI'],result['Pulse'],result['is_normal']])
                return result['filename'],result['BPM'],result['IBI'],result['Pulse'],result['is_normal']
    except pymysql.MySQLError as e:
        print(f"数据库错误: {e}")
        return False



def get_record_count():
    connection = pymysql.connect(**config)
    try:
        with connection.cursor() as cursor:
            sql = f"SELECT COUNT(*) FROM detectionRecord"
            cursor.execute(sql)
            result = cursor.fetchone()
            return result['COUNT(*)']
    except pymysql.MySQLError as e:
        print(f"数据库错误: {e}")
        return False


def calculate_column_IBI_mean(column_name='IBI'):
    connection = pymysql.connect(**config)
    try:
        with connection.cursor() as cursor:
            sql = f"SELECT AVG({column_name}) FROM detectionRecord"
            cursor.execute(sql)
            result = cursor.fetchone()
            return result['AVG(IBI)']
    except pymysql.MySQLError as e:
        print(f"数据库错误: {e}")
        return False
def calculate_column_Pulse_mean(column_name='Pulse'):
    connection = pymysql.connect(**config)
    try:
        with connection.cursor() as cursor:
            sql = f"SELECT AVG({column_name}) FROM detectionRecord"
            cursor.execute(sql)
            result = cursor.fetchone()
            return result['AVG(Pulse)']
    except pymysql.MySQLError as e:
        print(f"数据库错误: {e}")
        return False


def insert_mysql_feedback(email,message,table="feedback"):
    data = (email,message)
    connection = pymysql.connect(**config)
    try:
        with connection.cursor() as cursor:
            sql = f"INSERT INTO {table}(email,question) VALUES (%s, %s)"
            cursor.execute(sql, data)
            connection.commit()
            print("ok")
            return True
    except Exception as e:
        print(f"遇到错误: {e}")
        return False
    finally:
        connection.close()


def fetch_by_username(username, table="detectionRecord"):
    connection = pymysql.connect(**config)
    try:
        with connection.cursor() as cursor:
            sql = f"SELECT * FROM {table} WHERE username = %s ORDER BY time DESC"
            cursor.execute(sql, (username,))
            result = cursor.fetchall()
            return result
    except Exception as e:
        print(f"遇到错误: {e}")
        return False
 
def fetch_by_sensor(sensor, table="detectionRecord"):
    connection = pymysql.connect(**config)
    try:
        with connection.cursor() as cursor:
            sql = f"SELECT * FROM {table} WHERE sensor = %s ORDER BY time DESC"
            cursor.execute(sql, (sensor,))
            result = cursor.fetchall()
            return result
    except Exception as e:
        print(f"遇到错误: {e}")
        return False
 
def fetch_by_is_normal(is_normal, table="detectionRecord"):
    connection = pymysql.connect(**config)
    try:
        with connection.cursor() as cursor:
            db_is_normal = "正常" if is_normal else "疑似异常" 
            sql = f"SELECT * FROM {table} WHERE is_normal = %s ORDER BY time DESC"
            cursor.execute(sql, (db_is_normal,))
            result = cursor.fetchall()
            return result
    except Exception as e:
        print(f"遇到错误: {e}")
        return False

get_record_count()
calculate_column_Pulse_mean()
calculate_column_IBI_mean()