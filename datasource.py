# Arquivo com a classe que obtém e repassa dados lidos para as demais

class DataSource:
    def __init__(self):
        pass

    # Método só para testar como seriam os dados
    # se fossem lidos de um arquivo local.
    def dadosTeste():
        arq = open("dadosTeste.txt", 'r')
        dados = arq.read().splitlines()
        arq.close()
        return dados