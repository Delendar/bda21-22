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

DBHOST = "localhost"
DBUSER = "testuser"
DBUSERPASS = "testpass"
DBNAME = "testdb"

## ------------------------------------------------------------
def connect_db():
    try:
        conn=psycopg2.connect(host=DBHOST,
                              user=DBUSER,
                              password=DBUSERPASS,
                              dbname=DBNAME)
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
def insert_vacuna(conn):
    scod = input("Codigo de vacuna: ")
    cod = None if scod== "" else int(scod)
    
    snome = input("Nombre de vacuna: ")
    nombre= None if snome == "" else snome.upper()
    
    sentencia_insert = "insert into vacuna(cod_vacuna,nombre_vacuna) values (%(cod)s,%(nom)s)"
    valores = {'cod': cod, 'nom': nombre}
    
    with conn.cursor() as cur:
        try:
            cur.execute(sentencia_insert, valores)
            conn.commit()
            print("Vacuna añadida")
        except psycopg2.Error as e:
            if e.pgcode == psycopg2.errorcodes.UNDEFINED_TABLE:
                print("La tabla no existe.")
            elif e.pgcode == psycopg2.errorcodes.NOT_NULL_VIOLATION:
                if "cod_vacuna" in e.pgerror:
                    print("El código de vacuna es obligatorio.")
                else:
                    print("El nombre de vacuna es obligatorio.")
            #elif e.pgcode == psycopg2.errorcodes.CHECK_VIOLATION:
            #    print("O prezo debe ser positivo")
            elif e.pgcode == psycopg2.errorcodes.UNIQUE_VIOLATION:
                if "cod_vacuna" in e.pgerror:
                    print(f"El código de vacuna {cod} ya existe")
                else:
                    print(f"Una vacuna con el nombre {nombre} ya existe")
            else:
                print(f"Erro xenérico: {e.pgcode} : {e.pgerror}")
            conn.rollback()
            
## ------------------------------------------------------------
"""    
    -with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cur:
        cur.execute(f"select * from artigo where codart={cod}")
        row = cur.fetchone()
        while row:
            print(f"Fila número {cur.rownumber} de {cur.rowcount}: {row}")
            row = cur.fetchone()
    """

def show_estadisticas_vacuna(conn, control_tx=True):
    cod_search = False
    scod = input("Codigo o nombre de vacuna: ")
    if scod=="":
        cod = None
    elif scod.isdigit():
        cod = int(scod)
        cod_search = True
    else:
        nom = scod.upper()

    sql= "select * from vacuna v" \
         " join estadistica_vacuna ev on v.cod_vacuna=ev.cod_vacuna" \
         " join estadistica e on ev.cod_estadistica=e.cod_estadistica"

    if cod_search:
        sql += " where v.cod_vacuna = (%(cod)s)"
        valor = {'cod': cod}
    else:
        sql += " where v.nombre_vacuna = (%(nom)s)"
        valor = {'nom': nom}

    retval = None
    with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cur:
        try:
            cur.execute(sql, valor)
            records = cur.fetchall()
            if cod_search:
                print(f"Mostrando información para la vacuna con código ({cod}):")
            else:
                print(f"Mostrando información para la vacuna de nombre \"{nom}\":")
            result_header = True
            for row in records:
                if result_header:
                    print(f"-- {row['nombre_vacuna']} ({row['cod_vacuna']}) --")
                    result_header = False
                retval = row['cod_vacuna']
                c_est = row['cod_estadistica']
                n_est = row['nombre_estadistica']
                valor = row['valor']
                desc = row['descripcion'] if row['descripcion'] else "N/A"
                print(f"Cod ({c_est}); {n_est} {valor};"
                      f"\n\tDescripción: {desc}")
            if control_tx: conn.comit()
        except psycopg2.Error as e:
            print(f"Error genérico: {e.pgcode} : {e.pgerror}")
            if control_tx: conn.rollback()
    return retval


def show_row(conn, control_tx=True):
    scod = input("Codigo: ")
    cod = None if scod == "" else int(scod)

    """    
    with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cur:
        cur.execute(f"select * from artigo where codart={cod}")
        row = cur.fetchone()
        while row:
            print(f"Fila número {cur.rownumber} de {cur.rowcount}: {row}")
            row = cur.fetchone()
    """

    sql = "select nomart, prezoart from artigo where codart = %s"

    retval = None
    with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cur:
        try:
            cur.execute(sql, (cod,))
            row = cur.fetchone()
            if row:
                retval = cod
                prezo = row['prezoart'] if row['prezoart'] else "Descoñecido"
                print(f"Codigo: {prezo}; Nome: {row['nomart']}; Prezo: {prezo}")
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
        conn.rollback()
        return
    
    incremento = float (input("Introduce incremento de prezo:"))
    
    sql= "update artigo set prezoart = prezoart + prezoart * %(incremento)s /100 where codart=%(cod)s"
    
    
    with conn.cursor() as cur:
        try:
            cur.execute(sql, (cod,))
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
1 - Añadir vacuna
2 - Estadísticas de vacuna
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
            insert_vacuna(conn)
        elif tecla == '2':
            show_estadisticas_vacuna(conn, False)
            
            
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
