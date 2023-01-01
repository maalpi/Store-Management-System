import mysql.connector

class Conexao:
    def __init__(self):
        self.connection = mysql.connector.connect(host="localhost", user="root", password="Pokemon123.")

    def getConnection(self):
        return self.connection

    count = 0
    instancia = None

    @staticmethod
    def obterInstancia() :
        Conexao.count += 1
        if (Conexao.instancia == None) :
            Conexao.instancia = Conexao()
        return Conexao.instancia