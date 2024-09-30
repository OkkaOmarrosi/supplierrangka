import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'your_secret_key_here'
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:1787602n@localhost:3306/integrasi'
    SQLALCHEMY_TRACK_MODIFICATIONS = False


import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'your_secret_key_here'
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://Suplierman:plierman/databases/@Suplierman.mysql.pythonanywhere-services.com/Suplierman$Supplierman2'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
