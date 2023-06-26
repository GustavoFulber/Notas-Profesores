import os


class Config(object):
    # MYSQL_HOST = os.getenv('MYSQL_HOST')
    # MYSQL_USER = os.getenv('MYSQL_USER')
    # MYSQL_PASSWORD = os.getenv('MYSQL_PASSWORD')
    # MYSQL_DB = os.getenv('MYSQL_DB')
    # SECRET_KEY = os.getenv('SECRET_KEY')
    # JWT_ACCESS_TOKEN_EXPIRES =
    # timedelta(hours=int(os.getenv('JWT_ACCESS_TOKEN_EXPIRES')))
    # JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY')
    PORT = int(os.getenv('PORT', 5000))
    HOST = os.getenv('HOST', 'localhost')
