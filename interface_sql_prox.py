from __future__ import annotations
from datetime import datetime
from caixa_sql import *
from produtos_sql import *
from memento import *
from Adapter import *
import random
memento = MementoCareTaker()


class Interface:
    count = 0
    instancia = None

    @staticmethod
    def obterInstancia() :
        Interface.count += 1
        if (Interface.instancia == None) :
            Interface.instancia = Interface()
        return Interface.instancia

    def cadastrar_produtos(self):
        print("\n====================" * 2)
        nome = input("Digite o nome do produto:")
        valor = input("Digite o valor do produto:")
        quantidade = input("Digite a quantidade deste produto:")

        codigo = str(random.randint(1, 777))
        print("O código do produto será:", codigo)

        produto = Produtos(nome, valor, quantidade, codigo)
        produto.inserir_produtos()

    def Vender_Produtos(self):
        print("\n====================" * 2)
        caixa = Caixa.obterInstancia()
        print("Digite o código do produto:")
        codigo = input()

        acul = """SELECT * FROM Produtos WHERE Codigo=""" + codigo
        cursor_acul = con.cursor()
        cursor_acul.execute(acul)
        linha = cursor_acul.fetchall()


        for i in linha:
            print("Codigo {} || Nome {} || Valor {} || Quantidade {}".format(i[0],i[1],i[2],i[3]))
            print("\n Quantos produtos você vai retirar?")
            quantidade = int(input())
            caixa.addDados(str(datetime.today().strftime("%d/%m/%Y %H:%M:%S")), i[2], i[1],quantidade)

    def retirar_produtos(self):
        print("\n====================" * 2)
        codigo_tira = input("Digite o codigo do produto a ser apagado:")

        info = """SELECT * FROM Produtos WHERE Codigo=""" + '\'' + codigo_tira + '\''
        cursor_info = con.cursor()
        cursor_info.execute(info)
        linha = cursor_info.fetchall()

        x = Dados_Memento()
        x.EstadoMemento(linha)
        memento.addMemento(x)
        try:
            remove_sql = "DELETE FROM Produtos WHERE Codigo=" + codigo_tira
            cursor = con.cursor()
            cursor.execute(remove_sql)
            con.commit()

        except Error as erro:
            print("Erro ao remover produto: ", erro)

    def RestaurarUltimo(self):
        variavel = memento.getUltimoEstado()
        try:
            variavel = variavel.getMemento()
            declarar = """INSERT INTO Produtos (Codigo,Nome,Preco,Quantidade) VALUES """ + str(variavel[0])
            cursor_recuperar = con.cursor()
            cursor_recuperar.execute(declarar)
            con.commit()
            cursor_recuperar.close()
        except:
            print("ERRO, Não existe ultimo elemento apagado! ")

    def Salvar(self):
     opc = int(input("Choose 1 to save in CSV or 2 to save in EXCEL(xlsx):"))

     if (opc == 1):
         Salvar.Salvar_CSV()

     elif (opc == 2):
         Salvar.Salvar_excel()


    def carregar(self):
        Ler_dados()

    def atualiza(self):
        print("\n====================" * 2)
        codigo_att = input("Digite o codigo do produto a ser alterado:")
        valor = 0.0; quantidade = 0; escolha = 0

        while True:
            print("Escolha sua ação: \n 1-Alterar Apenas o valor \n 2-Adicionar mais estoque \n 3-Adicionar e Alterar Valor do produto")
            escolha = int(input())
            if escolha == 1:
                valor = input("Digite o novo valor do Produto:")
                Produtos.alterar_preco(valor,codigo_att)
                break

            elif escolha == 2:
                quantidade = int(input("Digite quantos produtos é para ser adicionado ao estoque:"))
                Produtos.add_quantidade(quantidade,codigo_att)
                break

            elif escolha == 3:
                valor = input("Digite o novo valor do Produto:")
                quantidade = int(input("Digite quantos produtos é para ser adicionado ao estoque:"))
                Produtos.alterar_preco(valor, codigo_att)
                Produtos.add_quantidade(quantidade, codigo_att)
                break
            else:
                print("\033[1;31mERROR: OPÇÃO DIGITADA ERRADA\033[m")

class proxy(Interface):
    def interface_proxy(self,user,password):
        self.usuario = user
        self.senha = password

        if self.temPermissao():
            caixa = Caixa.obterInstancia()
            gerenciador = self.obterInstancia()
            while True:
                print("\n====================")
                print("Choose your action: \n 1-Register Products \n 2-Show Products \n 3-Remove Products \n 4-Update Products \n 5-Sell Products \n 6-Print Sells \n 7-Recover Delete Product \n 8-Save \n 9-Load \n 0-End Program")
                escolha = int(input())

                if escolha == 1:
                    self.cadastrar_produtos()

                elif escolha == 2:
                    Produtos.imprimir_produtos()

                elif escolha == 3:
                    self.retirar_produtos()

                elif escolha == 4:
                    self.atualiza()

                elif escolha == 5:
                    self.Vender_Produtos()

                elif escolha == 6:
                    caixa.imprimirCaixa()

                elif escolha == 7:
                    self.RestaurarUltimo()

                elif escolha == 8:
                    self.Salvar()

                elif escolha == 9:
                    self.carregar()

                elif escolha == 0:
                    break

                else:
                    print("\033[1;31mERROR: OPÇÃO DIGITADA ERRADA\033[m")

    def temPermissao(self):
        if(self.usuario == 'user' and self.senha =='password'):
            return 1
        else:
            print("usuario sem permissão de entrada")
            return 0

