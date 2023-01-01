from database import*
from mysql.connector import Error
from Observer import *
con = Database().obterInstancia().getDatabaseConnection()

class Produtos(Observer):

    def __init__(self, nome, preco, quantidade, codigo):
        self.nome = nome
        self.codigo = codigo
        self.quantidade = quantidade
        self.preco = preco    

    def inserir_produtos(self):
        dados = self.codigo + ',\'' + self.nome + '\',' + self.preco + ',' + self.quantidade + ')'
        declarar = """INSERT INTO Produtos (Codigo, Nome, Preco, Quantidade) VALUES ("""
        sql = declarar + dados

        try:
            cursor = con.cursor()
            cursor.execute(sql)
            con.commit()
            print(cursor.rowcount,"registros inserido no Banco de Dados!")
            cursor.close()

        except Error as erro:
            print("Falha ao inserir Dados no Banco de Dados: {}".format(erro))

    def imprimir_produtos():
        print("\n====================" * 2)
        print("Imprimindo Produtos")
        cont = 0

        try:
            consulta_sql = "select * from Produtos"
            cursor = con.cursor()
            cursor.execute(consulta_sql)
            linhas = cursor.fetchall()
            print("Número total de produtos cadastrados: ", cursor.rowcount)
            print("====================")
            for linha in linhas:
                print("\033[1;33m{}\033[m. Codigo {} || Nome {} || Valor {} || Quantidade {}".format(cont, linha[0],
                                                                                                     linha[1], linha[2],
                                                                                                     linha[3]))
                cont += 1
        except Error as e:
            print("Erro ao consultar Banco de Dados: ", e)

    def alterar_preco(valor, codigo):
        try:
            altera_preco = """UPDATE Produtos SET Preco = """ + valor + """ WHERE Codigo = """ + codigo
            cursor = con.cursor()
            cursor.execute(altera_preco)
            con.commit()
            print("Preço alterado com sucesso!")
            cursor.close()
        except Error as e:
            print("Erro ao consultar Banco de Dados: ", e)

    def add_quantidade(quantidade, codigo):
        try:
            acul = """SELECT * FROM Produtos WHERE Codigo=""" + codigo
            cursor_acul = con.cursor()
            cursor_acul.execute(acul)
            linha = cursor_acul.fetchall()
            a = 0
            for i in linha:
                a = i[3]

            a = int(a)
            quantidade = quantidade + a
            quantidade = str(quantidade)

            altera_quant = """UPDATE Produtos SET Quantidade = """ + quantidade + """ WHERE Codigo = """ + codigo
            cursor = con.cursor()
            cursor.execute(altera_quant)
            con.commit()
            print("Quantidade alterada com sucesso!")
            cursor.close()

        except Error as e:
            print("Erro ao consultar Banco de Dados: ", e)

    def update( valor, nome):
        quantum = str(valor)
        altera_quant = """UPDATE Produtos SET Quantidade = """ + quantum + """ WHERE Nome = """ + '\'' + nome + '\''
        cursor = con.cursor()
        cursor.execute(altera_quant)
        con.commit()
        cursor.close()

