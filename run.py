from app import manager
from app.models.tables import User  # importei a tabela Users
from app.models.tables import Lab
from app.models.tables import Disciplina
from app import db

if 0:
    u = Disciplina("CC4612","Estrutura de Dados");
    db.session.add(u)  # sessao=periodo que meu usuario esta logado
    db.session.commit()

if __name__ == "__main__":
    manager.run()
