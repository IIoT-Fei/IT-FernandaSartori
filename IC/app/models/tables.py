from sqlalchemy import ForeignKey
from sqlalchemy.ext.hybrid import hybrid_property

from app import db


# classe User que herda da db.Model, que é uma classe da SQLAlchemy que tem um padrão de tabela

class User(db.Model):
    __tablename__ = "users"
    # campos da minha coluna do banco de dados

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True)
    professor = db.Column(db.Boolean)

    @property  # propriedades para saber se o usuario está logado
    def is_authenticated(self):
        return True

    @property  # propriedades para saber se o usuario está logado
    def is_active(self):
        return True

    @property  # propriedades para saber se o usuario está logado
    def is_anonymous(self):
        return False  # retorna falso se o usuario esta logado

    def get_id(self):  # função que retorna um unicode que identifica um usuário
        return str(self.id)  # no python3 a strig é unicode, no python2 é unicode(self.id)

    # construtor que inicializa os users
    def __init__(self, username, password, name, email, professor):
        self.username = username
        self.password = password
        self.name = name
        self.email = email
        self.professor = professor

    # função que faz uma representação de como vai aparecer depois que consultar o banco de dados
    def __repr__(self):
        return "<User %r>" % self.username  # %r=nomedousuario

#
# # também é instâcia de Model
class Lab(db.Model):
    __tablename__ = "labs"

    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(50), unique=True, nullable=False)
    arquivo = db.Column(db.String(10000))
    disciplina_id = db.Column(db.Integer, db.ForeignKey("disciplina.id"))
    disciplina = db.relationship("Disciplina")
    # disciplina = db.relationship('Disciplina', db.ForeignKey('disciplina.nome_disc'))
    # user = db.relationship('User', foreign_keys=user_id)  # eu vejo além do usuario, vejo o usuarios que é dono do post
    datahora = db.Column(db.TIMESTAMP(timezone=True))  # timezone= ativa fuso horario
    excluir = db.Column(db.Boolean)
    visivel = db.Column(db.Boolean)
    #     # construtor
    def __init__(self, titulo, arquivo, datahora, disciplina_id, excluir, visivel):
        self.titulo = titulo
        self.arquivo = arquivo
        self.datahora = datahora
        self.disciplina_id = disciplina_id
        self.excluir = excluir
        self.visivel = visivel

    #
    #     # representação
    def __repr__(self):
        return "<Laboratório %r>" % self.titulo


class Disciplina(db.Model):
    __tablename__ = "disciplina"

    id = db.Column(db.Integer, primary_key=True)
    codigo_disc = db.Column(db.String(50), unique=True, nullable=False)
    logo = db.Column(db.String(150))
    nome_disc = db.Column(db.String(100), nullable=False)
    chave = db.Column(db.String(50))
    visivel = db.Column(db.Boolean)
    id_prof = db.Column(db.Integer)
    excluir = db.Column(db.Boolean)
    # user = db.relationship('User', foreign_keys=user_id)  # eu vejo além do usuario, vejo o usuarios que é dono do post

    #     # construtor
    def __init__(self, codigo_disc, logo, nome_disc, chave, id_prof, excluir, visivel):
        self.codigo_disc = codigo_disc
        self.logo = logo
        self.nome_disc = nome_disc
        self.chave = chave
        self.id_prof = id_prof
        self.excluir = excluir
        self.visivel = visivel


    #
    #     # representação
    def __repr__(self):
        return "<Disciplina %r>" % self.codigo_disc


class Envios(db.Model):
    __tablename__ = "envios"

    id = db.Column(db.Integer, primary_key=True)
    status = db.Column(db.String(100), nullable=False)
    mensagem = db.Column(db.String(10000), nullable=False)
    cod_user = db.Column(db.Integer, db.ForeignKey("users.id"))
    cod_lab = db.Column(db.Integer, db.ForeignKey('labs.id'))
    usuario  = db.relationship("User")
    laboratorio = db.relationship("Lab")
    datahora = db.Column(db.TIMESTAMP(timezone=True)) #timezone= ativa fuso horario

    def __init__(self, status, mensagem, cod_user, cod_lab, datahora):
        self.status = status
        self.mensagem = mensagem
        self.cod_user = cod_user
        self.cod_lab = cod_lab
        self.datahora = datahora

    # representação

    def __repr__(self):
        return "<Envios %r>" % self.mensagem

    @hybrid_property
    def situacao(self):
        d = Envios.query.filter(Envios.usuario==self.usuario).filter(Envios.laboratorio==self.laboratorio).all()
        #if self.status == "Aprovado":
        #    return "Aprovado"
        #elif self.status == "Reprovado":
        ##    return "Reprovado"
        #else
        #    return "Nâo Enviado"
        return len(d)

class Convite(db.Model):
    __tablename__ = "convites"

    id = db.Column(db.Integer, primary_key=True)
    nome_convidado = db.Column(db.String(100), nullable=False)
    email_convidado = db.Column(db.String(100), nullable=False)
    mensagem_para_convidado = db.Column(db.String(10000), nullable=False)
    cod_remetente = db.Column(db.Integer, db.ForeignKey("users.id"))
    remetente = db.relationship("User")

    def __init__(self, nome_convidado, email_convidado, mensagem_para_convidado, cod_remetente):
        self.nome_convidado = nome_convidado
        self.email_convidado = email_convidado
        self.mensagem_para_convidado = mensagem_para_convidado
        self.cod_remetente = cod_remetente

    # representação

    def __repr__(self):
        return "<Convite %r>" % self.mensagem_para_convidado


class User_Disciplina(db.Model):
    __tablename__ = "user_disc"

    id = db.Column(db.Integer, primary_key=True)
    cod_user = db.Column(db.Integer, db.ForeignKey("users.id"))
    cod_dis = db.Column(db.Integer, db.ForeignKey("disciplina.id"))
    user = db.relationship('User')
    disc = db.relationship('Disciplina')


    def __init__(self, cod_user, cod_disc):
        self.cod_user = cod_user
        self.cod_dis = cod_disc


