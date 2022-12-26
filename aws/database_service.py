import pymysql.cursors
import datetime
import pytz


from .rds_config import *  # Import parameters for PyMySQL connection e.g. ENDPOINT, PORT etc.
from pytz import timezone


def current_time_Istanbul():
    utc_now = datetime.datetime.utcnow()
    utc = pytz.timezone('UTC')
    aware_date = utc.localize(utc_now)
    turkey = timezone('Europe/Istanbul')
    return aware_date.astimezone(turkey)

# Define function to establish RDS connection
def start_rds_connection():
    try:
        connection = pymysql.connect(host=ENDPOINT,
                                     port=PORT,
                                     user=USERNAME,
                                     passwd=PASSWORD,
                                     db=DBNAME,
                                     cursorclass=CURSORCLASS,
                                     ssl_ca=SSL_CA)
        print('[+] RDS Connection Successful',flush=True)
    except Exception as e:
        print(f'[+] RDS Connection Failed: {e}',flush=True)
        connection = None

    return connection

def check_record(connection,tableName,clientId):
    try:
        with connection.cursor() as cursor:
            checkUsername = cursor.execute(f'SELECT nClientId FROM {tableName} WHERE nClientId = {clientId}')
        print(f'Successfully checked userId {clientId}',flush=True)
        return checkUsername
    except Exception as e:
        print(f'Error in checking from MySQL database: {e}',flush=True)
        
def get_status_record(connection,tableName,clientId):
    try:
        with connection.cursor() as cursor:
            cursor.execute(f'SELECT codeStatus, results FROM {tableName} WHERE nClientId = {clientId}')
            result_dict = cursor.fetchone()
            codeStatus = result_dict['codeStatus']
            result = result_dict['results']
        print(f'Successfully checked codeStatus and result of userId {clientId}')
        return {'status':codeStatus,'result':result}
    except Exception as e:
        print(f'Error in checking status from MySQL database: {e}')

def insert_record(connection,tableName, nClientID, codeStatus, chatId, results):
    try:
        with connection.cursor() as cursor:
            sql = f"INSERT INTO `{tableName}` (`nClientID`, `codeStatus`, `dtLastVisit`, `chatId`, `results`) VALUES (%s, %s, %s, %s, %s)"
            cursor.execute(sql, (nClientID, codeStatus,current_time_Istanbul(), chatId, results))

        # Connection is not autocommit by default, so we must commit to save changes
        connection.commit()
        print(f'Successfully inserted record into {tableName}',flush=True)
    except Exception as e:
        print(f'Error in insertion to MySQL database: {e}',flush=True)

"""
def update_record(connection,tableName,clientId,status):

    try:
        with connection.cursor() as cursor:
            sql_update_query = f"Update {tableName} set codeStatus = {status} where nClientId = {clientId}"
            cursor.execute(sql_update_query)
            connection.commit()
        print(f'Successfully updated status of clientId {clientId}')
    except Exception as e:
        print(f'Error in checking from MySQL database: {e}')
"""