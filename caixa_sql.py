from Observer import Observer
from typing import Type
from produtos_sql import Produtos
from mysql.connector import Error
from database import*
con = Database().obterInstancia().getDatabaseConnection()

class Caixa:
    count = 0
    instancia = None

    @staticmethod
    def obterInstancia() :
        Caixa.count += 1
        if (Caixa.instancia == None) :
            Caixa.instancia = Caixa()
        return Caixa.instancia

    def Notify(self, quantum, nome):
        produto : Type[Observer]
        produto = Produtos
        produto.update(quantum,nome)

    def addDados(self, data, valor, nome, quantidade):
        valor = valor * quantidade
        data = str(data); valor = str(valor); quantidade = str(quantidade)
        aspa = "'"
        dados = aspa + data + aspa +',' + valor + ',\'' + nome + '\',' + quantidade + ')'
        print(data)
        declarar = """INSERT INTO Caixa (Data_Venda, Valor_Venda, Nome_Produto, Quantidade) VALUES ("""

        sql = declarar + dados

        try:
            ####PEGANDO INFO DA QUANTIDADE
            info = """SELECT * FROM Produtos WHERE Nome=""" + '\'' + nome + '\''

            cursor_info = con.cursor()
            cursor_info.execute(info)
            linha = cursor_info.fetchall()

            for i in linha:
                self.Notify(int(i[3])-int(quantidade),nome)

            cursor = con.cursor()
            cursor.execute(sql)
            con.commit()
            print(cursor.rowcount,"Venda inserida no Banco de Dados!")
            cursor.close()

        except Error as erro:
            print("Falha ao inserir Dados no Banco de Dados: {}".format(erro))

    def imprimirCaixa(self):
        print("\n====================" * 2)
        try:
            consulta_sql = "select * from Caixa"
            cursor = con.cursor()
            cursor.execute(consulta_sql)
            linhas = cursor.fetchall()
            print("Número total de vendas cadastrados: ", cursor.rowcount)
            print("====================")
            for linha in linhas:
                print(f"Data {linha[0]} || Nome {linha[2]}" + " "*(30-len(linha[2])) +f"|| Quantidade {linha[3]} || Valor {linha[1]} ")

        except Error as e:
            print("Erro ao consultar Banco de Dados: ", e)
