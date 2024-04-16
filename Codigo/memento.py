from typing import List

class Dados_Memento:
    def __init__(self):
        self.Ultimo_Dado = None

    def EstadoMemento(self,Dado):
        self.Ultimo_Dado = Dado

    def getMemento(self):
        return self.Ultimo_Dado

class MementoCareTaker:
    def __init__(self):
        self.stack_memento: List[str] = []

    def addMemento(self, dados = Dados_Memento()):
        self.stack_memento.append(dados)

    def getUltimoEstado(self):
        try:
            return self.stack_memento.pop()
        except:
            print("ERROR: Pilha sem elementos")


