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
import psycopg2.extensions
import sys
import datetime
from datetime import datetime

DBHOST = "localhost"
DBUSER = "testuser"
DBUSERPASS = "testpass"
DBNAME = "testdb"
DBMAXDIGITCOUNT = 12
DBMAXFLOATDIGITCOUNT = 2


# Database --------------------------------------------------------------------
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


def disconnect_db(conn):
    conn.commit()
    conn.close()


# ID finders ------------------------------------------------------------------
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


# DB inserts ------------------------------------------------------------------
def insert_vacuna(cur, v_cod, v_nom):
    """
    Ejecuta la sentencia de inserción de una vacuna en la tabla VACUNA.

    Parameters
    ----------
    cur:
        Cursor con conexión a la base de datos donde se realiza la inserción.
    v_cod: int
        Código de la vacuna a insertar.
    v_nom: str
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


# Insert functionalities ------------------------------------------------------
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
        código Asignado a la clave "cod",
        nombre Asignado a la clave "nom"
    """
    scod = input(f"Codigo de {nombre_data}: ")
    cod = None if scod == "" else scod

    snome = input(f"Nombre de {nombre_data}: ")
    nombre = None if snome == "" else snome.upper()

    return {'cod': cod,
            'nom': nombre}


def agregar_vacuna(conn):
    """
    Intenta insertar en la base de datos una nueva fila sobre la tabla VACUNA con los datos
    otorgados por el usuario.

    Parameters
    ----------
    conn:
        La conexión a la base de datos.
    """

    conn.isolation_level = psycopg2.extensions.ISOLATION_LEVEL_SERIALIZABLE

    inputs = form_generico('vacuna')
    v_cod = inputs['cod']
    v_nom = inputs['nom']

    with conn.cursor() as cur:
        try:
            insert_vacuna(cur, v_cod, v_nom)
            num_rec_registradas = menu_vacuna(conn, v_cod)
            if num_rec_registradas == -1:
                conn.rollback()
                print("Ha ocurrido un error en la realización de las transacciones, no se ha añadido la vacuna.")
            else:
                conn.commit()
                print("Vacuna añadida")
                print(f"Se han registrado un total de {num_rec_registradas} recomendaciones sobre la vacuna.")
        except psycopg2.Error as e:
            if e.pgcode == psycopg2.errorcodes.UNDEFINED_TABLE:
                print("\nERROR: La tabla VACUNA  no existe")
            elif e.pgcode == psycopg2.errorcodes.UNIQUE_VIOLATION:
                if "cod_vacuna" in e.pgerror:
                    print("\nERROR: Violación de restricción de unicidad."
                          f"\nYa existe una vacuna con el código ({v_cod})")
                else:
                    print("\nERROR: Violación de restricción de unicidad."
                          f"\nYa existe una vacuna con el nombre ({v_nom})")
            elif e.pgcode == psycopg2.errorcodes.NOT_NULL_VIOLATION:
                if "cod_vacuna" in e.pgerror:
                    print("\nERROR: El código de vacuna es obligatorio.")
                else:
                    print("\nERROR: El nombre de la vacuna es obligatorio.")
            elif e.pgcode == psycopg2.errorcodes.INVALID_TEXT_REPRESENTATION:
                print("\nERROR: Representación no válida."
                      "\nEl código de vacuna debe de ser un número.")
            else:
                print(f"\nFALLO: Error genérico {e.pgcode}: {e.pgerror}")
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

    conn.isolation_level = psycopg2.extensions.ISOLATION_LEVEL_SERIALIZABLE

    inputs = form_generico('estadistica')
    e_cod = inputs['cod']
    e_nom = inputs['nom']

    with conn.cursor() as cur:
        try:
            insert_estadistica(cur, e_cod, e_nom)
            conn.commit()
            print("Estadistica registrada")
        except psycopg2.Error as e:
            if e.pgcode == psycopg2.errorcodes.UNDEFINED_TABLE:
                print("\nERROR: la tabla ESTADISTICA no existe.")
            elif e.pgcode == psycopg2.errorcodes.UNIQUE_VIOLATION:
                if "cod_estadistica" in e.pgerror:
                    print("\nERROR: Violación de restricción de unicidad."
                          f"\nYa existe una estadística con el código ({e_cod})")
                else:
                    print("\nERROR: Violación de restricción de unicidad."
                          f"\nYa existe una estadística con el nombre ({e_nom})")
            elif e.pgcode == psycopg2.errorcodes.NOT_NULL_VIOLATION:
                if "cod_estadistica" in e.pgerror:
                    print("\nERROR: El código de estadística es obligatorio.")
                else:
                    print("\nERROR: El nombre de estadística es obligatorio.")
            elif e.pgcode == psycopg2.errorcodes.INVALID_TEXT_REPRESENTATION:
                print("\nERROR: Representación no válida."
                      "\nEl código de estadística debe de ser un número.")
            else:
                print(f"\nFALLO: Error genérico {e.pgcode}: {e.pgerror}")
            conn.rollback()


def form_agregar_recomendacion():
    """
    Obtiene del usuario la información necesaria para poder realizar la inserción de una nueva fila en la entidad
    RECOMENDACION.

    Returns
    -------
    data:
        Diccionario de datos con los siguientes elementos:
        código con clave 'cod_r',
        organización con clave 'org',
        descripción con clave 'desc'
    """
    scod = input("Codigo de recomendación: ")
    cod_r = None if scod == "" else scod

    sorg = input("Organización: ")
    org = None if sorg == "" else sorg.upper()

    sdesc = input("Descripción de recomendación: ")
    desc = None if sdesc == "" else sdesc
    return {'cod': cod_r, 'org': org, 'desc': desc}


def agregar_recomendacion(conn):
    """
    Trata de agregar una nueva fila a la entidad RECOMENDACION con datos otorgados por el usuario.

    Parameters
    ----------
    conn:
        La conexión con la base de datos.
    """

    conn.isolation_level = psycopg2.extensions.ISOLATION_LEVEL_SERIALIZABLE

    inputs = form_agregar_recomendacion()
    r_cod = inputs['cod']
    r_org = inputs['org']
    r_desc = inputs['desc']

    with conn.cursor() as cur:
        try:
            insert_recomendacion(cur, r_cod, r_org, r_desc)
            conn.commit()
            print("Recomendación registrada")
            return r_cod
        except psycopg2.Error as e:
            if e.pgcode == psycopg2.errorcodes.UNDEFINED_TABLE:
                print("\nERROR: La tabla RECOMENDACION_VACUNA no existe.")
            elif e.pgcode == psycopg2.errorcodes.NOT_NULL_VIOLATION:
                if "cod_recomendacion" in e.pgerror:
                    print("\nERROR: El código de recomendación es obligatorio.")
                elif "organizacion" in e.pgerror:
                    print("\nERROR: La organización que propone la recomendación es obligatoria.")
                else:
                    print("\nERROR: La descripción de la recomendación es obligatoria.")
            elif e.pgcode == psycopg2.errorcodes.UNIQUE_VIOLATION:
                if "cod_recomendacion" in e.pgerror:
                    print(f"\nERROR: Violación de unicidad."
                          f"\nYa existe una recomendación con el código ({r_cod})")
            elif e.pgcode == psycopg2.errorcodes.INVALID_TEXT_REPRESENTATION:
                print("\nERROR: Representación no válida."
                      "\nEl código de recomendación debe de ser un número.")
            else:
                print(f"\nFALLO: Error genérico {e.pgcode}: {e.pgerror}")
            conn.rollback()


def form_registrar_recomendacion_vacuna():
    """
    Obtiene del usuario la información necesaria para poder realizar la inserción de una nueva fila en la entidad
    RECOMENDACION_VACUNA.

    Returns
    -------
    data:
        Diccionario de datos con los siguientes elementos:
        código de la recomendación con clave 'cod_r',
        código de la vacuna con clave 'cod_v'
    """
    scodr = input("Codigo de recomendación: ")
    cod_r = None if scodr == "" else scodr

    scodv = input("Código de la vacuna: ")
    cod_v = None if scodv == "" else scodv

    return {'rec': cod_r, 'vac': cod_v}


def registrar_recomendacion_vacuna(conn):
    """
    Trata de agregar una nueva fila a la entidad RECOMENDACION_VACUNA con datos otorgados por el usuario.

    Parameters
    ----------
    conn:
        La conexión con la base de datos.
    """

    conn.isolation_level = psycopg2.extensions.ISOLATION_LEVEL_SERIALIZABLE

    inputs = form_registrar_recomendacion_vacuna()
    r_cod = inputs['rec']
    v_cod = inputs['vac']

    with conn.cursor() as cur:
        try:
            insert_recomendacion_vacuna(cur, r_cod, v_cod, datetime.now().strftime("%d/%m/%Y"))
            conn.commit()
            print("Recomendación para la vacuna registrada")
        except psycopg2.Error as e:
            if e.pgcode == psycopg2.errorcodes.UNDEFINED_TABLE:
                print("\nERROR: La tabla no RECOMENDACION_VACUNA no existe.")
            elif e.pgcode == psycopg2.errorcodes.NOT_NULL_VIOLATION:
                if "cod_vacuna" in e.pgerror:
                    print("\nERROR: El código de vacuna para la recomendación es obligatorio.")
                elif "fecha" in e.pgerror:
                    print("\nERROR: La fecha de la recomendación es obligatoria.")
                else:
                    print("\nERROR: El código de la recomendación es obligatorio.")
            elif e.pgcode == psycopg2.errorcodes.UNIQUE_VIOLATION:
                print("\nERROR: Violación de clave primaria."
                      f"\nLa recomendación ({r_cod}) ya está asociada a la vacuna ({v_cod}).")
            elif e.pgcode == psycopg2.errorcodes.FOREIGN_KEY_VIOLATION:
                print("\nERROR: Violación de clave foránea.")
                if "cod_recomendacion" in e.pgerror:
                    print(f"\nEl código de la recomendación ({r_cod}) no está registrado.")
                else:
                    print(f"\nEl código de la vacuna ({v_cod}) no está registrado.")
            elif e.pgcode == psycopg2.errorcodes.INVALID_TEXT_REPRESENTATION:
                print("\nERROR: Representación no válida de identificador."
                      "\nLos códigos deben de ser un número.")
            else:
                print(f"\nFALLO: Error genérico: {e.pgcode} : {e.pgerror}")
            conn.rollback()


def conectar_vacuna_recomendacion(conn, vac, rec_inputs):
    """
    Crea una fila nueva en la entidad RECOMENDACION_VACUNA que asigne la recomendación y la
    vacuna creadas anteriormente a fecha de hoy.

    Parameters
    ----------
    conn:
        La conexión con la base de datos.
    vac: int
        Código de la vacuna que se asigna la recomendación.
    rec_inputs: dict
        Diccionario de datos con:
        código de la recomendación a añadir con clave 'cod',
        organización de la recomendación a añadir con clave 'org',
        descripción de la recomendación a añadir con clave 'desc'

    Returns
    -------
        1 si se ha realizado la inserción de la recomendación y el registro asociada a la vacuna,
        0 en caso contrario
    """

    r_cod = rec_inputs['cod']
    r_org = rec_inputs['org']
    r_desc = rec_inputs['desc']

    with conn.cursor() as cur:
        try:
            insert_recomendacion(cur, r_cod, r_org, r_desc)
            insert_recomendacion_vacuna(cur, r_cod, vac, datetime.now().strftime("%d/%m/%Y"))
            return 1
        except psycopg2.Error as e:
            if e.pgcode == psycopg2.errorcodes.UNDEFINED_TABLE:
                print("ERROR: La tabla RECOMENDACION_VACUNA no existe.")
            elif e.pgcode == psycopg2.errorcodes.NOT_NULL_VIOLATION:
                if "cod_vacuna" in e.pgerror:
                    print("\nEl código de la vacuna es obligatorio.")
                elif "cod_recomendacion" in e.pgerror:
                    print("\nEl código de recomendacion para la recomendación es obligatorio.")
                else:
                    print("\nLa fecha de la recomendación es obligatoria.")
            elif e.pgcode == psycopg2.errorcodes.FOREIGN_KEY_VIOLATION:
                print("\nERROR: Violación de clave foránea.")
                if "cod_vacuna" in e.pgerror:
                    print(f"El código de vacuna ({vac}) no está registrado.")
                else:
                    print(f"El código de recomendación ({r_cod} no está registrado.")
            elif e.pgcode == psycopg2.errorcodes.UNIQUE_VIOLATION:
                print(f"\nERROR: Violación de restricción de unicidad.")
                print(f"Ya existe una recomendación con el código ({r_cod})")
            elif e.pgcode == psycopg2.errorcodes.INVALID_TEXT_REPRESENTATION:
                print("\nERROR: Representación no válida."
                      "\nLos códigos deben de ser un número.")
            else:
                print(f"\nFALLO: Error genérico: {e.pgcode} : {e.pgerror}")
            return 0


def form_registrar_estadistica_vacuna():
    """
    Obtiene del usuario la información necesaria para poder realizar la inserción de una nueva fila en la entidad
    ESTADISTICA_VACUNA.

    Returns
    -------
    data:
        Diccionario de datos con los siguientes elementos:
        criterio de igualdad de la vacuna con clave 'v_criteria',
        criterio de igualdad de la estadística con clave 'e_criteria',
        valor de la estadística con clave 'e_valor',
        descripción de la estadística con clave 'e_desc'
    """
    sv_cod = input("Código o nombre de vacuna: ")
    if sv_cod == "":
        v_criteria = None
    elif sv_cod.isdigit():
        v_criteria = sv_cod
    else:
        v_criteria = sv_cod.upper()

    se_cod = input("Código o nombre de estadística: ")
    if se_cod == "":
        e_criteria = None
    elif se_cod.isdigit():
        e_criteria = se_cod
    else:
        e_criteria = se_cod.upper()

    se_valor = input("Valor de la estadística (valor numérico): ")
    e_valor = None if se_valor == "" else se_valor

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
        print("\nERROR: Violación de clave foránea.")
        if 'cod_vacuna' in e.diag.message_detail:
            print(f"\nLa vacuna con clave cod_vacuna ({v_cod}) no está presente en la tabla VACUNA.")
        if 'cod_estadistica' in e.diag.message_detail:
            print(f"\nLa estadística con clave cod_estadistica ({e_cod}) no está presente en la tabla ESTADISTICA.")
    elif e.pgcode == psycopg2.errorcodes.NUMERIC_VALUE_OUT_OF_RANGE:
        print("\nERROR: Desbordamiento en el atributo valor."
              f"\nEl sistema solo admite números de {DBMAXDIGITCOUNT} en la parte entera "
              f"y {DBMAXFLOATDIGITCOUNT} decimales."
              f"\nEn caso de tener más de {DBMAXFLOATDIGITCOUNT} en la parte decimal, se truncará el número.")
    elif e.pgcode == psycopg2.errorcodes.INVALID_TEXT_REPRESENTATION:
        print("\nERROR: Representación no válida."
              "\nLos códigos identificadores y/o el valor de estadística deben de ser números.")
    else:
        print(f"\nFALLO: Error genérico: {e.pgcode} : {e.pgerror}")


def registrar_estadistica_vacuna(conn):
    """
    Trata de registrar una nueva fila sobre la entidad ESTADISTICA_VACUNA con los datos otorgados por el usuario.

    Parameters
    ----------
    conn:
        La conexión con la base de datos.
    """

    conn.isolation_level = psycopg2.extensions.ISOLATION_LEVEL_SERIALIZABLE

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


# Search functionalities ------------------------------------------------------
def listar_estadisticas(conn, control_tx=True):
    """
    Realiza una búsqueda en la base de datos sobre la tabla ESTADISTICA y lista todas las filas encontradas.

    Parameters
    ----------
    conn:
        La conexión con la base de datos.
    control_tx:
        Variable de control transaccional, predeterminado TRUE.
        Si TRUE entonces se realiza control transaccional,
        Si FALSE no se realiza.
    """
    if control_tx:
        conn.isolation_level = psycopg2.extensions.ISOLATION_LEVEL_READ_COMMITTED

    sql = "select * from estadistica"

    with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cur:
        try:
            cur.execute(sql)
            record = cur.fetchall()
            for row in record:
                c_est = row['cod_estadistica']
                n_est = row['nombre_estadistica']
                print(f"({c_est}) Nombre {n_est}")
            conn.commit()
        except psycopg2.Error as e:
            if e.pgcode == psycopg2.errorcodes.UNDEFINED_TABLE:
                print("\nERROR: La tabla no ESTADISTICA no existe.")
            print(f"\nFALLO: Error genérico: {e.pgcode} : {e.pgerror}")
            conn.rollback()


def listar_recomendaciones(conn, control_tx=True):
    """
    Realiza una búsqueda en la base de datos sobre la tabla RECOMENDACIONES y lista todas las filas encontradas.

    Parameters
    ----------
    conn:
        La conexión con la base de datos.
    control_tx:
        Variable de control transaccional, predeterminado TRUE.
        Si TRUE entonces se realiza control transaccional,
        Si FALSE no se realiza.
    """

    if control_tx:
        conn.isolation_level = psycopg2.extensions.ISOLATION_LEVEL_READ_COMMITTED

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
            conn.commit()
        except psycopg2.Error as e:
            print(f"\nFALLO: Error genérico: {e.pgcode} : {e.pgerror}")
            conn.rollback()


def buscar_recomendaciones(conn, control_tx=True):
    """
    Realiza una búsqueda en la base de datos sobre la tabla RECOMENDACIONES en base a un código de recomendación
    o nombre de organización otorgado por el usuario.

    Parameters
    ----------
    conn:
        La conexión con la base de datos.
    control_tx:
        Variable de control transaccional, predeterminado TRUE.
        Si TRUE entonces se realiza control transaccional,
        Si FALSE no se realiza.
    """

    if control_tx:
        conn.isolation_level = psycopg2.extensions.ISOLATION_LEVEL_READ_COMMITTED

    cod_search = False
    org = None
    scod = input("Criterio de búsqueda (código para búsqueda específica, nombre para organización): \n>")
    if scod == "":
        cod = None
    elif scod.isdigit():
        cod_search = True
        cod = int(scod)
    else:
        org = scod.upper()
        cod = None

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
            conn.commit()
        except psycopg2.Error as e:
            print(f"\nFALLO: Error genérico: {e.pgcode} : {e.pgerror}")
            conn.rollback()


def buscar_estadisticas_vacuna(conn, control_tx=True):
    """
    Realiza una búsqueda en la base de datos sobre la tabla ESTADISTICA_VACUNA
    en base a un código o nombre de una vacuna otorgado por el usuario.

    Parameters
    ----------
    conn:
        La conexión con la base de datos.
    control_tx:
        Variable de control transaccional, predeterminado TRUE.
        Si TRUE entonces se realiza control transaccional,
        Si FALSE no se realiza.
    """

    if control_tx:
        conn.isolation_level = psycopg2.extensions.ISOLATION_LEVEL_READ_COMMITTED

    cod_search = False
    scod = input("Código o nombre de vacuna: ")
    if scod == "":
        cod = None
        nom = None
    elif scod.isdigit():
        cod = int(scod)
        cod_search = True
        nom = None
    else:
        nom = scod.upper()
        cod = None

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
                if len(records) == 0:
                    print(f"\nNo se encontraron estadísticas para la vacuna ({cod})")
                else:
                    print(f"Mostrando información para la vacuna con código ({cod}):")
            else:
                if len(records) == 0:
                    print(f"No se encontraron estadísticas para la vacuna ({cod})")
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
            print("\n")
            if control_tx:
                conn.commit()
        except psycopg2.Error as e:
            print(f"\nFALLO: Error genérico: {e.pgcode} : {e.pgerror}")
            if control_tx:
                conn.rollback()
    return retval


def buscar_recomendaciones_vacuna(conn, control_tx=True):
    """
    Realiza una búsqueda en la base de datos sobre la tabla RECOMENDACIONES_VACUNA
    con base en un código o nombre de una vacuna otorgado por el usuario.

    Parameters
    ----------
    conn:
        La conexión con la base de datos.
    control_tx:
        Variable de control transaccional, predeterminado TRUE.
        Si TRUE entonces se realiza control transaccional,
        Si FALSE no se realiza.
    """

    if control_tx:
        conn.isolation_level = psycopg2.extensions.ISOLATION_LEVEL_READ_COMMITTED

    cod_search = False
    scod = input("Código o nombre de vacuna: ")
    if scod == "":
        cod = None
        nom = None
    elif scod.isdigit():
        cod = int(scod)
        cod_search = True
        nom = None
    else:
        nom = scod.upper()
        cod = None

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
                if len(records) == 0:
                    print(f"\nNo se encontraron recomendaciones para la vacuna ({cod})")
                else:
                    print(f"Mostrando información para la vacuna con código ({cod}):")
            else:
                if len(records) == 0:
                    print(f"No se encontraron recomendaciones para la vacuna \"{nom}\"")
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
                conn.commit()
        except psycopg2.Error as e:
            print(f"\nFALLO: Error genérico: {e.pgcode} : {e.pgerror}")
            if control_tx:
                conn.rollback()
    return retval


# Delete functionalities ------------------------------------------------------
def form_borrar_estadistica_vacuna():
    """
    Obtiene del usuario la información necesaria para poder borrar una fila en la entidad
    ESTADISTICAS_VACUNA.

    Returns
    -------
    data:
        Diccionario de datos con los siguientes elementos:
        código de la estadística con clave 'cod_e',
        código de la vacuna con clave 'cod_v'
    """
    scode = input("Código de estadística: ")
    cod_e = None if scode == "" else int(scode)

    scodv = input("Código de vacuna: ")
    cod_v = None if scodv == "" else scodv.upper()

    return {'cod_e': cod_e, 'cod_v': cod_v}


def borrar_estadisticas_vacuna(conn):
    """
    Borra de la base de datos una fila de la tabla ESTADISTIA_VACUNA según los códigos que
    le indique el usuario.

    Parameters
    ----------
    conn:
        La conexión con la base de datos.
    """

    conn.isolation_level = psycopg2.extensions.ISOLATION_LEVEL_SERIALIZABLE

    inputs = form_borrar_estadistica_vacuna()

    with conn.cursor() as cur:
        try:
            sql = "delete from estadistica_vacuna where cod_vacuna= (%(cod_v)s) and cod_estadistica= (%(cod_e)s)"

            cur.execute(sql, inputs)
            conn.commit()
            if cur.rowcount == 0:
                print("No se ha encontrado la estadística asociada a la vacuna.")
            else:
                print(f"Estadística asociada de vacuna borrada.")
        except psycopg2.Error as e:
            if e.pgcode == psycopg2.errorcodes.UNDEFINED_TABLE:
                print("\nERROR: la tabla ESTADISTICA_VACUNA no existe.")
            else:
                print(f"\nERROR: Error genérico: {e.pgcode} : {e.pgerror}")
            conn.rollback()


def form_borrar_recomendacion_vacuna():
    """
    Obtiene del usuario la información necesaria para poder borrar una fila en la entidad
    RECOMENDACION_VACUNA.

    Returns
    -------
    data:
        Diccionario de datos con los siguientes elementos:
        código de la recomendación con clave 'cod_r',
        código de la vacuna con clave 'cod_v'
    """
    scodr = input("Código de recomendación: ")
    cod_r = None if scodr == "" else int(scodr)

    scodv = input("Código de vacuna: ")
    cod_v = None if scodv == "" else scodv.upper()

    return {'cod_r': cod_r, 'cod_v': cod_v}


def borrar_recomendaciones_vacuna(conn):
    """
    Borra de la base de datos una fila de la tabla RECOMENDACION_VACUNA según los códigos que
    le indique el usuario

    Parameters
    ----------
    conn:
        La conexión con la base de datos.
    """

    conn.isolation_level = psycopg2.extensions.ISOLATION_LEVEL_SERIALIZABLE

    inputs = form_borrar_recomendacion_vacuna()

    with conn.cursor() as cur:
        try:
            sql = "delete from recomendacion_vacuna where cod_vacuna= (%(cod_v)s) and cod_recomendacion= (%(cod_r)s)"

            cur.execute(sql, inputs)
            conn.commit()
            if cur.rowcount == 0:
                print("No se ha encontrado la recomendación asociada a la vacuna.")
            else:
                print(f"Recomendación de vacuna borrada.")
        except psycopg2.Error as e:
            if e.pgcode == psycopg2.errorcodes.UNDEFINED_TABLE:
                print("\nERROR: la tabla RECOMENDACION_VACUNA no existe.")
            else:
                print(f"\nERROR: Error genérico: {e.pgcode} : {e.pgerror}")
            conn.rollback()


# Update functionalities ------------------------------------------------------
def form_modificar_recomendacion():
    """
    Obtiene del usuario la información necesaria para poder realizar la modificación de una fila en la entidad
    RECOMENDACION.

    Returns
    -------
    data:
        Diccionario de datos con los siguientes elementos:
        código con clave 'cod_r',
        organización con clave 'org',
        descripción con clave 'desc'
    """
    scod = input("Codigo de la recomendación que se quiere modificar: ")
    cod_r = None if scod == "" else int(scod)

    sorg = input("Nuevo nombre de organización: ")
    org = None if sorg == "" else sorg.upper()

    sdesc = input("Descripción de recomendación: ")
    desc = None if sdesc == "" else sdesc
    return {'cod': cod_r, 'nom': org, 'desc': desc}


def modificar_recomendacion(conn):
    """
    Hace un update de los campos nombre y descripción de la fila que tenga el código 
    indicado por el usuario en la entidad RECOMENDACION

    Parameters
    ----------
    conn:
        La conexión con la base de datos.
    """

    conn.isolation_level = psycopg2.extensions.ISOLATION_LEVEL_SERIALIZABLE

    inputs = form_modificar_recomendacion()

    with conn.cursor() as cur:
        try:
            sql = "update recomendacion set organizacion=(%(nom)s), descripcion=(%(desc)s) " \
                  "where cod_recomendacion= (%(cod)s)"

            cur.execute(sql, inputs)
            conn.commit()
            print(f"Recomendación modificada.")
        except psycopg2.Error as e:
            if e.pgcode == psycopg2.errorcodes.UNDEFINED_TABLE:
                print("\nERROR: La tabla no existe.")
            elif e.pgcode == psycopg2.errorcodes.NOT_NULL_VIOLATION:
                if "cod_vacuna" in e.pgerror:
                    print("\nEl código de recomendación es obligatorio.")
                elif "fecha" in e.pgerror:
                    print("\nLa fecha de la recomendación es obligatoria.")
                else:
                    print("\nEl código de vacuna para la recomendación es obligatorio.")
            conn.rollback()


def form_aumento_vacuna():
    """
    Obtiene del usuario la información necesaria para poder aumentar el valor de forma incremental del valor de una
    vacuna en la entidad ESTADISTICAS_VACUNA.

    Returns
    -------
    data:
        Diccionario de datos con los siguientes elementos:
        código con clave 'cod',
        porcentaje con clave 'por'
    """
    scod = input("Código de vacuna: ")
    cod = None if scod == "" else int(scod)

    ssta = input("Código de estadística: ")
    sta = None if ssta == "" else int(ssta)

    while True:
        sorg = input("Incremento (número o porcentaje): ")
        org = None if sorg == "" else sorg
        if org is not None and (sorg.lstrip("-+%").rstrip("%").isdigit()):
            break

    return {'cod': cod, 'sta': sta, 'por': org}


def aumento_vacuna(conn):
    """
    Modifica el valor de una vacuna. Si el usuario indica % en el incremento se calculará el tanto
    por ciento, si no se sumará el valor indicado.

    Parameters
    ----------
    conn:
        La conexión a la base de datos.
    """

    conn.isolation_level = psycopg2.extensions.ISOLATION_LEVEL_SERIALIZABLE

    inputs = form_aumento_vacuna()
    por = inputs['por']

    with conn.cursor() as cur:
        try:
            sql = "update estadistica_vacuna"

            if por.find("%") != -1:
                por = por.replace("%", "")
                print(por)
                sql = sql + " set valor = valor + valor *" + por + "/100" \
                                                                   "where cod_vacuna= (%(cod)s) and cod_estadistica = (%(sta)s)"
            else:
                sql = sql + " set valor = valor +" + por + \
                      "where cod_vacuna= (%(cod)s) and cod_estadistica = (%(sta)s)"

            cur.execute(sql, inputs)
            conn.commit()
            if cur.rowcount == 0:
                print(f"No se encontraron estadísticas para los códigos dados.")
            else:
                print(f"Valor modificado.")
        except psycopg2.Error as e:
            if e.pgcode == psycopg2.errorcodes.UNDEFINED_TABLE:
                print("\nERROR: La tabla ESTADISTICA_VACUNA no existe.")
            elif e.pgcode == psycopg2.errorcodes.NOT_NULL_VIOLATION:
                if "cod_vacuna" in e.pgerror:
                    print("\nEl código de la vacuna es obligatorio.")
                elif "cod_estadistica" in e.pgerror:
                    print("\nEl código de la estadística es obligatorio.")
                else:
                    print("\nEl valor del incremento es obligatorio")
            else:
                print(f"\nFALLO: Error genérico: {e.pgcode} : {e.pgerror}")
            conn.rollback()

        # Menus -----------------------------------------------------------------------


def menu_vacuna(conn, vac):
    """
    Ofrece al usuario la posibilidad de registrar recomendaciones nuevas sobre la vacuna que se ha añadido
    recientemente, dados datos otorgados por él mismo.

    Parameters
    ----------
    conn:
        Conexión con la base de datos.
    vac:
        Código de la vacuna que será añadida.

    Returns
    -------
    int:
        -1 si has sucedido un error a la hora de realizar las transacciones.
        O un número N indicando la cantidad de recomendaciones que se han registrado.
    """
    MENU_TEXT = """
          -- MENÚ > Quieres añadir una recomendación para la nueva vacuna?--
    1 - Añadir
    q - No 
    """
    num_rec_añadidas = 0
    while True:
        print(MENU_TEXT)
        tecla = input('Opción> ')
        if tecla == 'q':
            break
        elif tecla == '1':
            rec_inputs = form_agregar_recomendacion()
            if conectar_vacuna_recomendacion(conn, vac, rec_inputs) == 0:
                return -1
            else:
                num_rec_añadidas += 1
    return num_rec_añadidas


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
            listar_recomendaciones(conn, True)
        elif tecla == '2':
            buscar_recomendaciones(conn, True)


def menu(conn):
    """
    Imprime un menú de opcións, solicita a opción e executa a función asociada.
    'q' para saír.
    """
    MENU_TEXT = """
      -- MENÚ --
av - Añadir vacuna                          ar - Añadir recomendación                   ae - Añadir estadística
re - Registrar estadística de vacuna        rr - Registrar recomendación sobre vacuna
1 - Ver recomendaciones                     2 - Listar estadísticas
3 - Ver estadísticas de vacuna              4 - Ver recomendaciones de vacuna
5 - Modificar una recomendación             6 - Modificar estadística de vacuna
7 - Borrar una recomendación de una vacuna  8 - Borrar una estadística de una vacuna
q - Salir   
"""
    while True:
        print(MENU_TEXT)
        tecla = input('Opción> ')
        if tecla.lower() == 'q':
            break
        elif tecla.lower() == 'av':
            agregar_vacuna(conn)
        elif tecla.lower() == 'ar':
            agregar_recomendacion(conn)
        elif tecla.lower() == 'ae':
            agregar_estadistica(conn)
        elif tecla.lower() == 're':
            registrar_estadistica_vacuna(conn)
        elif tecla.lower() == 'rr':
            registrar_recomendacion_vacuna(conn)
        elif tecla == '1':
            menu_recomendaciones(conn)
        elif tecla == '2':
            listar_estadisticas(conn)
        elif tecla == '3':
            buscar_estadisticas_vacuna(conn)
        elif tecla == '4':
            buscar_recomendaciones_vacuna(conn)
        elif tecla == '5':
            modificar_recomendacion(conn)
        elif tecla == '6':
            aumento_vacuna(conn)
        elif tecla == '7':
            borrar_recomendaciones_vacuna(conn)
        elif tecla == '8':
            borrar_estadisticas_vacuna(conn)
        else:
            print("\nComando desconocido.")


def main():
    """
    Función principal. Conecta la base de datos y ejecuta el menú.
    En la salida del menú, desconecta la base de datos y finaliza el programa.
    """
    print('Conectando a PosgreSQL...')
    conn = connect_db()
    print('Conectado.')
    menu(conn)
    disconnect_db(conn)


if __name__ == '__main__':
    main()
