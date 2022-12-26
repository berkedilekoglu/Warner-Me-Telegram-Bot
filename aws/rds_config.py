import pymysql
import os

USERNAME = os.environ.get('RDSUSERNAME')  # Replace with your master username
PASSWORD = os.environ.get('RDSPASSWORD')  # Replace with your RDS instance password
ENDPOINT = os.environ.get('RDSENDPOINT')  # Replace with your RDS endpoint
PORT = int(os.environ.get('RDSPORT'))   # Replace with instance port
REGION = os.environ.get('RDSREGION')  # Replace with your AWS region
DBNAME = os.environ.get('RDSDBNAME')  # Replace with the name of your SCHEMA in MySQL workbench
SSL_CA = os.path.abspath("/etc/secrets/rds-combined-ca-bundle.pem") # Replace with folder location of SSL bundle
CURSORCLASS = pymysql.cursors.DictCursor  # NO NEED to modify this