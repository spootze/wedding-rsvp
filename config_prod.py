import os

DB_CONNECTION_STRING='postgresql://' + os.getenv('RDS_USERNAME') + ':' + \
                      os.getenv('RDS_PASSWORD') + '@' + \
                      os.getenv('RDS_HOSTNAME') + ':' + \
                      os.getenv('RDS_PORT') + '/' + \
                      os.getenv('RDS_DB_NAME')
