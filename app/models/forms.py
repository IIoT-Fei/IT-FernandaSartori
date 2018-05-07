#from flask_wtf import Form, validators

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SelectField
from wtforms.validators import DataRequired, Required, StopValidation, Length, EqualTo
from wtforms.widgets import TextArea
from flask_wtf.file import FileField, FileRequired, FileAllowed


def checa(form, field):
    if field.data:
        raise StopValidation("blabla")
def extensao(form, field):
    if field.data == None:
        raise StopValidation("Arquivo não selecionado!!!")

class LoginForm(FlaskForm):
    #username = StringField("username", validators=[DataRequired(message="Usuário requerido")]) #diz que esses campos são obrogatórios
    username = StringField("username", validators=[DataRequired(message="Usuário requerido!")])  # diz que esses campos são obrogatórios
    password = PasswordField("password", validators=[DataRequired(message="Senha requerida!")]) #diz que esses campos são obrogatórios
    #password = PasswordField("password", [validators.Required("Please include a password.")])
    #remember_me = BooleanField("remember_me") #para deixar dados "salvos"
    email = StringField("email")
    name = StringField("name")
    professor = BooleanField("professor")
    #titulodis = StringField("titulodisc")

class Cadastro(FlaskForm):
    username = StringField("username", validators=[DataRequired(message="Nome de usuário requerido!")])
    password = PasswordField("password", validators=[DataRequired(message="Senha requerida!"),Length(min=6, max=25,message="Sua senha deve ter no mínimo 6 caracteres e no máximo 25!"),EqualTo("conf_password", message="As senhas devem ser correspondentes!")])
    conf_password = PasswordField("conf_password", validators=[DataRequired(message="Confirmação de senha requerida!"),Length(min=6, max=25,message="Sua senha deve ter no mínimo 6 caracteres e no máximo 25!")])
    email = StringField("email", validators=[DataRequired(message="E-mail requerido!")])
    name = StringField("name", validators=[DataRequired(message="Nome completo requerido!")])

class Submissoes(FlaskForm):
    linguagem = SelectField("linguagem", choices=[('cpp', 'C++'), ('py', 'Python'), ('c', 'C'), ('java', 'Java')])
    #anexo = PasswordField("anexo", validators=[DataRequired()])
    xnt = "c java png jpeg"

    arquivo = FileField(validators=[FileAllowed(xnt.split(" "), "As extensões permitidas são somente: " + xnt), FileRequired("Arquivo requerido!!!")])
    #file = FileField("file", validators=[FileRequired("blablabla")])

class Novadisciplina(FlaskForm):
    codigo = StringField("codigo", validators=[DataRequired(message="Código da disciplina requerido!")])
    nome = StringField("nome", validators=[DataRequired(message="Título da disciplina requerido!")])
    conf_chave = PasswordField("conf_chave", validators=[DataRequired(message="Confirmação de chave requerida!")])
    chave = PasswordField("chave", validators=[DataRequired(message="Chave requerida!")])
    visivel = BooleanField("visivel")

class NovoConvite(FlaskForm):
    nome = StringField("nome", validators=[DataRequired(message="Nome do professor convidado requerido!")])
    email = StringField("email", validators=[DataRequired(message="E-mail do professor convidado requerido!")])
    mensagem = StringField("mensagem", widget=TextArea(), validators=[DataRequired(message="Mensagem para o professor requerida!")])

class EdtDisc(FlaskForm):
    titulo = StringField("titulo", validators=[DataRequired(message="Título da disciplina requerido!")])
    chave = PasswordField("chave" , validators=[DataRequired(message="Chave da disciplina requerida!")])

class Perfil(FlaskForm):
    password = PasswordField("password", validators=[DataRequired(message="Senha requerida!"), Length(min=6, max=25,message="Sua senha deve ter no mínimo 6 caracteres e no máximo 25!")])


