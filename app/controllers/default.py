from functools import wraps

from flask.json import jsonify, dumps
import numpy as np
from app import app
from flask_login import login_user, logout_user
from app import db  # do módulo app (pasta app) importo a variável app do __init__
from flask import render_template, request, session, send_from_directory, current_app
from flask import flash
from flask import redirect, url_for
from app.models.forms import LoginForm, Cadastro, Submissoes, Novadisciplina, NovoConvite, EdtDisc, Perfil, NovoLab, \
    EdtLab
from app.models.tables import User, Lab, Disciplina, Convite, Envios, User_Disciplina  # importei a tabela Users
from app import lm
from datetime import datetime
from sqlalchemy import and_
import os
from flask import Flask
from werkzeug.utils import secure_filename
# from flask.ext.images import resized_img_src
from werkzeug.datastructures import CombinedMultiDict


ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'zip', 'rar', 'png', 'jpg', 'docx'])
ALLOWED_EXTENSIONS_SUBMISSION = set(['c','h','cpp','hpp','java','py', 'zip', 'rar'])


def checaLogado(controller):
    @wraps(controller)
    def empacotador():
        if "user" in session:
            print("t1")
            return controller()
        else:
            print("t2")
            return redirect(url_for("logar"))
    return empacotador

def ehProfessor():
    user = User.query.filter_by(id=session['user']).first()
    if user and user.professor == 1:
        return True
    else:
        return False


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def allowed_file_submission(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS_SUBMISSION

@lm.user_loader  # função que tem que ser colocada antes de tudo para carregar o usuario que esta logado e retornar os dados dele. Retorna os dados do usuario que esta logado no momento
def load_user(id):
    return User.query.filter_by(id=id).first()


# @app.route("/nome/<name>")
# @app.route("/nome", defaults={"name": None})  # função que retorna paginas html
# def nome(name):
#   if name:
#       return "Olá, %s!" %name
#    else:
#       return "Olá, usuário! "

# @app.route("/numero/<int:id>")# faz conversão para int
# def num(id):
#    print(type(id))
#    return ""

# @app.route("/", defaults={"user": None})
# @app.route("/index/<user>")
# def index(user):
#    return render_template('index.html', user=user)


@app.route("/logar", methods=["GET", "POST"])
def logar():
    #session.clear()
    #logout_user()
    #print("teste")
    form = LoginForm(request.form)
    #print("entrei na funcao")

    if form.validate_on_submit():  # se o login for válido, embora não sei se está correto
        print(form.username.data)
        user = User.query.filter_by(username=form.username.data).first()  # estou checando se existe o nome de usuario que o usuario inseriu
        #print("check 1")
        if user and user.password == form.password.data:  # estou testando se user existe e se a senha inseria é igual a senha cadastrada
            session['user'] = user.id
            session['professor'] = user.professor

            if user.professor == True:
                login_user(user)
                flash("Logged in")

                return redirect(url_for("homeprofessor"))  # faz o redirecionamento à outra função
            else:
                login_user(user)
                flash("Logged in")
                return redirect(url_for("homealuno"))  # faz o redirecionamento à outra função
        else:
            #print("check 4")
            flash("Invalid Login!")  # retorna uma mensagem


    else:

        print(form.errors)

    return render_template('login.html', form=form)

@app.route("/Home", methods=["GET", "POST"])
@checaLogado
def home():
    #form = LoginForm()
    #user = User.query.filter_by().first()  # estou checando se existe o nome de usuario que o usuario inseriu

    if ehProfessor(): # estou testando se user existe e se a senha inseria é igual a senha cadastrada,
        return redirect(url_for("homeprofessor"))  # faz o redirecionamento à outra função
    else:
        return redirect(url_for("homealuno"))


def checaProfessor(controller):
    @wraps(controller)
    def pacote():
        if ehProfessor():
            return controller()
        else:
            return "<h1>Not Found</h1> " \
                   "<h4> <p>The requested URL was not found on the server. " \
                   "If you entered the URL manually please check your spelling and try again.</h4> </p>"
    return pacote

def checaAluno(controller):
    @wraps(controller)
    def pacote():
        if not ehProfessor():
            return controller()
        else:
            return "<h1>Not Found</h1> " \
                   "<h4> <p>The requested URL was not found on the server. " \
                   "If you entered the URL manually please check your spelling and try again.</h4> </p>"
    return pacote

@app.route("/", methods=["GET", "POST"])
def default():

    logout_user()
    if "user" in session:
        return redirect(url_for("home"))
    else:
       session.clear()
       return redirect(url_for("logout"))

        #print (session)
    #disc = User_Disciplina.query.filter_by(cod_user=session['user']).all()
    #return redirect(url_for("logar"))


#@app.route("/cadastroaluno", methods=["GET", "POST"])
#def cadastroaluno():
#   if request.method == 'POST':
#        nome_user = request.form.get("NomeUser")
#        nome = request.form.get("Nome")
#        email = request.form.get("Email")
#        senha = request.form.get("Senha")

#    return render_template('CadastroAluno.html')


@app.route("/agradecimentos", methods=["GET", "POST"])
def agradecimentos():
    return render_template('Agradecimentos.html')


#@app.route("/cadastroprofessor", methods=["GET", "POST"])
#def cadastroprof():
#    form = LoginForm()
#    #user = User.query.filter_by(id=session['user']).first()
#    #if user.professor == True:
#    return render_template('CadastroProfessor.html', form=form)
#   # else:
#    #    return "<h1>Not Found</h1> " \
#    #           "<h4> <p>The requested URL was not found on the server. " \
#     #          "If you entered the URL manually please check your spelling and try again.</h4> </p>"

#@app.route("/envioarquivo", methods=["GET", "POST"])
#def envioarq():
#    return render_template('EnvioArquivo.html')


@app.route("/cadastro", methods=["GET", "POST"])
def cadastro():
    form = Cadastro(CombinedMultiDict((request.files, request.form)))
    #user = User.query.filter_by(id=session['user']).first()

    #if user.professor == True:

    if form.validate_on_submit():
        nome_user =  form.username.data
        nome = form.name.data
        email = form.email.data
        senha = form.password.data
        conf_senha = form.conf_password.data
        if senha == conf_senha:
            i = User(nome_user, senha, nome, email, True)
            db.session.add(i)
            db.session.commit()
            session['user'] = i.id
            return render_template('HomeProf2.html')
        else:
            return "Erro ao inserir"

    return render_template('CadastroProfessor.html', form=form)


@app.route("/logout")
def logout():
    logout_user()
    session.clear()
    #print("SAINDOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOO")
    #print(session['user'])
    flash("Logged out!")
    return redirect(url_for("logar"))


@app.route("/edicao", methods=["GET", "POST"])
@checaLogado
@checaProfessor
def edicao():
    form = EdtDisc(CombinedMultiDict((request.files, request.form)))
    disc_id = request.args.get("disc")
    disciplina = Disciplina.query.filter_by(id=disc_id).first()
    UPLOAD_FOLDER = './app/static/professores/'
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
    if disc_id == None:
        return " iohpeoidjdóij <h1>Not Found</h1> " \
               "<h4> <p>The requested URL was not found on the server. " \
               "If you entered the URL manually please check your spelling and try again.</h4> </p>"
    ud = Disciplina.query.filter(and_(Disciplina.id_prof == session['user'], Disciplina.id == disc_id)).all()
    if ud:
        print(00)
        if form.validate_on_submit():
            print (0)

            print("01")
            novotitulo = form.titulo.data
            print("02")
            novachave =  form.chave.data

            print(novachave)
            file = request.files['arquivo']
            disciplina.nome_disc = novotitulo

            print(1)

            if file.filename == '':
                print(2)
               #print("não selecionado")
                disciplina.nome_disc = novotitulo
                if novachave != "":
                   disciplina.chave = novachave
                   print(novachave)

                db.session.add(disciplina)
                db.session.commit()

                return redirect(url_for("home"))

            elif file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                print(3)

                filename = secure_filename(file.filename)

                disciplina.logo = filename
                disciplina.nome_disc = novotitulo
                if novachave != "":
                    disciplina.chave = novachave
                    print(novachave)
                    print(4)
                db.session.add(disciplina)
                db.session.commit()
                return redirect(url_for("home"))
            else:
                return redirect(url_for("home"))

    else:
        return "<h1>Not Found</h1> " \
               "<h4> <p>The requested URL was not found on the server. " \
               "If you entered the URL manually please check your spelling and try again.</h4> </p>"

    return render_template('Edicao.html', disciplina=disciplina, form=form)


@app.route("/enviosub", methods=["GET", "POST"])
@checaLogado
def envsub():
    form = Submissoes(CombinedMultiDict((request.files, request.form)))
    lab = Lab.query.filter_by(id=1).first()
    env = Envios.query.filter_by(cod_lab=1).all()
    id_ = request.args.get("lab_id")
    disc_id = request.args.get("disc_id")
    print("disc %s" % disc_id)
    #r = Lab.query.filter_by(id=id_).first()
    r = Lab.query.filter(and_(Lab.id== id_, Lab.disciplina_id == disc_id)).first()

    if disc_id == None:
        return " cwedec <h1>Not Found</h1> " \
        "<h4> <p>The requested URL was not found on the server. " \
        "If you entered the URL manually please check your spelling and try again.</h4> </p>"
    else:
        #u_s = User_Disciplina.query.filter(and_(User_Disciplina.cod_user == session['user'], User_Disciplina.cod_dis == disc_id)).first_or_404()
        user= User.query.filter_by(id=session['user']).first()
        uda = User_Disciplina.query.filter(and_(User_Disciplina.cod_dis == disc_id, User_Disciplina.cod_user == session['user'])).all()

        if ehProfessor():
            udp = Disciplina.query.filter(and_(Disciplina.id == disc_id, Disciplina.id_prof == session['user'])).all()
        else:
            uda = User_Disciplina.query.filter(
                and_(User_Disciplina.cod_dis == disc_id, User_Disciplina.cod_user == session['user'])).all()

        if (uda and r) or (udp and r):
            envios = Envios.query.filter(and_(Envios.cod_lab == id_, Envios.cod_user == session['user'])).all()
            print(form.data)

            if form.validate_on_submit():
                print("PASSOU!!!")

                user = User.query.filter_by(id=session['user']).first()
                #if user.professor == False:
                #u_s = User_Disciplina.query.filter(and_(User_Disciplina.cod_user == session['user'], User_Disciplina.cod_dis == disc_id)).first()
                #u_d= Lab.query.filter(and_(Lab.id == id_, Lab.disciplina_id == disc_id)).first()
                r = Lab.query.filter_by(id=id_).first()  # estou selecionandos todos os registros filtrados por um campo
                u = Envios.query.filter_by(cod_lab=id_).all()


                envios = Envios.query.filter(and_(Envios.cod_lab == id_, Envios.cod_user == session['user'])).all()

                UPLOAD_FOLDER = './app/static/submissões/'
                app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

                linguagem = form.linguagem.data

                now = datetime.now()
                file = request.files['arquivo']
                ext = file.filename.rsplit(".")[1]
                print(file.filename)

                if file.filename != '':

                    filename = secure_filename(str(user.id) +"_" + file.filename + "." + ext)
                    #filename = secure_filename(file.filename)
                    file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                    print(3)
                    print(form.data)
                    lab = Envios("Aprovado", "---", session['user'], id_, now, filename, linguagem)  # passando os parametros que quero inserir
                    db.session.add(lab)
                    db.session.commit()
                    r = Lab.query.filter_by(id=id_).first()  # estou selecionandos todos os registros filtrados por um campo
                    print("vou fazer o redirect")
                    return redirect(url_for("envsub", lab_id=id_, disc_id=disc_id))

                else:
                    print("não selecionado")
            else:
                print("Formulario novo ou erros")
                print(form.data)

        else:
            print("teste")
            return "<h1> 22222 Not Found</h1> " \
                  "<h4> <p>The requested URL was not found on the server. " \
                    "If you entered the URL manually please check your spelling and try again.</h4> </p>"

    return render_template('EnvioSubmissao.html', lab=r, env=envios, disc_id=disc_id, form=form)


@app.route("/homeProfessor", methods=["GET", "POST"])
@checaLogado
@checaProfessor
def homeprofessor():
    disc = Disciplina.query.filter(and_(Disciplina.id_prof == session['user'], Disciplina.excluir == False)).all()

    return render_template('HomeProf2.html', disc=disc)


@app.route("/NovaDiscp", methods=["GET", "POST"])
@checaLogado
@checaProfessor
def novadisc():
    form = Novadisciplina(CombinedMultiDict((request.files, request.form)))
    print(form)

    user = User.query.filter_by(id=session['user']).first()

    if form.validate_on_submit():

        #print("0")
        UPLOAD_FOLDER = './app/static/professores/'
        app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
        #form = NovaDisciplina(request.form)
        now = datetime.now()

        titulo = form.codigo.data
        nome = form.nome.data
        chave = form.chave.data
        conf_chave = form.conf_chave.data

        print(titulo)
        print(nome)
        print(chave)
        print(conf_chave)
        visivel = form.visivel.data
        print(visivel)
        #print("print 1")
        file = request.files['arquivo']
        #logo = filename + "azul";

        ext = file.filename.rsplit(".")[1]

        filename = secure_filename(str(user.id)+titulo+"."+ext)

        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        print(filename)

        if (chave != None):
            i = Disciplina(titulo, filename, nome, None, user.id, False, visivel)
        else:
            i = Disciplina(titulo, filename, nome, chave, user.id, False, visivel)

        db.session.add(i)
        db.session.commit()

        return redirect(url_for("home"))
    else:
        print(form.errors)

    return render_template('NovaDisciplina.html', form=form)


@app.route("/Perfil", methods=["GET", "POST"])
@checaLogado
def perfil():
    form = Perfil(request.form)
    r = User.query.filter_by(id=session['user']).first()  # estou selecionandos o primeiro dos registros filtrados por um campo

    if request.method == "POST":
        novasenha = form.password.data
        if novasenha != "":
            print("abcc")
            r = User.query.filter_by(username = r.username).first()  # estou pegando o primeiro registro que tem o username F
            r.password = novasenha  # pego o registro que já usei lá em cima, e altero o name dele
            db.session.add(r)
            db.session.commit()  # salvo
            return redirect(url_for("home"))
        else:
            return redirect(url_for("home"))

    return render_template('Perfil.html',user=r, form=form)

@app.route("/homealuno", methods=["GET", "POST"])
@checaLogado
@checaAluno
def homealuno():
    user = User.query.filter_by(id=session['user']).first()

    disc = User_Disciplina.query.filter_by(cod_user=session['user']).all()
    #b = User_Disciplina.query.filter(and_(User_Disciplina.cod_user == session['user'], User_Disciplina.disc.excluir == False)).all()
    b = User_Disciplina.query.filter(and_(User_Disciplina.cod_user == session['user'], User_Disciplina.disc.has(excluir = False))).all()


    return render_template('view2.html', disc=b)


#@app.route("/inscricaoDisc", methods=["GET", "POST"])
#def inscricao():
#    return render_template('InscricaoDisc.html')


@app.route("/escolhaExerc", methods=["GET", "POST"])
@checaLogado
def exercicio():
    disc_id = request.args.get("disc_id")

    if disc_id == None:
        return "<h1>Not Found</h1> " \
               "<h4> <p>The requested URL was not found on the server. " \
               "If you entered the URL manually please check your spelling and try again.</h4> </p>"

    #u_d = User_Disciplina.query.filter(and_(User_Disciplina.cod_user == session['user'], User_Disciplina.cod_dis == disc_id)).first_or_404()


    labs = Lab.query.filter(and_(Lab.disciplina_id == disc_id, Lab.excluir == False, Lab.visivel == True)).all()
    r = Envios.query.filter_by(cod_lab=disc_id).first()
    v = []
    S = 2
    # envios = Envios.query.filter_by(cod_lab = la.id).all()
    for la in labs :
        envios = Envios.query.filter(and_(Envios.cod_user == session['user'], Envios.cod_lab == la.id)).all()
        S = 2
        for e in envios:

            if(e.status == "Aprovado"):
                S=0
            elif( S != 0 and e.status == "Reprovado"):
                S=1
            elif (S!=0 and S!=1):
                S=2
        v.append(S)
    print(v)

    dados = zip(labs, v)


    return render_template('EscolhaExercicio.html', lab=dados, laboratorios = labs, r=r, disc_id=disc_id)


@app.route("/menudaDisc", methods=["GET", "POST"])
@checaLogado
@checaProfessor
def menudisc():

    user = User.query.filter_by(id=session['user']).first()

    id_ = request.args.get("disc")
    if id_ == None:
        return "<h1>Not Found</h1> " \
               "<h4> <p>The requested URL was not found on the server. " \
               "If you entered the URL manually please check your spelling and try again.</h4> </p>"
    #lab = Lab.query.filter_by(id=id_).all()
    ud = Disciplina.query.filter(and_(Disciplina.id_prof == session['user'], Disciplina.id ==id_)).all()
    if ud:
        return render_template('MenudaDisciplina.html', id=id_)
    else:
        return "<h1>Not Found</h1> " \
               "<h4> <p>The requested URL was not found on the server. " \
               "If you entered the URL manually please check your spelling and try again.</h4> </p>"


@app.route("/escolhaLab", methods=["GET", "POST"])
@checaLogado
@checaProfessor
def escolhaLab():
    id_ = request.args.get("disc")
    if id_ == None:
        return "<h1>Not Found</h1> " \
               "<h4> <p>The requested URL was not found on the server. " \
               "If you entered the URL manually please check your spelling and try again.</h4> </p>"
    user = User.query.filter_by(id=session['user']).first()
    ud = Disciplina.query.filter(and_(Disciplina.id_prof == session['user'], Disciplina.id == id_)).all()
    if ud:
        #lab = Lab.query.filter_by(disciplina_id=id_).all()
        lab = Lab.query.filter(and_(Lab.disciplina_id == id_, Lab.excluir == False)).all()
        return render_template('EscolhaLab2.html', lab=lab, disc_id=id_)
    else:
        return "<h1>Not Found</h1> " \
               "<h4> <p>The requested URL was not found on the server. " \
               "If you entered the URL manually please check your spelling and try again.</h4> </p>"


@app.route("/novoLab", methods=["GET", "POST"])
@checaLogado
@checaProfessor
def novoLab():
    formulario = NovoLab(CombinedMultiDict((request.files, request.form)))
    user = User.query.filter_by(id=session['user']).first()

    disc_id= request.args.get("disc")
    UPLOAD_FOLDER = './app/static/EnviosLab'
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

    print("dataaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa")
    data = request.form.get("data")
    print(data)
    if formulario.validate_on_submit():

        nome = request.form.get("titulo")
        data = request.form.get("data")
        visivel = request.form.get("visivel")
        saida = request.form.get("comparacao")
        now = datetime.now()
        substituicao = request.form.get("substituicao")
        file = request.files['arquivo']
        ext = file.filename.rsplit(".")[1]

        filename = secure_filename(str(user.id) + nome + "." + ext)
        #filename = secure_filename(file.filename)

        print(nome)
        print("dataaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa")
        print(data)
        print(visivel)
        print(filename)
        cod_subs = None

        cod_subs = request.form.get("codigo")
        print("cooooooooooodigoooooooooo")
        print(cod_subs)

        print("entreiiiii")
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        print(filename)
        i = Lab(nome, filename, data, disc_id, False, visivel,saida, cod_subs)
        db.session.add(i)
        db.session.commit()
        print(5)


        return redirect(url_for("escolhaLab", disc=disc_id))


    return render_template('NovoLab.html', disc_id=disc_id, form=formulario)


@app.route("/relatorios", methods=["GET", "POST"])
@checaLogado
@checaProfessor
def relatorios():

    user = User.query.filter_by(id=session['user']).first()


    disc_id = request.args.get("disc_id")
    laboratorios = Lab.query.filter_by(disciplina_id = disc_id).all()
    alunos = User_Disciplina.query.filter_by(cod_dis = disc_id).all()
    qtdalunos = User_Disciplina.query.filter_by(cod_dis=disc_id).count()

    labs = Lab.query.filter(and_(Lab.disciplina_id == disc_id, Lab.excluir == False, Lab.visivel == True)).all()
    qtdlabs = Lab.query.filter(and_(Lab.disciplina_id == disc_id, Lab.excluir == False, Lab.visivel == True)).count()


    l_alunos = []
    totais = []


    for al in alunos:
        #print(la)
        l = []
        total = [0, 0, 0]
        for la in labs:
            #print(al)
            envios = Envios.query.filter(and_(Envios.cod_lab == la.id, Envios.cod_user == al.id)).all()
            #envios = Envios.query.filter_by(cod_lab=la.id).all()
            S = 2
            for e in envios:
                if (e.status == "Aprovado"):
                    S = 0

                elif (S != 0 and e.status == "Reprovado"):
                    S = 1

                elif (S != 0 and S != 1):
                    S = 2

            total[S] += 1
            l.append(S)
        totais.append(total)

        l_alunos.append(l)


    #dados = zip(l,labs )


    return render_template('Relatorios.html', disc_id = disc_id, labs = labs, alunos=alunos, dados = l_alunos, totais=totais, qtdlabs = qtdlabs, qtdalunos=qtdalunos)


@app.route("/novoProfessor", methods=["GET", "POST"])
@checaLogado
@checaProfessor
def novoProfessor():
    form = NovoConvite(request.form)
    user = User.query.filter_by(id=session['user']).first()
    print(user.id)

    if request.method == 'POST':
        if form.validate_on_submit():
            nome = form.nome.data
            email = form.email.data
            texto = form.mensagem.data
            usuario = user.id
            #print(nome)
            #print(email)
            #print(texto)
            #print(usuario)

            i = Convite(nome, email, texto, usuario)  # passando os parametros que quero inserir#
            db.session.add(i)  # sessao=periodo que meu usuario esta logado
            db.session.commit()
            return redirect(url_for("homeprofessor"))
        else:
            print(form.errors)


    return render_template('NovoProfessor.html', form=form)


@app.route("/editarLab", methods=["GET", "POST"])
@checaLogado
@checaProfessor
def editarLab():
    form = EdtLab(CombinedMultiDict((request.files, request.form)))
    user = User.query.filter_by(id=session['user']).first()
    disc_id = request.args.get("disc_id")
    id_ = request.args.get("lab_id")
    lab = Lab.query.filter_by(id=id_).first()

    if form.validate_on_submit():

        UPLOAD_FOLDER = './EnviosLab/'
        app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

        novotitulo = form.titulo.data
        novadata = request.form['dataentrega']
        file = request.files['arquivo']
        filename = secure_filename(file.filename)

        print(novadata)


        if file.filename != '':
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            print(3)
            filename = secure_filename(file.filename)
            lab.arquivo = filename

        if novotitulo != "":
            lab.titulo = novotitulo

        if novadata != "":
            lab.datahora = novadata


        db.session.add(lab)
        db.session.commit()
        return redirect(url_for("escolhaLab", disc = disc_id))



    return render_template('EditarLab.html', lab_id=id_, lab = lab, disc_id= disc_id, form=form)


#@app.route("/login", methods=["GET", "POST"])
#def login():
#    form = LoginForm()
#    # print("entrei na funcao")
# #   if form.validate_on_submit():  # se o login for válido, embora não sei se está correto
# #       print(form.username.data)
#  #      print(form.password.data)
# #       user = User.query.filter_by(
#            username=form.username.data).first()  # estou checando se existe o nome de usuario que o usuario inseriu
#        # print("check 1")
#        if user and user.password == form.password.data:  # estou testando se user existe e se a senha inseria é igual a senha cadastrada
#            # print("check 2")
#            login_user(user)
#            # print("check 3")
#            flash("Logged in")
#            return redirect(url_for("html"))  # faz o redirecionamento à outra função
#
#       else:
#            # print("check 4")
#            flash("Invalid Login!")  # retorna uma mensagem
#
#    else:
#        print(form.errors)
#
#    return render_template('loginbase.html', form=form)


# EXEMPLPO DO CREATE. ADICIONANDO UM REGISTRO AO BANCO DE DADOS
#@app.route("/write/<info>")
#@app.route("/write", defaults={"info": None})
#def write(info):
#    i = User("Mel", "1234", "Mel S B", "mel@fei.edu.br", False)  # passando os parametros que quero inserir#
#
#    db.session.add(i)  # sessao=periodo que meu usuario esta logado
#    db.session.commit()  # é o salvamento de informações, a sessao é temporaria, logo, para não perder, eu as salvo com o commit
#   return "Ok, foi adicionado com sucesso!!"


## EXEMPLPO DO READ. LENDO OS REGISTROS EXISTENTES
#@app.route("/read/<info>")
#@app.route("/read", defaults={"info": None})
#def read(info):
#    # r = User.query.filter_by(name = "Fernandinha").first() #estou selecionandos apenas um dos registros filtrados por um campo
#    # r = User.query.order_by(User.username)#seleciona todos em ordem alfabética
#    r = User.query.filter_by(password="1234").all()  # estou selecionandos todos os registros filtrados por um campo
#    # print(r.username, r.name)
#    print(r)
#    # print(r.username, r.name, r.email, r.password) só funciona se vc imprimir usando first(), se for com all() ele dá erro
#    return "Ok, foi lido com sucesso!"


# EXEMPLPO DO UPDATE. ALTERANDO ALGUM REGISTRO EXISTENTE
#@app.route("/update/<info>")
#@app.route("/update", defaults={"info": None})
#def update(info):
#    r = User.query.filter_by(username="Fernanda").first()  # estou pegando o primeiro registro que tem o username F
#    r.name = "Fernandinha"  # pego o registro que já usei lá em cima, e altero o name dele
#    db.session.add(r)
#    db.session.commit()  # salvo
#    return "Ok, foi modificado com sucesso!!"


# EXEMPLPO DO DELETE. DELETENANDO ALGUM REGISTRO EXISTENTE
#@app.route("/delete/<info>")
#@app.route("/delete", defaults={"info": None})
#def delete(info):
#    r = User.query.filter_by(username="fernandas").first()  # estou pegando o primeiro registro que tem o username F
#    env = Envios.query.filter_by(id=15).first()
#    if env:
#        db.session.delete(env)  # estou deletando o registro selecionado na linha de cima
#        db.session.commit()  # salvo
#        return "Ok, deletado com sucesso!"
#    else:
#        return "Impossivel deletar, pois não existe :("


#@app.route("/teste")
#def teste():
#    r = Lab.query.first()  # estou pegando o primeiro registro que tem o username F
#    u = Envios.query.first()
#    v = User_Disciplina.query.filter_by(cod_dis = 1).first()
#    print(u.laboratorio.titulo)
#    print(u.usuario.id)
#    print(r.disciplina.nome_disc)
#    print(v.dis.cod_disc)
#    return "teste"


#@app.route("/teste2")
#def teste2():
#    now = datetime.now()
#    print(now)
#    i = Lab("Lab5", "Descrição", "Arquivo", now)  # passando os parametros que quero inserir
#    envio = Envios("Reprovado", "Erro de saída")
#    db.session.add(envio)  # sessao=periodo que meu usuario esta logado
#    db.session.commit()
#    return "teste2"


#@app.route("/listagemteste")
#def listagemteste():
#    l = Lab.query.all()
#
#    return render_template('Listagem.html', labs=l)


@app.route("/detalhesLab")
def detalhesLab():
    id_ = request.args.get("lab_id")
    r = Lab.query.filter_by(id=id_).first()  # estou selecionandos todos os registros filtrados por um campo
    u = Envios.query.filter_by(cod_lab = id_).all()

    return render_template('EnvioSubmissao.html', lab=r, env=u)

@app.route("/listardisciplinas")
def listardisc():
    disc = User_Disciplina.query.filter_by(cod_user=1).all()
    return render_template('listagemdisc.html', disc = disc)

@app.route("/testelab")
def testelab():
    return render_template('EscolhaLab3.html')

@app.route("/excluirDisc")
@checaLogado
@checaProfessor
def excluirdisc():
    user = User.query.filter_by(id=session['user']).first()
    disc_id = request.args.get("disc")
    r = Disciplina.query.filter_by(id=disc_id).first()  # estou pegando o primeiro registro que tem o username F
    r.excluir = True # pego o r egistro que já usei lá em cima, e altero o name dele
    db.session.add(r)
    db.session.commit()

    return redirect(url_for("homeprofessor"))


@app.route("/deixarDiscInv")
@checaLogado
@checaProfessor
def deixardiscinv():

    user = User.query.filter_by(id=session['user']).first()
    disc_id = request.args.get("disc")
    r = Disciplina.query.filter_by(id=disc_id).first()  # estou pegando o primeiro registro que tem o username F
    if r.visivel == False:
        r.visivel = True
    else:
        r.visivel = False
    db.session.add(r)
    db.session.commit()

    return redirect(url_for("homeprofessor"))



@app.route("/excluirLab")
@checaLogado
@checaProfessor
def excluirlab():
    user = User.query.filter_by(id=session['user']).first()

    lab_id = request.args.get("lab_id")
    r = Lab.query.filter_by(id=lab_id).first()  # estou pegando o primeiro registro que tem o username F
    disc_id = r.disciplina.id
    r.excluir = True # pego o registro que já usei lá em cima, e altero o name dele
    db.session.add(r)
    db.session.commit()
    return redirect(url_for("escolhaLab", disc=disc_id))


@app.route("/deixarLabInv")
@checaLogado
@checaProfessor
def deixarlabinv():

    user = User.query.filter_by(id=session['user']).first()


    disc_id = request.args.get("disc_id")
    print(disc_id)
    lab_id = request.args.get("lab_id")
    r = Lab.query.filter_by(id=lab_id).first()  # estou pegando o primeiro registro que tem o username F
    if r.visivel == False:
        r.visivel = True
    else:
        r.visivel = False
    db.session.add(r)
    db.session.commit()
    return redirect(url_for("escolhaLab", disc = disc_id))


#@app.route('/upload', methods=['GET', 'POST'])
#def upload_file():
#    if request.method == 'POST':
#        # check if the post request has the file part
#        print(0)
#        file = request.files['file']
#        if file and allowed_file(file.filename) == False:
#            print(file)#
#
#            return "incompatível"
#        # if user does not select file, browser also
#        # submit a empty part without filename
#        if file.filename == '':
#            print(2)
#            flash('No selected file')
#            return "não selecionado"
#        if file and allowed_file(file.filename):
#            filename = secure_filename(file.filename)
#            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
#            print(filename)
 #           return "funfou"
 #   return render_template('EnvioTeste.html')


@app.route("/download", methods=["GET", "POST"])
def download():
    UPLOAD_FOLDER = './EnviosLab/'
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
    r = Lab.query.filter_by(id=1).first()
    uploads = os.path.join(current_app.root_path, app.config['UPLOAD_FOLDER'])
    return send_from_directory(directory=uploads, filename=r.arquivo)