#from flask_wtf import Form, validators

from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms import StringField, PasswordField, BooleanField, SelectField, DateTimeField
from wtforms.validators import DataRequired, StopValidation, Length, EqualTo, Optional
from wtforms.widgets import TextArea

from app.validators.validators import NotExistsInDb, RequiredIfChoice


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
    username = StringField("username", validators=[DataRequired(message="Nome de usuário requerido!"),NotExistsInDb("users", "Esse username já existe, por favor, escolha outro!")])
    password = PasswordField("password", validators=[DataRequired(message="Senha requerida!"),Length(min=6, max=25,message="Sua senha deve ter no mínimo 6 caracteres e no máximo 25!"),EqualTo("conf_password", message="As senhas devem ser correspondentes!")])
    conf_password = PasswordField("conf_password", validators=[DataRequired(message="Confirmação de senha requerida!"),Length(min=6, max=25,message="Sua senha deve ter no mínimo 6 caracteres e no máximo 25!")])
    email = StringField("email", validators=[DataRequired(message="E-mail requerido!"),NotExistsInDb("users", "Este e-mail já está cadastrado, por favor, digite outro!")])
    name = StringField("name", validators=[DataRequired(message="Nome completo requerido!")])

class Submissoes(FlaskForm):
    linguagem = SelectField("linguagem", choices=[('cpp', 'C++'), ('py', 'Python'), ('c', 'C'), ('java', 'Java')])
    #anexo = PasswordField("anexo", validators=[DataRequired()])
    xnt = "c java py h cpp exe zip rar"
    arquivo = FileField(validators=[FileAllowed(xnt.split(" "), "As extensões permitidas são somente: " + xnt), FileRequired("Arquivo requerido!!!")])
    #file = FileField("file", validators=[FileRequired("blablabla")])

class Novadisciplina(FlaskForm):
    #codigo = StringField("codigo", validators=[NotExistsInDb(Disciplina, Disciplina.codigo_disc, "Já existe!"), DataRequired(message="Código da disciplina requerido!")])
    #codigo = StringField("codigo", validators=[DataRequired(message="Código da disciplina requerido!")])
    codigo = StringField("codigo", validators=[NotExistsInDb("disciplina", "Já existe uma disciplina com esse código, por favor, escolha outro!"), DataRequired(message="Código da disciplina requerido!")])
    nome = StringField("nome", validators=[DataRequired(message="Título da disciplina requerido!")])
    conf_chave = PasswordField("conf_chave")
    chave = PasswordField("chave", validators=[Optional(), Length(min=6, max=25,message="Sua senha deve ter no mínimo 6 caracteres e no máximo 25!"),EqualTo("conf_chave", message="As senhas devem ser correspondentes!")])
    xnt = "png jpg "
    arquivo = FileField(validators=[FileAllowed(xnt.split(" "), "As extensões permitidas são somente: " + xnt),
                                    FileRequired("Arquivo requerido!!!")])
    visivel = BooleanField("visivel")

class NovoConvite(FlaskForm):
    nome = StringField("nome", validators=[DataRequired(message="Nome do professor convidado requerido!")])
    email = StringField("email", validators=[DataRequired(message="E-mail do professor convidado requerido!")])
    mensagem = StringField("mensagem", widget=TextArea(), validators=[DataRequired(message="Mensagem para o professor requerida!")])

class EdtDisc(FlaskForm):
    titulo = StringField("titulo", validators=[DataRequired(message="Título da disciplina requerido!")])
    chave = PasswordField("chave", validators=[Length(min=6, max=25,message="Sua senha deve ter no mínimo 6 caracteres e no máximo 25!")])
    xnt = "txt pdf zip rar png jpg docx"
    arquivo = FileField(validators=[FileAllowed(xnt.split(" "), "As extensões permitidas são somente: " + xnt)])

class Perfil(FlaskForm):
    password = PasswordField("password", validators=[DataRequired(message="Senha requerida!"), Length(min=6, max=25,message="Sua senha deve ter no mínimo 6 caracteres e no máximo 25!")])

class NovoLab(FlaskForm):
    titulo = StringField("titulo", validators=[DataRequired(message="Título do novo Labortatório requerido!")])
    xnt = "pdf txt docx"
    arquivo = FileField(validators=[FileAllowed(xnt.split(" "), "As extensões permitidas são somente: " + xnt), FileRequired("Arquivo requerido!!!")])
    visivel = BooleanField("visivel")
    data = DateTimeField(validators=[DataRequired("Data requerida")],format='%Y-%m-%dT%H:%M')
    comparacao = StringField("comparacao",widget=TextArea(), validators=[DataRequired(message="Saída de comparação requerida requerido!")])
    substituicao = BooleanField("substituicao")
    codigo = StringField("codigo",widget=TextArea(), validators=[RequiredIfChoice("substituicao")])

class EdtLab(FlaskForm):
    titulo = StringField("titulo", validators=[DataRequired(message="Título do novo Labortatório requerido!")])
    xnt = "pdf txt docx"
    arquivo = FileField(validators=[FileAllowed(xnt.split(" "), "As extensões permitidas são somente: " + xnt)])
