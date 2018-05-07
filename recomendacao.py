

def checaLogado(funcao):
    def g():
        if session:
            funcao()
        else:
            print("nao vou chamar")
    return g

@checaLogado
def buscaDisciplinas():
    print("d1")
    print("d2")

#x = checaLogado(buscaDisciplinas)

buscaDisciplinas(True)
