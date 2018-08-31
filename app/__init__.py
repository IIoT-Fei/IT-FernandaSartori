# __init__ é para quando está trabalhando com módulo (conjunto de declaraçãoes de funções, classes...)
from flask import Flask #importando flask
from flask_sqlalchemy import SQLAlchemy #importando o SQLAlchemy, sempre segue o padrão flask_
from flask_script import Manager
from flask_migrate import Migrate
from flask_migrate import MigrateCommand
from flask_login import LoginManager #essa classe é um gerenciador



#from flask_login import LoginManager #essa classe é um gerenciador



app = Flask(__name__)
app.config.from_object('config') #"habilitando" as configurações

#app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///storage.db' #estou passando uma configuração chamada SQLALCHEMY_DATABASE_URI, que é a URI de conexão com o banco de dados e é uma string do sqlite

#migrações são para quando vc faz alguma alteração no bando de dados

db = SQLAlchemy(app)#instancia do SQLAlchemy
migrate = Migrate(app, db)#instancia do Migrate
#quero instanciar o Migrate e ele cuiudará das minhas Migrações
#cuida dos comandos
#o MigrateCommand já tem uns comandos preparados como rodar o programa

manager = Manager(app)
manager.add_command('db', MigrateCommand)

lm = LoginManager()#estou criando uma instancia de Login em app
lm.init_app(app)

from app.models import tables, forms
from app.controllers import default