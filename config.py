#fazendo configurações
import os.path
basedir = os.path.abspath(os.path.dirname(__file__))


DEBUG = True

#SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'storage.db')
SQLALCHEMY_DATABASE_URI = 'mysql://escapepp:escapepp@127.0.0.1/escapepp'


SQLALCHEMY_TRACK_MODIFICATIONS = True

SECRET_KEY = 'um-nome-bem-seguro'

