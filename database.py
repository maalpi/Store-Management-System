import mysql.connector
from conexao import *

class Database:
    def __init__(self):
        con = Conexao().obterInstancia().getConnection()
        cursor = con.cursor()
        cursor.execute("CREATE DATABASE IF NOT EXISTS PRODUTOS_SB")
        self.connection = mysql.connector.connect(host="localhost", user="root", database="PRODUTOS_SB", password="Pokemon123.")
        self.cursor = self.connection.cursor()
        self.cursor.execute("CREATE TABLE IF NOT EXISTS Produtos(Codigo int, Nome varchar(50), Preco float, Quantidade int)")
        self.cursor.execute("CREATE TABLE IF NOT EXISTS Caixa (Data_Venda varchar(30), Valor_Venda float, Nome_Produto varchar(50), Quantidade int)")

    def getDatabaseConnection(self):
        return self.connection

    count = 0
    instancia = None

    @staticmethod
    def obterInstancia() :
        Database.count += 1
        if (Database.instancia == None) :
            Database.instancia = Database()
        return Database.instancia