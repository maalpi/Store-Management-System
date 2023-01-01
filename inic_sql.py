from __future__ import annotations
from interface_sql_prox import *

if __name__ == '__main__':
    print("Start")
    usuario = input("User:")
    senha = input("Password:")
    admin = proxy()
    admin.interface_proxy(usuario, senha)