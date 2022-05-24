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
import datetime
from datetime import datetime

DBHOST = "localhost"
DBUSER = "testuser"
DBUSERPASS = "testpass"
DBNAME = "testdb"


# ------------------------------------------------------------


def connect_db():
    try:
        conn = psycopg2.connect(host=DBHOST,
                                user=DBUSER,
                                password=DBUSERPASS,
                                dbname=DBNAME)
        conn.autocommit = False
        return conn
    except psycopg2.OperationalError as e:
        print(f"non se puido conectar: {e}")
    sys.exit(1)


# ------------------------------------------------------------
def disconnect_db(conn):
    conn.commit()
    conn.close()


# ------------------------------------------------------------


def get_cod_vacuna(cur, nombre_vacuna):
    """
    Dado el nombre de una vacuna, recupera de base de datos el código correspondiente a esta.

    Parameters
    ----------
    cur:
        Cursor con conexión a la base de datos donde se realiza la petición.
    nombre_vacuna: str
        Nombre de la vacuna por el que se va a realizar la búsqueda.

    Returns
    -------
    cod_vacuna
        Código (int) correspondiente a la fila encontrada por el nombre de vacuna.
    """
    select_vac_cod = "select cod_vacuna from vacuna where nombre_vacuna=(%(v_nom)s)"
    valor_select_vac_cod = {'v_nom': nombre_vacuna}
    cur.execute(select_vac_cod, valor_select_vac_cod)
    record = cur.fetchall()
    if len(record) == 0:
        return None
    else:
        return record[0]['cod_vacuna']


def get_cod_estadistica(cur, nombre_estadistica):
    """
    Dado el nombre de una estadística, recupera de base de datos el código correspondiente a esta.

    Parameters
    ----------
    cur:
        Cursor con conexión a la base de datos donde se realiza la petición.
    nombre_estadistica: str
        Nombre de la estadística por el que se va a realizar la búsqueda.

    Returns
    -------
    cod_estadistica
        Código (int) correspondiente a la fila encontrada por el nombre de estadística.
    """
    select_est_cod = "select cod_estadistica from estadistica where nombre_estadistica=(%(e_nom)s)"
    valor_select_est_cod = {'e_nom': nombre_estadistica}
    cur.execute(select_est_cod, valor_select_est_cod)
    record = cur.fetchall()
    if len(record) == 0:
        return None
    else:
        return record[0]['cod_estadistica']


def insert_vacuna(cur, v_cod, v_nom):
    """
    Ejecuta la sentencia de inserción de una vacuna en la tabla VACUNA.

    Parameters
    ----------
    cur:
        Cursor con conexión a la base de datos donde se realiza la inserción.
    v_cod: int
        Código de la vacuna a insertar.
    v_nom: int
        Nombre de la vacuna a insertar.
    """
    sentencia_insert = "insert into vacuna(cod_vacuna, nombre_vacuna)" \
                       " values(%(v_cod)s,%(v_nom)s)"
    valores_insert = {'v_cod': v_cod, 'v_nom': v_nom}
    cur.execute(sentencia_insert, valores_insert)


def insert_estadistica(cur, e_cod, e_nom):
    """
    Ejecuta la sentencia de inserción de una vacuna en la tabla ESTADISTICA.

    Parameters
    ----------
    cur:
        Cursor con conexión a la base de datos donde se realiza la inserción.
    e_cod: int
        Código de la estadística a insertar.
    e_nom: str
        Nombre de la estadística a insertar.
    """
    sentencia_insert = "insert into estadistica(cod_estadistica, nombre_estadistica)" \
                       " values(%(e_cod)s,%(e_nom)s)"
    valores_insert = {'e_cod': e_cod, 'e_nom': e_nom}
    cur.execute(sentencia_insert, valores_insert)


def insert_recomendacion(cur, r_cod, r_org, r_desc):
    """
    Ejecuta la sentencia de inserción de una recomendación en la tabla RECOMENDACION.

    Parameters
    ----------
    cur:
        Cursor con conexión a la base de datos donde se realiza la inserción.
    r_cod: int
        Código de la recomendación a insertar.
    r_org: str
        Nombre de la organización que propone la recomendación a insertar.
    r_desc: str
        Descripción de la recomendación a insertar.
    """
    sentencia_insert = "insert into recomendacion(cod_recomendacion, organizacion, descripcion)" \
                       " values(%(r_cod)s,%(r_org)s,%(r_desc)s)"
    valores_insert = {'r_cod': r_cod, 'r_org': r_org, 'r_desc': r_desc}
    cur.execute(sentencia_insert, valores_insert)


def insert_estadistica_vacuna(cur, v_cod, e_cod, e_valor, e_desc):
    """
    Ejecuta la sentencia de inserción de una estadística sobre una vacuna en la tabla ESTADISTICA_VACUNA.

    Parameters
    ----------
    cur:
        Cursor con conexión a la base de datos donde se realiza la inserción.
    v_cod: int
        Código de la vacuna sobre la que se guarda la estadística a insertar.
    e_cod: int
        Código de la estadística a insertar.
    e_valor: float
        Valor de la estadística a insertar.
    e_desc: str
        Breve descripción de la estadística a insertar.
    """
    sentencia_insert = "insert into estadistica_vacuna(cod_vacuna, cod_estadistica, valor, descripcion)" \
                       " values(%(v_cod)s,%(e_cod)s,%(valor)s,%(desc)s)"
    valores_insert = {'v_cod': v_cod, 'e_cod': e_cod, 'valor': e_valor, 'desc': e_desc}
    cur.execute(sentencia_insert, valores_insert)


def insert_recomendacion_vacuna(cur, v_cod, r_cod, rv_fecha):
    """
    Ejecuta la sentencia de inserción de una recomendación sobre una vacuna en la tabla RECOMENDACION_VACUNA.

    Parameters
    ----------
    cur:
        Cursor con conexión a la base de datos donde se realiza la inserción.
    v_cod: int
        Código de la vacuna sobre la que se propone la recomendación a insertar.
    r_cod: int
        Código de la recomendación a insertar.
    rv_fecha: str
        Fecha en la que se aplica la recomendación sobre la vacuna.
    """
    sentencia_insert = "insert into recomendacion_vacuna(cod_vacuna, cod_recomendacion, fecha_aplicacion)" \
                       " values(%(r_cod)s,%(v_cod)s,to_date(%(rv_fecha)s,'DD/MM/YY'))"
    valores_insert = {'r_cod': r_cod, 'v_cod': v_cod, 'rv_fecha': rv_fecha}
    cur.execute(sentencia_insert, valores_insert)


def form_generico(nombre_data):
    """
    Función que abstrae la adquisición de códigos identificadores y nombres sobre un dato pasado por parámetro.

    Parameters
    ----------
    nombre_data: str
        Nombre que se desea mostrar al usuario como información de lo que se le pide.

    Returns
    -------
    data:
        Diccionario de datos que cuenta con los parámetros:
        <código> Asignado a la clave "cod" y
        <nombre> Asignado a la clave "nom"
    """
    scod = input(f"Codigo de {nombre_data}: ")
    cod = None if scod == "" else int(scod)

    snome = input(f"Nombre de {nombre_data}: ")
    nombre = None if snome == "" else snome.upper()

    return {'cod': cod,
            'nom': nombre}


def error_control_generico(nombre_data, cod, nom, error):
    """
    Formatea información genérica sobre un error dado sobre un elemento.

    Parameters
    ----------
    nombre_data:
        El nombre del objeto que se desea mostrar al usuario.
    cod:
        El atributo identificador (clave primaria) del objeto.
    nom:
        El atributo de nombre del objeto.
    error:
        El error a formatear.
    """
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


def agregar_vacuna(conn):
    """
    Intenta insertar en la base de datos una nueva fila sobre la tabla VACUNA con los datos
    otorgados por el usuario.

    Parameters
    ----------
    conn:
        La conexión a la base de datos.
    """
    inputs = form_generico('vacuna')
    v_cod = inputs['cod']
    v_nom = inputs['nom']

    with conn.cursor() as cur:
        try:
            insert_vacuna(cur, v_cod, v_nom)
            conn.commit()
            print("Vacuna añadida")
            menu_vacuna(conn, v_cod)
        except psycopg2.Error as e:
            error_control_generico('vacuna', v_cod, v_nom, e)
            conn.rollback()


def agregar_estadistica(conn):
    """
    Intenta insertar en la base de datos una nueva fila sobre la tabla ESTADISTICA con los datos
    otorgados por el usuario.

    Parameters
    ----------
    conn:
        La conexión a la base de datos.
    """
    inputs = form_generico('estadistica')
    e_cod = inputs['cod']
    e_nom = inputs['nom']

    with conn.cursor() as cur:
        try:
            insert_estadistica(cur, e_cod, e_nom)
            conn.commit()
            print("Estadistica registrada")
        except psycopg2.Error as e:
            error_control_generico('estadistica', e_cod, e_nom, e)
            conn.rollback()


def form_agregar_recomendacion():
    """
    Obtiene del usuario la información necesaria para poder realizar la inserción de una nueva fila en la entidad
    RECOMENDACION.

    Returns
    -------
    data:
        Diccionario de datos con los siguientes elementos:
        <código> con clave 'cod_r',
        <organización> con clave 'org',
        <descripción> con clave 'desc'
    """
    scod = input("Codigo de recomendación: ")
    cod_r = None if scod == "" else int(scod)

    sorg = input("Organización: ")
    org = None if sorg == "" else sorg.upper()

    sdesc = input("Descripción de recomendación: ")
    desc = None if sdesc == "" else sdesc
    return {'cod': cod_r, 'nom': org, 'desc': desc}


def agregar_recomendacion(conn):
    """
    Trata de agregar una nueva fila a la entidad RECOMENDACION con datos otorgados por el usuario.

    Parameters
    ----------
    conn:
        La conexión con la base de datos.
    """
    inputs = form_agregar_recomendacion()
    r_cod = inputs['cod']
    r_nom = inputs['nom']
    r_desc = inputs['desc']

    with conn.cursor() as cur:
        try:
            insert_recomendacion(cur, r_cod, r_nom, r_desc)
            conn.commit()
            return r_cod
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
                    print(f"El código de recomendación {r_cod} ya existe")
            else:
                print(f"Error genérico: {e.pgcode} : {e.pgerror}")
            conn.rollback()


def form_registrar_recomendacion_vacuna():
    """
    Obtiene del usuario la información necesaria para poder realizar la inserción de una nueva fila en la entidad
    RECOMENDACION_VACUNA.

    Returns
    -------
    data:
        Diccionario de datos con los siguientes elementos:
        <código de la recomendación> con clave 'cod_r',
        <código de la vacuna> con clave 'cod_v',
        <fecha de aplicación de la recomendación> con clave 'fecha'
    """
    scodr = input("Codigo de recomendación: ")
    cod_r = None if scodr == "" else int(scodr)

    scodv = input("Código de la vacuna: ")
    cod_v = None if scodv == "" else int(scodv)

    sfecha = input("Fecha de aplicación de la recomendación(dd/mm/yy): ")
    fecha = None if sfecha == "" else sfecha
    return {'rec': cod_r, 'vac': cod_v, 'fecha': fecha}


def registrar_recomendacion_vacuna(conn):
    """
    Trata de agregar una nueva fila a la entidad RECOMENDACION_VACUNA con datos otorgados por el usuario.

    Parameters
    ----------
    conn:
        La conexión con la base de datos.
    """
    inputs = form_registrar_recomendacion_vacuna()
    r_cod = inputs['rec']
    v_cod = inputs['vac']
    r_date = inputs['fecha']

    with conn.cursor() as cur:
        try:
            insert_recomendacion_vacuna(cur, r_cod, v_cod, r_date)
            conn.commit()
            print("Recomendación para la vacuna registrada")
        except psycopg2.Error as e:
            if e.pgcode == psycopg2.errorcodes.UNDEFINED_TABLE:
                print("La tabla no existe.")
            elif e.pgcode == psycopg2.errorcodes.NOT_NULL_VIOLATION:
                if "cod_vacuna" in e.pgerror:
                    print("El código de recomendación es obligatorio.")
                elif "organizacion" in e.pgerror:
                    print("La fecha de la recomendación es obligatoria.")
                else:
                    print("El código de vacuna para la recomendación es obligatorio.")
            else:
                print(f"Error genérico: {e.pgcode} : {e.pgerror}")
            conn.rollback()


# ------------------------------------------------------------
"""    
    -with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cur:
        cur.execute(f"select * from artigo where codart={cod}")
        row = cur.fetchone()
        while row:
            print(f"Fila número {cur.rownumber} de {cur.rowcount}: {row}")
            row = cur.fetchone()
    """


def buscar_estadisticas_vacuna(conn, control_tx=True):
    """
    Realiza una búsqueda en la base de datos sobre la tabla ESTADISTICA_VACUNA en base a un código o nombre de una vacuna
    otorgado por el usuario.

    Parameters
    ----------
    conn:
        La conexión con la base de datos.
    control_tx:
        Variable de control transaccional, predeterminado TRUE.
        Si TRUE entonces se realiza control transaccional,
        Si FALSE no se realiza.
    """
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
            if control_tx:
                conn.comit()
        except psycopg2.Error as e:
            print(f"Error genérico: {e.pgcode} : {e.pgerror}")
            if control_tx:
                conn.rollback()
    return retval


def buscar_recomendaciones_vacuna(conn, control_tx=True):
    """
    Realiza una búsqueda en la base de datos sobre la tabla RECOMENDACIONES_VACUNA en base a un código o nombre de una vacuna
    otorgado por el usuario.

    Parameters
    ----------
    conn:
        La conexión con la base de datos.
    control_tx:
        Variable de control transaccional, predeterminado TRUE.
        Si TRUE entonces se realiza control transaccional,
        Si FALSE no se realiza.
    """
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
            if control_tx:
                conn.comit()
        except psycopg2.Error as e:
            print(f"Error genérico: {e.pgcode} : {e.pgerror}")
            if control_tx:
                conn.rollback()
    return retval


def listar_estadisticas(conn):
    """
    Realiza una búsqueda en la base de datos sobre la tabla ESTADISTICAS y lista todas las filas encontradas.

    Parameters
    ----------
    conn:
        La conexión con la base de datos.
    """
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


# Registrar Estadísticas
def form_registrar_estadistica_vacuna():
    """
    Obtiene del usuario la información necesaria para poder realizar la inserción de una nueva fila en la entidad
    ESTADISTICA_VACUNA.

    Returns
    -------
    data:
        Diccionario de datos con los siguientes elementos:
        <criterio de igualdad de la vacuna> con clave 'v_criteria',
        <criterio de igualdad de la estadística> con clave 'e_criteria',
        <valor de la estadística> con clave 'e_valor',
        <descripicón de la estadística> con clave 'e_desc'
    """
    sv_cod = input("Codigo o nombre de vacuna: ")
    if sv_cod == "":
        v_criteria = None
    elif sv_cod.isdigit():
        v_criteria = int(sv_cod)
    else:
        v_criteria = sv_cod.upper()

    se_cod = input("Codigo o nombre de estadística: ")
    if se_cod == "":
        e_criteria = None
    elif se_cod.isdigit():
        e_criteria = int(se_cod)
    else:
        e_criteria = se_cod.upper()

    se_valor = input("Valor de la estadística (valor numérico): ")
    e_valor = None if se_valor == "" else float(se_valor)

    se_desc = input("Descripción de la estadística ( [ENTER] para dejarlo en blanco): ")
    e_desc = None if se_desc == "" else se_desc
    return {'v_criteria': v_criteria,
            'e_criteria': e_criteria,
            'e_valor': e_valor, 'e_desc': e_desc}


def registrar_estadistica_vacuna_control_errores(e, v_cod, e_cod):
    """
    Formatea los errores que se hayan podido dar en la realización de la transacción de inserción de una estadística
    sobre una vacuna.

    Parameters
    ----------
    e:
        El error.
    v_cod:
        El valor del atributo "cod_vacuna" (código de vacuna) a registrar.
    e_cod:
        El valor del atributo "cod_estadistica" (código de estadistica) a registrar.
    """
    if e.pgcode == psycopg2.errorcodes.UNIQUE_VIOLATION:
        print(f"\nFALLO: Violación de clave primaria."
              f"\nYa existe un registro para la estadística ({e_cod}) sobre la vacuna ({v_cod})")
    elif e.pgcode == psycopg2.errorcodes.NOT_NULL_VIOLATION:
        print(f"\nFALLO: Los siguientes valores son obligatorios:"
              f"\n\t Código de vacuna"
              f"\n\t Código de estadística"
              f"\n\t Valor de estadística")
    elif e.pgcode == psycopg2.errorcodes.FOREIGN_KEY_VIOLATION:
        if 'cod_vacuna' in e.diag.message_detail:
            print(f"\nFALLO: Violación de clave foránea."
                  f"\nLa vacuna con clave cod_vacuna ({v_cod}) no está presente en la tabla VACUNA.")
        if 'cod_estadistica' in e.diag.message_detail:
            print(f"\nFALLO: Violación de clave foránea."
                  f"\nLa estadistica con clave cod_estadistica ({e_cod}) no está presente en la tabla ESTADISTICA.")
    else:
        print(f"\nError genérico: {e.pgcode} : {e.pgerror}")


def registrar_estadistica_vacuna(conn):
    """
    Trata de registrar una nueva fila sobre la entidad ESTADISTICA_VACUNA con los datos otorgados por el usuario.

    Parameters
    ----------
    conn:
        La conexión con la base de datos.
    """
    inputs = form_registrar_estadistica_vacuna()
    v_criteria = inputs['v_criteria']
    e_criteria = inputs['e_criteria']
    e_valor = inputs['e_valor']
    e_desc = inputs['e_desc']

    with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cur:
        try:
            # Check si el dato es el nombre o es el codigo
            if isinstance(v_criteria, str):
                v_cod = get_cod_vacuna(cur, v_criteria)
                if v_cod is None:
                    print(f"No se encontró ninguna vacuna con el nombre \"{v_criteria}\"")
                    conn.rollback()
                    return
                else:
                    v_criteria = v_cod
            # Check si el dato es el nombre o es el codigo
            if isinstance(e_criteria, str):
                e_cod = get_cod_estadistica(cur, e_criteria)
                if e_cod is None:
                    print(f"No se encontró ninguna estadística con el nombre \"{e_criteria}\"")
                    conn.rollback()
                    return
                else:
                    e_criteria = e_cod

            insert_estadistica_vacuna(cur, v_criteria, e_criteria, e_valor, e_desc)
            conn.commit()
            print(f"Estadística registrada.")
        except psycopg2.Error as e:
            registrar_estadistica_vacuna_control_errores(e, v_criteria, e_criteria)
            conn.rollback()


def listar_recomendaciones(conn):
    """
    Realiza una búsqueda en la base de datos sobre la tabla RECOMENDACIONES y lista todas las filas encontradas.

    Parameters
    ----------
    conn:
        La conexión con la base de datos.
    """
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
    """
    Realiza una búsqueda en la base de datos sobre la tabla RECOMENDACIONES en base a un código de recomendación
    o nombre de organización otorgado por el usuario.

    Parameters
    ----------
    conn:
        La conexión con la base de datos.
    """
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
                          f"\n\t Descripción: {desc}")
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


def form_borrar_recomendaciones():
    """
    Obtiene del usuario la información necesaria para poder borrar una fila en la entidad
    RECOMENDACION_VACUNA.

    Returns
    -------
    data:
        Diccionario de datos con los siguientes elementos:
        <código de la recomendación> con clave 'cod_r',
        <código de la vacuna> con clave 'cod_v'
    """
    scodr = input("Código de recomendación: ")
    cod_r = None if scodr == "" else int(scodr)

    scodv = input("Código de vacuna: ")
    cod_v = None if scodv == "" else scodv.upper()

    return {'cod_r': cod_r, 'cod_v': cod_v}


def borrar_recomendaciones_vacuna(conn):
    inputs = form_borrar_recomendaciones()
    r_cod = inputs['cod_r']
    v_cod = inputs['cod_v']

    with conn.cursor() as cur:
        try:
            sql = "delete from recomendacion_vacuna where cod_vacuna= (%(cod_v)s) and cod_recomendacion= (%(cod_r)s)"

            cur.execute(sql, inputs)
            conn.commit()
            print(f"Recomendación de vacuna borrada.")
        except psycopg2.Error as e:
            if e.pgcode == psycopg2.errorcodes.UNDEFINED_TABLE:
                print("ERRO: a táboa non existe")
            else:
                print(f"Erro xenérico: {e.pgcode} : {e.pgerror}")
            conn.rollback()
            
def form_modificar_recomendacion():
    """
    Obtiene del usuario la información necesaria para poder realizar la modificación de una fila en la entidad
    RECOMENDACION.

    Returns
    -------
    data:
        Diccionario de datos con los siguientes elementos:
        <código> con clave 'cod_r',
        <organización> con clave 'org',
        <descripción> con clave 'desc'
    """
    scod = input("Codigo de la recomendación que se quiere modificar: ")
    cod_r = None if scod == "" else int(scod)

    sorg = input("Nuevo nombre de organización: ")
    org = None if sorg == "" else sorg.upper()

    sdesc = input("Descripción de recomendación: ")
    desc = None if sdesc == "" else sdesc
    return {'cod': cod_r, 'nom': org, 'desc': desc}
    
def modificar_recomendacion(conn):
    inputs= form_modificar_recomendacion()
    cod= inputs['cod']
    org= inputs['nom']
    desc= inputs['desc']
    
    with conn.cursor() as cur:
        try:
            sql = "update recomendacion set organizacion=(%(nom)s), descripcion=(%(desc)s) where cod_recomendacion= (%(cod)s)"

            cur.execute(sql, inputs)
            conn.commit()
            print(f"Recomendación de modificada.")
        except psycopg2.Error as e:
            if e.pgcode == psycopg2.errorcodes.UNDEFINED_TABLE:
                print("ERRO: a táboa non existe")
            else:
                print(f"Erro xenérico: {e.pgcode} : {e.pgerror}")
            conn.rollback()
            
def menu_vacuna(conn,vac):
    MENU_TEXT = """
          -- MENÚ > Quieres añadir una recomendación para la nueva vacuna?--
    1 - Añadir
    q - No 
    """
    while True:
        print(MENU_TEXT)
        tecla = input('Opción> ')
        if tecla == 'q':
            break
        elif tecla == '1':
            rec = agregar_recomendacion(conn)
            conectar_vacuna_recomendacion(conn, vac, rec)

def conectar_vacuna_recomendacion(conn,vac,rec):
    
    with conn.cursor() as cur:
        try:
            insert_recomendacion_vacuna(cur, rec, vac, datetime.now().strftime("%d/%m/%Y"))
            conn.commit()
            print("Recomendación para la vacuna registrada")
        except psycopg2.Error as e:
            if e.pgcode == psycopg2.errorcodes.UNDEFINED_TABLE:
                print("La tabla no existe.")
            elif e.pgcode == psycopg2.errorcodes.NOT_NULL_VIOLATION:
                if "cod_vacuna" in e.pgerror:
                    print("El código de recomendación es obligatorio.")
                elif "organizacion" in e.pgerror:
                    print("La fecha de la recomendación es obligatoria.")
                else:
                    print("El código de vacuna para la recomendación es obligatorio.")
            else:
                print(f"Error genérico: {e.pgcode} : {e.pgerror}")
            conn.rollback()
    
    


def menu_recomendaciones(conn):
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


# ------------------------------------------------------------
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
9 - Registrar recomendación sobre vacuna
a - Borrar una recomendación de una vacuna
b - Modificar una recomendación
q - Saír   
"""
    while True:
        print(MENU_TEXT)
        tecla = input('Opción> ')
        if tecla == 'q':
            break
        elif tecla == '1':
            agregar_vacuna(conn)
        elif tecla == '2':
            agregar_recomendacion(conn)
        elif tecla == '3':
            agregar_estadistica(conn)
        elif tecla == '4':
            buscar_estadisticas_vacuna(conn, False)
        elif tecla == '5':
            buscar_recomendaciones_vacuna(conn, False)
        elif tecla == '6':
            menu_recomendaciones(conn)
        elif tecla == '7':
            listar_estadisticas(conn)
        elif tecla == '8':
            registrar_estadistica_vacuna(conn)
        elif tecla == '9':
            registrar_recomendacion_vacuna(conn)
        elif tecla == 'a':
            borrar_recomendaciones_vacuna(conn)
        elif tecla == 'b':
            modificar_recomendacion(conn)


# ------------------------------------------------------------
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


# ------------------------------------------------------------

if __name__ == '__main__':
    main()


# EJEMPLOS viejos


# ------------------------------------------------------------
def select_table(conn):
    with conn.cursor() as cur:
        cur.execute("select * from artigo")
        row = cur.fetchone()
        while row:
            print(f"Fila número {cur.rownumber} de {cur.rowcount}: {row}")
            row = cur.fetchone()


# ------------------------------------------------------------
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


# ------------------------------------------------------------
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
            if control_tx:
                conn.comit()
        except psycopg2.Error as e:
            print(f"Erro xenérico: {e.pgcode} : {e.pgerror}")
            if control_tx:
                conn.rollback()
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
