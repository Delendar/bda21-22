# Índice

- [Instalación del entorno](#instalacion-entorno)
  - [Base de datos](#base-de-datos)
- [Dominio](#dominio)
  - [Decisiones de diseño](#decisiones-de-diseño)
- [TO:DO](#todo)
  - [Diseño](#diseño)
  - [Aplicación Python](#aplicacion-python)
    - [Funcionalidades de obtención de datos](#func-obtencion-datos)
    - [Funcionalidades de modificación de datos](#func-modificacion-datos)
  - [Gestión de errores](#gestion-de-errores)

<a id="instalacion-entorno"></a>
# Instalación del entorno

<a id="base-de-datos"></a>
## Base de datos

|   Parámetro   |    Valor    |
|:-------------:|:-----------:|
|     host      | _localhost_ |
|    usuario    | _testuser_  |
|  contraseña   | _testpass_  |
| base de datos |  _testdb_   |

Creación de un usuario
```postgresql
CREATE USER testuser 
    WITH [ ENCRYPTED | UNENCRYPTED ] PASSWORD 'testpass' CREATEDB;
```
Creación de la base de datos
```postgresql
CREATE DATABASE testdb;
```
Creación de las tablas (vía ejecución del script conectado al usuario en psql)
```postgresql
/* Conexión al usuario */
psql -U testuser
/* Conexión a la DB */
\c testdb
/* Ejecución del script */
\i 'path/script.sql'
```
Creación de las tablas (vía ejecución línea de comandos de SO) 
```bash
psql -U testuser -d testdb -a -f script.sql
```

```postgresql
/* Para obtener información sobre la conexión actual */
\conninfo

/* Para cambiar de usuario conectado en postgres */
\c - a_new_user 
/* Para cambiar de usuario conectado y base de datos en postgres */
\c a_new_database a_new_user
```


## Dependencias Python

- Python 3.X
- Instalación de la librería <span style="font-family:monospace;">psycopg2</span>:
  ```bash
  pip install psycopg2
  ```

<a id="estructura-bd"></a>
## Estructura de la base de datos

<span style="font-family:monospace;">vacuna</span>

|     PK     |               |
|:----------:|:-------------:|
| cod_vacuna | nombre_vacuna |

<span style="font-family:monospace;">estadistica</span>

|       PK        |                    |
|:---------------:|:------------------:|
| cod_estadistica | nombre_estadistica |


<span style="font-family:monospace;">recomendacion</span>

|        PK         |              |             |
|:-----------------:|:------------:|:-----------:|
| cod_recomendacion | organizacion | descripcion |

<span style="font-family:monospace;">recomendacion_vacuna</span>

|   PK, FK   |      PK, FK       |                  |
|:----------:|:-----------------:|:----------------:|
| cod_vacuna | cod_recomendacion | fecha_aplicacion |

<span style="font-family:monospace;">estadistica_vacuna</span>

|   PK, FK   |     PK, FK      |       |             |
|:----------:|:---------------:|:-----:|:-----------:|
| cod_vacuna | cod_estadistica | valor | descripcion |

<a id="dominio"></a>
# Dominio

<a name="decisiones-de-diseño"></a>
## Decisiones de diseño 

La separación de las entidades en:
- <span style="font-family:monospace;">Vacuna</span>
- <span style="font-family:monospace;">Estadisticas</span>
- <span style="font-family:monospace;">Recomendacion</span>
- <span style="font-family:monospace;">Recomendaciones_vacuna</span>
- <span style="font-family:monospace;">Estadistias_vacuna</span>

Se deben a la capacidad de abstracción que nos ofrecerá tenerlas separadas, de tal forma que sean fácilmente accesibles
tanto las estadísticas que se pueden almacenar de las vacunas como las recomendaciones que se pueden aplicar a una de
estas. De la misma forma esto nos permite añadir de forma sencilla a la base de datos tanto nuevas recomendaciones 
todavía no aplicadas como estadísticas no medidas.

Esto también nos permitirá crear de forma más sencilla una interfaz mediante la cual la adición de una vacuna al sistema
llegue seguida de asignaciones de recomendaciones o estadísticas ya tomadas.

Esta abtracción nos ofrece una sencilla accesibilidad y edición tanto mediante nombres de vacunas y/o estadísticas como
sus códigos de identificación. La existencia de un campo descriptivo en las estadísticas sobre una vacuna es de buen uso
en caso de que el nombre de la estadística no sea lo sufientemente descriptivo _(e.g. : en caso de un porcentaje se podría
aclarar si se guarda en base 100 o en base 1)_

En cuanto a la abstracción de las recomendaciones y sus relaciones con una vacuna nos permite controlarlas mediante la
mera existencia de su asignación en la entidad <span style="font-family:monospace;">Recomendaciones_vacuna</span>.

> Dado que la base de datos es pequeña y es fundamental el correcto acceso a datos correcta y completamente modificados
> haremos uso de un nivel de aislamiento alto, serializable.
> ¿Por poner algo?

<a name="todo"></a>
# TO:DO 

<a name="diseño"></a>
## Diseño 
- [X] E/R
- [X] Modelo Relacional
- [X] Diccionario de Datos
- [X] Script SQL

<a name="aplicacion-python"></a>
## Aplicación Python: 

No contará con gestión DDL. La creación de la base de datos se realizará con el script SQL.

Leyenda de prioridades:

| Prioridad | Símbolo                                                    |
|:---------:|:----------------------------------------------------------:|
|   Alta    |  <span style="font-family:monospace;color:red;">A</span>   |
|   Media   | <span style="font-family:monospace;color:yellow;">M</span> |
|   Baja    | <span style="font-family:monospace;color:green;">B</span>  |
| Opcional  | <span style="font-family:monospace;color:green;">O</span>  |

Los apartados con prioridad <span style="font-family:monospace;color:red;">ALTA</span> es lo mínimo necesario para las 
funcionalidades.

<a name="func-obtencion-datos"></a>
### Funcionalidades de obtención de datos: 
- [X] Recuperación de información de una vacuna (fila única).
  - [X] <span style="font-family:monospace;color:red;">A</span> Por identificador.
  - [X] <span style="font-family:monospace;color:yellow;">M</span> Por nombre de vacuna.
- [ ] Recuperación de información de recomendación.
  - [X] <span style="font-family:monospace;color:red;">A</span> Por organización (filas múltiples).
  - [X] <span style="font-family:monospace;color:yellow;">M</span> Por identificador (fila única). 
  - [ ] <span style="font-family:monospace;color:green;">O</span> ¿Por descripciones? (filas múltiples). 
- [ ] Recuperación de recomendaciones por vacuna.
  - [X] <span style="font-family:monospace;color:red;">A</span> Por vacuna (filas múltiples). 
  - [ ] <span style="font-family:monospace;color:green;">B</span> Por fechas (filas múltiples). 
- [X] Recuperación de estadísticas.
  - [X] <span style="font-family:monospace;color:yellow;">M</span> Por vacuna (filas múltiples). 
- [X] Listado de estadísticas.
  - [X] <span style="font-family:monospace;color:green;">B</span> Completas (filas múltiples). 

<a name="func-modificacion-datos"></a>
### Funcionalidades de modificación de datos: 
- [ ] Vacuna:
  - [X] <span style="font-family:monospace;color:red;">A</span> Inserción de vacuna.
  - [X] <span style="font-family:monospace;color:red;">A</span> Inserción de estadísticas de una vacuna.
  - [ ] <span style="font-family:monospace;color:red;">A</span> Modificación de vacuna
  (mínimo 1 funcionalidad de modificación directa). 
- [x] Recomendación:
  - [X] <span style="font-family:monospace;color:red;">A</span> Inserción de recomendación. 
  - [x] <span style="font-family:monospace;color:red;">A</span> Inserción de una recomendación para una vacuna. 
  - [x] <span style="font-family:monospace;color:red;">A</span> Modificación de recomendación 
  (mínimo 1 funcionalidad de modificación directa).
- [ ] Estadísticas:
  - [X] <span style="font-family:monospace;color:red;">A</span> Inserción de estadísticas.
  - [x] <span style="font-family:monospace;color:red;">A</span> Modificación de estadística.
  (mínimo 1 funcionalidad de modificación incremental).
- [ ] Inserciones múltiples:
  - [x] <span style="font-family:monospace;color:red;">A</span> Inserción de recomendación y vacuna asociada.
  - [ ] <span style="font-family:monospace;color:yellow;">M</span> Inserción de vacuna y estadísticas.
- [ ] Borrados:
  - [x] <span style="font-family:monospace;color:red;">A</span> Borrado de recomendaciones sobre vacunas.
  - [ ] <span style="font-family:monospace;color:green;">B</span> Borrado de estadísticas sobre vacunas.

<a name="gestion-de-errores"></a>
## Gestión de errores. 
Errores a considerar:
- Comunes:
  - [ ] Nulidad de clave primaria.
  - [ ] Duplicación de clave primaria.
- Vacunas:
  - [ ] Inexistencia de:
    - <span style="font-family:monospace;">nombre_vacuna</span>
  - [ ] Valores nulos en:
    - <span style="font-family:monospace;">nombre_vacuna</span>
  - [ ] Valores duplicados en:
    - <span style="font-family:monospace;">nombre_vacuna</span>
- Recomendación:
  - [ ] Inexistencia de:
    - <span style="font-family:monospace;">organizacion</span>
  - [ ] Valores nulos en:
    - <span style="font-family:monospace;">organizacion</span>
    - <span style="font-family:monospace;">descripcion</span>
- Estadística:
  - [ ] Inexistencia de:
    - <span style="font-family:monospace;">nombre_estadistica</span>
  - [ ] Valores nulos en:
    - <span style="font-family:monospace;">nombre_estadistica</span>
  - [ ] Valores duplicados en:
    - <span style="font-family:monospace;">nombre_estadistica</span>
  - [ ] Números no admitidos:
    - [ ] Parte entera demasiado grande.
    - [ ] Parte decimal demasiado grande.
- Estadística-vacuna:
  - [X] Inexistencia de:
    - <span style="font-family:monospace;">nombre_vacuna</span>
    - <span style="font-family:monospace;">nombre_estadistica</span>
  - [X] Valores nulos en:
    - <span style="font-family:monospace;">valor</span>
  - [X] Inexistencia de valores objetivo de claves referenciales en:
    - <span style="font-family:monospace;">cod_vacuna</span>
    - <span style="font-family:monospace;">cod_estadistica</span>
- Recomendación-vacuna:
  - [ ] Inexistencia de:
    - <span style="font-family:monospace;">nombre_vacuna</span>
  - [ ] Valores nulos en:
    - <span style="font-family:monospace;">fecha_aplicacion</span>
  - [ ] Inexistencia de valores objetivo de claves referenciales en:
    - <span style="font-family:monospace;">cod_vacuna</span>
    - <span style="font-family:monospace;">cod_recomendacion</span>