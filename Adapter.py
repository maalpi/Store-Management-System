from database import *
import pandas as pd
con = Database().obterInstancia().getDatabaseConnection()
import pathlib

class Salvar:
    def Salvar_CSV():
        query_meta1 = "SELECT * FROM Produtos"
        cur = con.cursor()
        cur.execute(query_meta1)
        result = cur.fetchall()
        df = pd.DataFrame(result)
        df.to_csv("test_produto.csv",index=False)

        query_meta1_2 = "SELECT * FROM Caixa"
        cur2 = con.cursor()
        cur2.execute(query_meta1_2)
        result = cur2.fetchall()
        df = pd.DataFrame(result)
        df.to_csv("test_caixa.csv",index=False)

        print("Produtos e caixa salvos com sucesso em arquivos .CSV !!")

    def Salvar_excel():
        query_meta1 = "SELECT * FROM Produtos"
        cur = con.cursor()
        cur.execute(query_meta1)
        result = cur.fetchall()
        df = pd.DataFrame(result)
        df.to_excel("Produtos_EXCEL.xlsx", index=False)

        query_meta1_2 = "SELECT * FROM Caixa"
        cur2 = con.cursor()
        cur2.execute(query_meta1_2)
        result = cur2.fetchall()
        df = pd.DataFrame(result)
        df.to_excel("Caixa_EXCEL.xlsx", index=False)

class Ler_dados:
    def __init__(self):
        try:
            print("Enter the path of the file where the Products are:")
            caminho_produto = str(input())

            print("Enter the path of the file where the Cash Register are:")
            caminho_caixa = str(input())
            Adapter.Request_ad(self,caminho_produto,caminho_caixa)

        except:
            print("File not found.")

    def Request(self,caminho_produto,caminho_caixa):
        df_caixa = pd.read_csv(caminho_caixa)
        df_produto = pd.read_csv(caminho_produto)
        cur = con.cursor()

        for index, row in df_produto.iterrows():
            dados = str(row[0]) + ',\'' + str(row[1]) + '\',' + str(row[2]) + ',' + str(row[3]) + ')'
            declarar = """INSERT INTO Produtos (Codigo,Nome,Preco,Quantidade) VALUES ("""
            sql = declarar + dados
            cur.execute(sql)
            con.commit()

        for index, row in df_caixa.iterrows():
            dados = "'" + str(row[0]) + "'" + ',' + str(row[1]) + ',\'' + str(row[2]) + '\',' + str(row[3]) + ')'
            declarar = """INSERT INTO Caixa (Data_Venda, Valor_Venda, Nome_Produto, Quantidade) VALUES ("""
            sql = declarar + dados
            cur.execute(sql)
            con.commit()

        self.remover_repeticao()

    def remover_repeticao(self):
        parte1 = "CREATE TABLE source_copy LIKE Produtos;"
        parte2 = "INSERT INTO source_copy select * from Produtos group by Codigo;"
        parte3 = "Drop table Produtos;"
        parte4 = "Alter Table source_copy rename to Produtos;"
        cursor_duplicada_produto = con.cursor()
        cursor_duplicada_produto.execute(parte1)
        con.commit()
        cursor_duplicada_produto.execute(parte2)
        con.commit()
        cursor_duplicada_produto.execute(parte3)
        con.commit()
        cursor_duplicada_produto.execute(parte4)
        con.commit()

        parte1 = "CREATE TABLE source_copy LIKE Caixa;"
        parte2 = "INSERT INTO source_copy select * from Caixa group by Nome_Produto;"
        parte3 = "Drop table Caixa;"
        parte4 = "Alter Table source_copy rename to Caixa;"
        cursor_duplicada_caixa = con.cursor()
        cursor_duplicada_caixa.execute(parte1)
        con.commit()
        cursor_duplicada_caixa.execute(parte2)
        con.commit()
        cursor_duplicada_caixa.execute(parte3)
        con.commit()
        cursor_duplicada_caixa.execute(parte4)
        con.commit()

        cursor_duplicada_produto.close()
        cursor_duplicada_caixa.close()

class Adapter(Ler_dados):
    def Request_ad(self,caminho_produto,caminho_caixa):
        file_extension = pathlib.Path(caminho_produto).suffix
        file_extension_caixa = pathlib.Path(caminho_caixa).suffix
        if file_extension == '.csv' and file_extension_caixa == '.csv':
            self.Request(caminho_produto,caminho_caixa)

        else:
            if file_extension != '.csv':
                Adaptee.Adaptar_produto(caminho_produto)

            if file_extension_caixa != '.csv':
                Adaptee.adaptar_caixa(caminho_caixa)


        self.remover_repeticao()

class Adaptee:
    def Adaptar_produto(caminho):
        read_file = pd.read_excel(caminho)
        read_file.to_csv("ProdutoXLSX_Convertido.csv",index = None)
        conversao = "ProdutoXLSX_Convertido.csv"
        df_produto = pd.read_csv(conversao)
        cur = con.cursor()

        for index, row in df_produto.iterrows():
            dados = str(row[0]) + ',\'' + str(row[1]) + '\',' + str(row[2]) + ',' + str(row[3]) + ')'
            declarar = """INSERT INTO Produtos (Codigo,Nome,Preco,Quantidade) VALUES ("""
            sql = declarar + dados
            cur.execute(sql)
            con.commit()

    def adaptar_caixa(caminho2):
        read_file = pd.read_excel(caminho2)
        read_file.to_csv("Caixa_XLSX_Convertido.csv", index=None)
        conversao = "Caixa_XLSX_Convertido.csv"
        df_caixa = pd.read_csv(conversao)
        cur = con.cursor()
        for index, row in df_caixa.iterrows():
            dados = "'" + str(row[0]) + "'" + ',' + str(row[1]) + ',\'' + str(row[2]) + '\',' + str(row[3]) + ')'
            declarar = """INSERT INTO Caixa (Data_Venda, Valor_Venda, Nome_Produto, Quantidade) VALUES ("""
            sql = declarar + dados
            cur.execute(sql)
            con.commit()




