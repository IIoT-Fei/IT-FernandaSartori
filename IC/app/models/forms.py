from flask_wtf import Form
from wtforms import StringField, PasswordField, BooleanField
from wtforms.validators import DataRequired

class LoginForm(Form):
    username = StringField("username", validators=[DataRequired()]) #diz que esses campos são obrogatórios
    password = PasswordField("password", validators=[DataRequired()]) #diz que esses campos são obrogatórios
    remember_me = BooleanField("remember_me") #para deixar dados "salvos"
    email = StringField("email")
    name = StringField("name")
    professor = BooleanField("professor")
    titulodis = StringField("titulodisc")


