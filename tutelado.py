#!/usr/bin/python3
# -*- coding: utf-8 -*-
#
# tutelado.py:
# Programa python trabajo tutelado BDA 2021-2022.
#
# Autoría:
# María Gandoy López (maria.gandoy@udc.es)
# Alan Xes López Fernández (alan.lfernandez@udc.es)
# Data de creación: 20-05-2021 - _
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

TITLE_DATA_STR = 'nombre_data'
COD_STR = 'cod'
NOM_STR = 'nom'
ERROR_STR = 'error'


## ------------------------------------------------------------
def connect_db():
    try:
        conn = psycopg2.connect(host=DBHOST,
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
    sentenza_create = """
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

    sentenza_drop = """
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

def insert_generico(nombre_data):
    scod = input(f"Codigo de {nombre_data}: ")
    cod = None if scod == "" else int(scod)

    snome = input(f"Nombre de {nombre_data}: ")
    nombre = None if snome == "" else snome.upper()

    return {'sentencia': f"insert into {nombre_data}(cod_{nombre_data},nombre_{nombre_data}) values (%(cod)s,%(nom)s)",
            'valores': {COD_STR: cod, NOM_STR: nombre}}


def error_control_generico(data):
    nombre_data = data[TITLE_DATA_STR]
    cod = data[COD_STR]
    nom = data[NOM_STR]
    error = data[ERROR_STR]
    if error.pgcode == psycopg2.errorcodes.UNDEFINED_TABLE:
        print("La tabla no existe.")
    elif error.pgcode == psycopg2.errorcodes.NOT_NULL_VIOLATION:
        if f"cod_{nombre_data}" in error:
            print(f"El código de {nombre_data} es obligatorio.")
        else:
            print(f"El nombre de {nombre_data} es obligatorio.")
    elif error.pgcode == psycopg2.errorcodes.UNIQUE_VIOLATION:
        if f"cod_{nombre_data}" in error.pgerror:
            print(f"El código de {nombre_data} ({cod}) ya existe")
        else:
            print(f"Una {nombre_data} con el nombre {nom} ya existe")
    else:
        print(f"Erro genérico: {error.pgcode} : {error.pgerror}")


def insert_vacuna(conn):
    formulario = insert_generico('vacuna')

    sentencia_insert = formulario['sentencia']
    valores = formulario['valores']

    with conn.cursor() as cur:
        try:
            cur.execute(sentencia_insert, valores)
            conn.commit()
            print("Vacuna añadida")
        except psycopg2.Error as e:
            error_control_generico({COD_STR: valores[COD_STR], NOM_STR: valores[NOM_STR],
                                    TITLE_DATA_STR: 'vacuna',
                                    ERROR_STR: e})
            conn.rollback()


def insert_estadistica(conn):
    formulario = insert_generico('estadistica')

    sentencia_insert = formulario['sentencia']
    valores = formulario['valores']

    with conn.cursor() as cur:
        try:
            cur.execute(sentencia_insert, valores)
            conn.commit()
            print("Estadistica registrada")
        except psycopg2.Error as e:
            error_control_generico({COD_STR: valores[COD_STR], NOM_STR: valores[NOM_STR],
                                    TITLE_DATA_STR: 'estadistica',
                                    ERROR_STR: e})
            conn.rollback()


def insert_recomendacion(conn):
    scod = input("Codigo de recomendación: ")
    cod = None if scod == "" else int(scod)

    snome = input("Organización: ")
    nombre = None if snome == "" else snome.upper()

    sdesc = input("Descripción de recomendación: ")
    desc = None if sdesc == "" else sdesc

    sentencia_insert = "insert into recomendacion(cod_recomendacion,organizacion,descripcion) values (%(cod)s,%(nom)s,%(desc)s)"
    valores = {'cod': cod, 'nom': nombre, 'desc': desc}

    with conn.cursor() as cur:
        try:
            cur.execute(sentencia_insert, valores)
            conn.commit()
            print("Recomendación registrada")
        except psycopg2.Error as e:
            if e.pgcode == psycopg2.errorcodes.UNDEFINED_TABLE:
                print("La tabla no existe.")
            elif e.pgcode == psycopg2.errorcodes.NOT_NULL_VIOLATION:
                if "cod_vacuna" in e.pgerror:
                    print("El código de recomendación es obligatorio.")
                elif "organizacion" in e.pgerror:
                    print("La organización que propone la recomendación es obligatoria.")
                else:
                    print("La descripción de la recomendación es obligatoria.")
            elif e.pgcode == psycopg2.errorcodes.UNIQUE_VIOLATION:
                if "cod_vacuna" in e.pgerror:
                    print(f"El código de recomendación {cod} ya existe")
            else:
                print(f"Error genérico: {e.pgcode} : {e.pgerror}")
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
    if scod == "":
        cod = None
    elif scod.isdigit():
        cod = int(scod)
        cod_search = True
    else:
        nom = scod.upper()

    sql = "select * from vacuna v" \
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


def show_recomendaciones_vacuna(conn, control_tx=True):
    cod_search = False
    scod = input("Codigo o nombre de vacuna: ")
    if scod == "":
        cod = None
    elif scod.isdigit():
        cod = int(scod)
        cod_search = True
    else:
        nom = scod.upper()

    sql = "select * from vacuna v" \
          " join recomendacion_vacuna rv on v.cod_vacuna=rv.cod_vacuna" \
          " join recomendacion r on r.cod_recomendacion=rv.cod_recomendacion"

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
                    retval = row['cod_vacuna']
                    result_header = False
                cod_rec = row['cod_recomendacion']
                org = row['organizacion']
                fecha = row['fecha_aplicacion']
                desc = row['descripcion']
                print(f"({cod_rec}) Organización {org}; Aplicación {fecha};"
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
    cod = show_row(conn, control_tx=False)

    if cod is None:
        conn.rollback()
        return

    incremento = float(input("Introduce incremento de prezo:"))

    sql = "update artigo set prezoart = prezoart + prezoart * %(incremento)s /100 where codart=%(cod)s"

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

def listar_estadisticas(conn):
    sql = "select * from estadistica"

    with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cur:
        try:
            cur.execute(sql)
            record = cur.fetchall()
            for row in record:
                c_est = row['cod_estadistica']
                n_est = row['nombre_estadistica']
                print(f"({c_est}) Nombre {n_est}")
        except psycopg2.Error as e:
            print(f"Error genérico: {e.pgcode} : {e.pgerror}")

"""
Falta gestión de errores:
    PK duplicadas
    FK inexistentes
    ...
"""
def registrar_estadistica(conn):
    v_cod_search = False
    sv_cod = input("Codigo o nombre de vacuna: ")
    if sv_cod == "":
        v_cod = None
    elif sv_cod.isdigit():
        v_cod = int(sv_cod)
        v_cod_search = True
    else:
        v_nom = sv_cod.upper()

    e_cod_search = False
    se_cod = input("Codigo o nombre de estadística: ")
    if se_cod == "":
        e_cod = None
    elif se_cod.isdigit():
        e_cod = int(se_cod)
        e_cod_search = True
    else:
        e_nom = se_cod.upper()

    se_valor = input("Valor de la estadística (valor numérico): ")
    e_valor = None if se_valor == "" else float(se_valor)

    se_desc = input("Descripción de la estadística ( [ENTER] para dejarlo en blanco): ")
    e_desc = None if se_desc == "" else se_desc

    with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cur:
        try:
            if (not v_cod_search):
                select_vac_cod = "select cod_vacuna from vacuna where nombre_vacuna=(%(v_nom)s)"
                valor_select_vac_cod = {'v_nom': v_nom}
                cur.execute(select_vac_cod, valor_select_vac_cod)
                record = cur.fetchall()
                if len(record) == 0:
                    print(f"No se encontró ninguna vacuna con el nombre \"{v_nom}\"")
                    conn.rollback()
                    return
                else:
                    v_cod = record[0]['cod_vacuna']
            if (not e_cod_search):
                select_est_cod = "select cod_estadistica from estadistica where nombre_estadistica=(%(e_nom)s)"
                valor_select_est_cod = {'e_nom': e_nom}
                cur.execute(select_est_cod, valor_select_est_cod)
                record = cur.fetchall()
                if len(record) == 0:
                    print(f"No se encontró ninguna estadistica con el nombre \"{e_nom}\"")
                    conn.rollback()
                    return
                else:
                    e_cod = record[0]['cod_estadistica']
            sentencia_insert = "insert into estadistica_vacuna(cod_vacuna, cod_estadistica, valor, descripcion)" \
                               " values(%(v_cod)s,%(e_cod)s,%(valor)s,%(desc)s)"
            valores_insert = {'v_cod': v_cod, 'e_cod': e_cod, 'valor': e_valor, 'desc': e_desc}
            cur.execute(sentencia_insert, valores_insert)
            conn.commit()
            print(f"Estadística registrada.")
        except psycopg2.Error as e:
            if e.pgcode == psycopg2.errorcodes.UNIQUE_VIOLATION:
                print(f"FALLO: Ya existe un registro para la estadística ({e_cod}) sobre la vacuna ({v_cod})")
            elif e.pgcode == psycopg2.errorcodes.FOREIGN_KEY_VIOLATION:
                print(f"FALLO: Una de las claves foráneas no coincide con ninguna clave primaria de la tabla referenciada."
                      f"\n\t Código de estadística = cod_estadistica = {e_cod}"
                      f"\n\t Código de vacuna = cod_vacuna = {v_cod}"
                      f"\n{e.diag.message_detail}")
            else:
                print(f"Error genérico: {e.pgcode} : {e.pgerror}")
            conn.rollback()








def listar_recomendaciones(conn):
    sql = "select * from recomendacion"

    with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cur:
        try:
            cur.execute(sql)
            record = cur.fetchall()
            for row in record:
                c_rec = row['cod_recomendacion']
                org = row['organizacion']
                desc = row['descripcion']
                print(f"({c_rec}) Organización {org}"
                      f"\n\t Descripción: {desc}")
        except psycopg2.Error as e:
            print(f"Erro xenérico: {e.pgcode} : {e.pgerror}")

def buscar_recomendaciones(conn):
    cod_search = False
    scod = input("Criterio de búsqueda (código para búsqueda específica, nombre para organización): \n>")
    if scod == "":
        cod = None
    elif scod.isdigit():
        cod_search = True
        cod = int(scod)
    else:
        org = scod.upper()

    if cod_search:
        sql = "select * from recomendacion where cod_recomendacion = (%(cod)s)"
        valor = {'cod': cod}
    else:
        sql = "select * from recomendacion where organizacion = (%(org)s)"
        valor = {'org': org}

    with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cur:
        try:
            cur.execute(sql, valor)
            if cod_search:
                record = cur.fetchall()
                if len(record) == 0:
                    print(f"La recomendación con código {cod} no existe.")
                else:
                    row = record[0]
                    c_rec = cod
                    org = row['organizacion']
                    desc = row['descripcion']
                    print(f"({c_rec}) Organización {org}"
                          f"\n\t Descripción: {desc}");
            else:
                record = cur.fetchall()
                for row in record:
                    c_rec = row['cod_recomendacion']
                    org = row['organizacion']
                    desc = row['descripcion']
                    print(f"({c_rec}) Organización {org}"
                          f"\n\t Descripción: {desc}")
        except psycopg2.Error as e:
            print(f"Erro xenérico: {e.pgcode} : {e.pgerror}")

def ver_recomendaciones(conn):
    MENU_TEXT = """
          -- MENÚ > Ver recomendaciones--
    1 - Listar todas
    2 - Búsqueda
    q - Atrás   
    """
    while True:
        print(MENU_TEXT)
        tecla = input('Opción> ')
        if tecla == 'q':
            break
        elif tecla == '1':
            listar_recomendaciones(conn)
        elif tecla == '2':
            buscar_recomendaciones(conn)
## ------------------------------------------------------------
def menu(conn):
    """
    Imprime un menú de opcións, solicita a opción e executa a función asociada.
    'q' para saír.
    """
    MENU_TEXT = """
      -- MENÚ --
1 - Añadir vacuna           2 - Añadir recomendación       3 - Añadir estadística
4 - Estadísticas de vacuna  5 - Recomendaciones de vacuna
6 - Ver recomendaciones     7 - Listar estadísticas
8 - Registrar estadística de vacuna
q - Saír   
"""
    while True:
        print(MENU_TEXT)
        tecla = input('Opción> ')
        if tecla == 'q':
            break
        elif tecla == '1':
            insert_vacuna(conn)
        elif tecla == '2':
            insert_recomendacion(conn)
        elif tecla == '3':
            insert_estadistica(conn)
        elif tecla == '4':
            show_estadisticas_vacuna(conn, False)
        elif tecla == '5':
            show_recomendaciones_vacuna(conn, False)
        elif tecla == '6':
            ver_recomendaciones(conn)
        elif tecla == '7':
            listar_estadisticas(conn)
        elif tecla == '8':
            registrar_estadistica(conn)


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
