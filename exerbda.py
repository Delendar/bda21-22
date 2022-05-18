#!/usr/bin/python3
# -*- coding: utf-8 -*-
#
# exerbda.py: 
# Programa python para completar seguindo o boletín de exercicios de BDA.
#
# Autor: Miguel Rodríguez Penabad (miguel.penabad@udc.es)
# Data de creación: 19-01-2021
#

import psycopg2
import psycopg2.extras
import psycopg2.errorcodes
import sys
import json


## ------------------------------------------------------------
def connect_db():
    try:
        conn=psycopg2.connect(host="localhost",
                              user="testuser",
                              password="testpass",
                              dbname="testdb")
        conn.autocommit = False
        return conn
    except psycopg2.OperationalError as e:
        print("non se puido conectar: {e}")
    sys.exit(1)


## ------------------------------------------------------------
def disconnect_db(conn):
    conn.commit()
    conn.close()

## ------------------------------------------------------------
def select_table(conn):
    with conn.cursor() as cur:
        cur.execute("select * from artigo")
        row = cur.fetchone()
        while row:
            print(f"Fila número {cur.rownumber} de {cur.rowcount}: {row}")
            row = cur.fetchone()

## ------------------------------------------------------------
def create_table(conn):
    """
    Crea a táboa artigo (codart, nomart, prezoart)
    :param conn: a conexión aberta á bd
    :return: Nada
    """
    sentenza_create= """
      create table artigo(
            codart int constraint pk_artigo primary key,
            nomart varchar(30) not null,
            prezoart numeric (5,2) constraint c_prezopos check (prezoart > 0))
    """
    with conn.cursor() as cur:
        try:
            cur.execute(sentenza_create)
            conn.commit()
            print("Táboa artigo creada")
        except psycopg2.Error as e:
            if e.pgcode == psycopg2.errorcodes.DUPLICATE_TABLE:
                print("A táboa xa existe")
            else:
                print(f"Erro xenérico: {e.pgcode} : {e.pgerror}")
            conn.rollback()

## ------------------------------------------------------------
def drop_table(conn):
    """
    Elimina a táboa artigo (codart, nomart, prezoart)
    :param conn: a conexión aberta á bd
    :return: Nada
    """
    
    sentenza_drop ="""
        drop table artigo
    """
    with conn.cursor() as cur:
        try:
            cur.execute(sentenza_drop)
            conn.commit()
            print("Táboa artigo borrada")
        except psycopg2.Error as e:
            if e.pgcode == psycopg2.errorcodes.UNDEFINED_TABLE:
                print("A táboa non existe")  
            else:
                print(f"Erro xenérico: {e.pgcode} : {e.pgerror}")
            conn.rollback()
## ------------------------------------------------------------
def insert_row(conn):  
    scod = input("Codigo: ")
    cod = None if scod== "" else int(scod)
    
    snome = input("Nome: ")
    nome= None if snome == "" else snome
    
    sprezo = input("Prezo: ")
    prezo = None if sprezo == "" else float(sprezo)
    
    sentenza_insert = "insert into artigo(codart,nomart,prezoart) values (%(cod)s,%(nom)s,%(prezo)s)"
    valores = {'cod': cod, 'nom': nome, 'prezo': prezo}
    
    with conn.cursor() as cur:
        try:
            cur.execute(sentenza_insert, valores)
            conn.commit()
            print("Artigo engadidos")
        except psycopg2.Error as e:
            if e.pgcode == psycopg2.errorcodes.UNDEFINED_TABLE:
                print("A táboa non existe")  
            elif e.pgcode == psycopg2.errorcodes.NOT_NULL_VIOLATION:
                if "codart" in e.pgerror:
                    print("O código é obrigatorio")
                else:
                    print("O nome é obrigatorio")
            elif e.pgcode == psycopg2.errorcodes.CHECK_VIOLATION:
                print("O prezo debe ser positivo")
            elif e.pgcode == psycopg2.errorcodes.UNIQUE_VIOLATION:
                print(f"O codigo de artigo {cod} xa existe")
            else:
                print(f"Erro xenérico: {e.pgcode} : {e.pgerror}")
            conn.rollback()
            
## ------------------------------------------------------------
def show_row(conn, control_tx=True):
    scod = input("Codigo: ")
    cod = None if scod== "" else int(scod)
    
    """    
    with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cur:
        cur.execute(f"select * from artigo where codart={cod}")
        row = cur.fetchone()
        while row:
            print(f"Fila número {cur.rownumber} de {cur.rowcount}: {row}")
            row = cur.fetchone()"""
            
    sql= "select nomart, prezoart from artigo where codart = %s"
            
    retval = None
    with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cur:
        try:
            cur.execute(sql, (cod,))
            row= cur.fetchone()
            if row:
                retval = cod
                prezo = row['prezoart'] if row['prezoart'] else "Descoñecido"
                printf(f"Codigo: {prezo}; Nome: {row['nomart']}; Prezo: {prezo}")
            else:
                print(f"O artigo de código {cod} non existe.")
            if control_tx: conn.comit()
        except psycopg2.Error as e:
            print(f"Erro xenérico: {e.pgcode} : {e.pgerror}")
            if control_tx: conn.rollback()
    return retval
    
    
def update_price(conn):
    
    conn.isolation_level = psycopg2.extensions.ISOLATION_LEVEL_READ_COMMITTED
    cod= show_row(conn, control_tx=False)
    
    if cod is None:
        donn.rollback()
        return
    
    incremento = float (input("Introduce incremento de prezo:"))
    
    sql= "update artigo set prezoart = prezoart + prezoart * %(incremento)s /100 where codart=%(cod)s"
    
    
    with conn.cursor() as cur:
        try:
            cur.execute(sentenza_insert, valores)
            input("Pulsa una tecla")
            conn.commit()
            print("Artigo engadidos")
        except psycopg2.Error as e:
            if e.pgcode == psycopg2.errorcodes.UNDEFINED_TABLE:
                print("A táboa non existe")  
            elif e.pgcode == psycopg2.errorcodes.NOT_NULL_VIOLATION:
                if "codart" in e.pgerror:
                    print("O código é obrigatorio")
                else:
                    print("O nome é obrigatorio")
            elif e.pgcode == psycopg2.errorcodes.CHECK_VIOLATION:
                print("O prezo debe ser positivo")
            elif e.pgcode == psycopg2.errorcodes.UNIQUE_VIOLATION:
                print(f"O codigo de artigo {cod} xa existe")
            else:
                print(f"Erro xenérico: {e.pgcode} : {e.pgerror}")
            conn.rollback()
    
    

    
## ------------------------------------------------------------
def menu(conn):
    """
    Imprime un menú de opcións, solicita a opción e executa a función asociada.
    'q' para saír.
    """
    MENU_TEXT = """
      -- MENÚ --
s - Ver artigo
1 - Crear táboa artigo   
2 - Borrar táboa artigo
3 - Insertar fila
4 - Mostrar artigo
q - Saír   
"""
    while True:
        print(MENU_TEXT)
        tecla = input('Opción> ')
        if tecla == 'q':
            break
        elif tecla == 's':
            select_table(conn)
        elif tecla == '1':
            create_table(conn)
        elif tecla == '2':
            drop_table(conn)
        elif tecla == '3':
            insert_row(conn)
        elif tecla == '4':
            show_row(conn)
        elif tecla == '5':
            update_price(conn)
            
            
## ------------------------------------------------------------
def main():
    """
    Función principal. Conecta á bd e executa o menú.
    Cando sae do menú, desconecta da bd e remata o programa
    """
    print('Conectando a PosgreSQL...')
    conn = connect_db()
    print('Conectado.')
    menu(conn)
    disconnect_db(conn)

## ------------------------------------------------------------

if __name__ == '__main__':
    main()
