from flask.json import jsonify

from app import app
from flask_login import login_user, logout_user
from app import db  # do módulo app (pasta app) importo a variável app do __init__
from flask import render_template, request, session
from flask import flash
from flask import redirect, url_for
from app.models.forms import LoginForm
from app.models.tables import User, Lab, Disciplina, Convite, Envios, User_Disciplina  # importei a tabela Users
from app import lm
from datetime import datetime
from sqlalchemy import and_


# from flask.ext.images import resized_img_src


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
    form = LoginForm(request.form)
    print("entrei na funcao")
    if form.validate_on_submit():  # se o login for válido, embora não sei se está correto
        print(form.username.data)
        user = User.query.filter_by(username=form.username.data).first()  # estou checando se existe o nome de usuario que o usuario inseriu
        print("check 1")
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
            print("check 4")
            flash("Invalid Login!")  # retorna uma mensagem


    else:

        print(form.errors)

    return render_template('login.html', form=form)


@app.route("/Home", methods=["GET", "POST"])
def home():
    #form = LoginForm()
    #user = User.query.filter_by().first()  # estou checando se existe o nome de usuario que o usuario inseriu
    user = User.query.filter_by(id=session['user']).first()
    if user and user.professor == 1:  # estou testando se user existe e se a senha inseria é igual a senha cadastrada,
        return redirect(url_for("homeprofessor"))  # faz o redirecionamento à outra função
    else:
        return redirect(url_for("homealuno"))


@app.route("/", methods=["GET", "POST"])
def default():
    disc = User_Disciplina.query.filter_by(cod_user=session['user']).all()
    return render_template('view2.html', disc=disc)


@app.route("/cadastroaluno", methods=["GET", "POST"])
def cadastroaluno():
    if request.method == 'POST':
        nome_user = request.form.get("NomeUser")
        nome = request.form.get("Nome")
        email = request.form.get("Email")
        senha = request.form.get("Senha")

    return render_template('CadastroAluno.html')


@app.route("/agradecimentos", methods=["GET", "POST"])
def agradecimentos():
    return render_template('Agradecimentos.html')


@app.route("/cadastroprofessor", methods=["GET", "POST"])
def cadastroprof():
    form = LoginForm()
    return render_template('CadastroProfessor.html', form=form)


@app.route("/envioarquivo", methods=["GET", "POST"])
def envioarq():
    return render_template('EnvioArquivo.html')


@app.route("/cadastro", methods=["GET", "POST"])
def cadastro():
    form = LoginForm()
    if request.method == 'POST':
        nome_user = request.form.get("NomeUser")
        nome = request.form.get("Nome")
        email = request.form.get("Email")
        senha = request.form.get("Senha")
        conf_senha = request.form.get("ConfSenha")
        if senha == conf_senha:
            i = User(nome_user, senha, nome,email, True)
            db.session.add(i)
            db.session.commit()
            return render_template('HomeProf2.html')
        else:
            return "Erro ao inserir"
    return render_template('CadastroProfessor.html', form=form)


@app.route("/logout")
def logout():
    logout_user()
    flash("Logged out!")
    return redirect(url_for("logar"))


@app.route("/edicao", methods=["GET", "POST"])
def edicao():
    disc_id = request.args.get("disc")
    disciplina = Disciplina.query.filter_by(id = disc_id).first()

    if request.method == "POST":
        novotitulo = request.form.get("Titulo")
        novachave = request.form.get("Chave")
        novologo = request.form.get("Imagem")
        disciplina.nome_disc = novotitulo
        disciplina.chave = novachave  # pego o registro que já usei lá em cima, e altero o name dele
        disciplina.logo = novologo
        db.session.add(disciplina)
        db.session.commit()
        return redirect(url_for("home"))
    return render_template('Edicao.html', disciplina=disciplina)


@app.route("/enviosub", methods=["GET", "POST"])
def envsub():
    lab = Lab.query.filter_by(id=1).first()
    env = Envios.query.filter_by(cod_lab=1).all()
    id_ = request.args.get("lab_id")
    r = Lab.query.filter_by(id=id_).first()  # estou selecionandos todos os registros filtrados por um campo
    u = Envios.query.filter_by(cod_lab=id_).all()
    envios = Envios.query.filter(and_(Envios.cod_lab == id_, Envios.cod_user == session['user'])).all()
    language = ['C', 'C++', 'Java', 'Python']
    #print(session['user'])
    if request.method == 'POST':
        linguagem = request.form.get("linguagem")
        print(linguagem)
        now = datetime.now()
        lab = Envios("Aprovado", "---", session['user'], id_, now)  # passando os parametros que quero inserir
        db.session.add(lab)
        db.session.commit()
        r = Lab.query.filter_by(id=id_).first()  # estou selecionandos todos os registros filtrados por um campo
        u = Envios.query.filter_by(cod_lab=id_).all()
        return render_template('EnvioSubmissao.html', lab=r, env=envios)

    return render_template('EnvioSubmissao.html', lab=r, env=envios)


@app.route("/homeProfessor", methods=["GET", "POST"])
def homeprofessor():
    disc = Disciplina.query.filter(and_(Disciplina.id_prof == session['user'], Disciplina.excluir == False)).all()
    return render_template('HomeProf2.html', disc=disc)


@app.route("/NovaDiscp", methods=["GET", "POST"])
def novadisc():
    form = LoginForm()
    if request.method == 'POST':
        titulo = request.form.get("Titulo")
        nome = request.form.get("Nome")
        chave = request.form.get("Chave")
        conf_chave = request.form.get("Confchave")
        logo = request.form.get("Imagem")
        visivel = request.form.get("Visivel")
        id_user = session['user']
        print(titulo)
        if chave == conf_chave:
            i = Disciplina(titulo, logo, nome, chave, id_user, False, visivel)
            db.session.add(i)
            db.session.commit()
            return redirect(url_for("home"))

        else:

            return ("Erro ao gravar")

    return render_template('NovaDisciplina.html', form=form)


@app.route("/Perfil", methods=["GET", "POST"])
def perfil():
    form = LoginForm()
    r = User.query.filter_by(id=session['user']).first()  # estou selecionandos o primeiro dos registros filtrados por um campo

    if request.method == "POST":
        novoemail = request.form.get("Email")
        novasenha = request.form.get("Senha")
        r.email = novoemail  # pego o registro que já usei lá em cima, e altero o name dele
        r.password = novasenha
        db.session.add(r)
        db.session.commit()  # salvo
    return render_template('Perfil.html', user=r, form=form)


@app.route("/homealuno", methods=["GET", "POST"])
def homealuno():
    disc = User_Disciplina.query.filter_by(cod_user=session['user']).all()
    #b = User_Disciplina.query.filter(and_(User_Disciplina.cod_user == session['user'], User_Disciplina.disc.excluir == False)).all()
    b = User_Disciplina.query.filter(and_(User_Disciplina.cod_user == session['user'], User_Disciplina.disc.has(excluir = False))).all()

    return render_template('view2.html', disc=b)


@app.route("/inscricaoDisc", methods=["GET", "POST"])
def inscricao():
    return render_template('InscricaoDisc.html')


@app.route("/escolhaExerc", methods=["GET", "POST"])
def exercicio():
    disc_id = request.args.get("disc_id")
    labs = Lab.query.filter(and_(Lab.disciplina_id == disc_id, Lab.excluir == False, Lab.visivel == True)).all()
    r = Envios.query.filter_by(cod_lab=disc_id).first()
    v = []
    S = 2

    for la in labs :

        envios = Envios.query.filter_by(cod_lab = la.id).all()
        S = 2
        for e in envios :

            if(e.status == "Aprovado"):
                S=0
            elif( S != 0 and e.status == "Reprovado"):
                S=1
            elif (S!=0 and S!=1):
                S=2
        v.append(S)
        print(v)

    dados = zip(labs, v)


    return render_template('EscolhaExercicio.html', lab=dados, laboratorios = labs, r=r)


@app.route("/menudaDisc", methods=["GET", "POST"])
def menudisc():
    id_ = request.args.get("disc")
    #lab = Lab.query.filter_by(id=id_).all()
    return render_template('MenudaDisciplina.html', id=id_)


@app.route("/escolhaLab", methods=["GET", "POST"])
def escolhaLab():
    id_ = request.args.get("disc")
    #lab = Lab.query.filter_by(disciplina_id=id_).all()
    lab = Lab.query.filter(and_(Lab.disciplina_id == id_, Lab.excluir == False)).all()
    return render_template('EscolhaLab2.html', lab=lab, disc_id=id_)


@app.route("/novoLab", methods=["GET", "POST"])
def novoLab():
    disc_id= request.args.get("disc")
    if request.method == 'POST':

        nome = request.form.get("Titulo")
        data = request.form.get("dataentrega")
        arquivo = request.form.get("Arquivo")
        visivel = request.form.get("Visivel")

        i = Lab(nome, arquivo, data, disc_id, False, visivel)
        db.session.add(i)
        db.session.commit()
        return redirect(url_for("escolhaLab", disc = disc_id))



    return render_template('NovoLab.html', disc_id=disc_id)


@app.route("/relatorios", methods=["GET", "POST"])
def relatorios():
    disc_id = request.args.get("disc_id")
    laboratorios = Lab.query.filter_by(disciplina_id = disc_id).all()
    alunos = User_Disciplina.query.filter_by(cod_dis = disc_id).all()


    labs = Lab.query.filter(and_(Lab.disciplina_id == disc_id, Lab.excluir == False, Lab.visivel == True)).all()

    v = []
    S = 2


    for la in labs:
        for al in alunos:
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
    v.append(S)
    print(v)

    dados = zip(labs, v)


    return render_template('Relatorios.html', disc_id = disc_id, labs = labs, alunos=alunos, dados = dados)


@app.route("/novoProfessor", methods=["GET", "POST"])
def novoProfessor():
    if request.method == 'POST':
        nome = request.form.get("Nome")
        email = request.form.get("Email")
        texto = request.form.get("Texto")
        usuario = session['user']
        i = Convite(nome, email, texto, usuario)
        db.session.add(i)
        db.session.commit()
        return redirect(url_for("homeprofessor"))

    return render_template('NovoProfessor.html')


@app.route("/editarLab", methods=["GET", "POST"])
def editarLab():

    disc_id = request.args.get("disc_id")
    id_ = request.args.get("lab_id")
    lab = Lab.query.filter_by(id=id_).first()

    if request.method == 'POST':
        print("check1")

        titulo_ = request.form.get("Titulo")
        anexo_ = request.form.get("Anexo")
        data_ = request.form.get("dataentrega")
        print(titulo_)
        lab.titulo= titulo_
        lab.anexo = anexo_
        lab.datahora = data_
        db.session.add(lab)
        db.session.commit()
        #print(disc_id)
        return redirect(url_for("escolhaLab", disc = disc_id))

    return render_template('EditarLab.html', lab_id=id_, lab = lab, disc_id= disc_id)


@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    # print("entrei na funcao")
    if form.validate_on_submit():  # se o login for válido, embora não sei se está correto
        print(form.username.data)
        print(form.password.data)
        user = User.query.filter_by(
            username=form.username.data).first()  # estou checando se existe o nome de usuario que o usuario inseriu
        # print("check 1")
        if user and user.password == form.password.data:  # estou testando se user existe e se a senha inseria é igual a senha cadastrada
            # print("check 2")
            login_user(user)
            # print("check 3")
            flash("Logged in")
            return redirect(url_for("html"))  # faz o redirecionamento à outra função

        else:
            # print("check 4")
            flash("Invalid Login!")  # retorna uma mensagem

    else:
        print(form.errors)

    return render_template('loginbase.html', form=form)


# EXEMPLPO DO CREATE. ADICIONANDO UM REGISTRO AO BANCO DE DADOS
@app.route("/write/<info>")
@app.route("/write", defaults={"info": None})
def write(info):
    i = User("Mel", "1234", "Mel S B", "mel@fei.edu.br", False)  # passando os parametros que quero inserir

    db.session.add(i)  # sessao=periodo que meu usuario esta logado
    db.session.commit()  # é o salvamento de informações, a sessao é temporaria, logo, para não perder, eu as salvo com o commit
    return "Ok, foi adicionado com sucesso!!"


# EXEMPLPO DO READ. LENDO OS REGISTROS EXISTENTES
@app.route("/read/<info>")
@app.route("/read", defaults={"info": None})
def read(info):
    # r = User.query.filter_by(name = "Fernandinha").first() #estou selecionandos apenas um dos registros filtrados por um campo
    # r = User.query.order_by(User.username)#seleciona todos em ordem alfabética
    r = User.query.filter_by(password="1234").all()  # estou selecionandos todos os registros filtrados por um campo
    # print(r.username, r.name)
    print(r)
    # print(r.username, r.name, r.email, r.password) só funciona se vc imprimir usando first(), se for com all() ele dá erro
    return "Ok, foi lido com sucesso!"


# EXEMPLPO DO UPDATE. ALTERANDO ALGUM REGISTRO EXISTENTE
@app.route("/update/<info>")
@app.route("/update", defaults={"info": None})
def update(info):
    r = User.query.filter_by(username="Fernanda").first()  # estou pegando o primeiro registro que tem o username F
    r.name = "Fernandinha"  # pego o registro que já usei lá em cima, e altero o name dele
    db.session.add(r)
    db.session.commit()  # salvo
    return "Ok, foi modificado com sucesso!!"


# EXEMPLPO DO DELETE. DELETENANDO ALGUM REGISTRO EXISTENTE
@app.route("/delete/<info>")
@app.route("/delete", defaults={"info": None})
def delete(info):
    r = User.query.filter_by(username="fernandas").first()  # estou pegando o primeiro registro que tem o username F
    env = Envios.query.filter_by(id=15).first()
    if env:
        db.session.delete(env)  # estou deletando o registro selecionado na linha de cima
        db.session.commit()  # salvo
        return "Ok, deletado com sucesso!"
    else:
        return "Impossivel deletar, pois não existe :("


@app.route("/teste")
def teste():
    r = Lab.query.first()  # estou pegando o primeiro registro que tem o username F
    u = Envios.query.first()
    v = User_Disciplina.query.filter_by(cod_dis = 1).first()
    print(u.laboratorio.titulo)
    print(u.usuario.id)
    print(r.disciplina.nome_disc)
    print(v.dis.cod_disc)
    return "teste"


@app.route("/teste2")
def teste2():
    now = datetime.now()
    print(now)
    i = Lab("Lab5", "Descrição", "Arquivo", now)  # passando os parametros que quero inserir
    envio = Envios("Reprovado", "Erro de saída")
    db.session.add(envio)  # sessao=periodo que meu usuario esta logado
    db.session.commit()
    return "teste2"


@app.route("/listagemteste")
def listagemteste():
    l = Lab.query.all()

    return render_template('Listagem.html', labs=l)


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
def excluirdisc():
    disc_id = request.args.get("disc")
    r = Disciplina.query.filter_by(id=disc_id).first()  # estou pegando o primeiro registro que tem o username F
    r.excluir = True # pego o registro que já usei lá em cima, e altero o name dele
    db.session.add(r)
    db.session.commit()

    return redirect(url_for("homeprofessor"))

@app.route("/deixarDiscInv")
def deixardiscinv():
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
def excluirlab():
    lab_id = request.args.get("lab_id")
    r = Lab.query.filter_by(id=lab_id).first()  # estou pegando o primeiro registro que tem o username F
    disc_id = r.disciplina.id
    r.excluir = True # pego o registro que já usei lá em cima, e altero o name dele
    db.session.add(r)
    db.session.commit()

    return redirect(url_for("escolhaLab", disc = disc_id))

@app.route("/deixarLabInv")
def deixarlabinv():
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