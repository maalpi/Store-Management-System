from __future__ import annotations
from interface_sql_prox import *

if __name__ == '__main__':
    print("inicio")
    usuario = input("Digite o usuario:")
    senha = input("Digite a senha:")
    admin = proxy()
    admin.interface_proxy(usuario, senha)