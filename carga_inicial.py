import os,logging,subprocess,re,json
import sqlite3
import psycopg2

dir_base=os.path.dirname(os.path.abspath(__file__))
file_politicas_json=os.path.join(dir_base,'politicas.json')
if os.path.isdir('/var/log'):
    path_log='/var/log/carga_inicial.log'
else:
    path_log=os.path.join(os.path.dirname(os.path.abspath(__file__)),'carga_inicial.log')
tareas=[
        ("test_conexion","tarea para testing de conexion al server"),
        ("sinc_users","tarea para sincronizacion de usuarios de los servers"),
        ("sinc_users_db","tarea para sincronizacion de usuarios de los servers"),
        ("ep","tarea para evaluacion de politicas en los servers"),
        ]


encoding=('ascii','windows-1252','utf_32','utf_32_be','utf_32_le','utf_16','utf_16_be','utf_16_le','utf_7','utf_8','utf_8_sig','iso-8859-1','iso8859_2','iso8859_3','iso8859_4','iso8859_5','iso8859_6','iso8859_7','iso8859_8','iso8859_9','iso8859_10','iso8859_11','iso8859_13','iso8859_14','iso8859_15','iso8859_16','big5','big5hkscs','cp037','cp273','cp424','cp437','cp500','cp720','cp737','cp775','cp850','cp852','cp855','cp856','cp857','cp858','cp860','cp861','cp862','cp863','cp864','cp865','cp866','cp869','cp874','cp875','cp932','cp949','cp950','cp1006','cp1026','cp1125','cp1140','cp1250','cp1251','cp1252','cp1253','cp1254','cp1255','cp1256','cp1257','cp1258','cp65001','euc_jp','euc_jis_2004','euc_jisx0213','euc_kr','gb2312','gbk','gb18030','hz','iso2022_jp','iso2022_jp_1','iso2022_jp_2','iso2022_jp_2004','iso2022_jp_3','iso2022_jp_ext','iso2022_kr','latin_1','johab','koi8_r','koi8_t','koi8_u','kz1048','mac_cyrillic','mac_greek','mac_iceland','mac_latin2','mac_roman','mac_turkish','ptcp154','shift_jis','shift_jis_2004','shift_jisx0213')
def clean_string(b=''):
    data=''
    print("begin funcion clean_string")
    for i in b:
        if re.fullmatch(r'[a-zA-Z0-9\_\-\ \t\n\,\<\>\.\!\#\\\/\(\)\=\?\:\;\$]',i) :
            data=data+i
    print("end func clean_string")
    return data
#configuracion inicial de logging
#logging.basicConfig(filename=os.path.join(dir_log,'cargar_inicial.log'),level=logging.WARNING )
logger = logging.getLogger('Carga_Inicial')
logger.setLevel(logging.DEBUG)
# create console handler and set level to debug
#ch = logging.StreamHandler()
#ch.setLevel(logging.WARNING)
fh = logging.FileHandler(path_log)
fh.setLevel(logging.DEBUG)
# create formatter
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
# add formatter to ch
#ch.setFormatter(formatter)
fh.setFormatter(formatter)
# add ch to logger
#logger.addHandler(ch)
logger.addHandler(fh)

def get_politicas():
    pass
    politicas={}
    if os.path.exists(file_politicas_json):
        pass
        with open(file_politicas_json, "r") as read_file:
            politicas = json.load(read_file)
        #leo el archivo y lo guardo en politicas_old
    return politicas

def conexion_bd(funcion):
    def nueva_funcion(*args,**kargs):
        try:
            #print("===================================================================")
            #conn=mysql.connector.connect(user='root',password='edraed.123',host='localhost',database='zabbix')
            logger.debug("Conexion a la BD")
            #path_database=os.path.join(os.path.join(dir_base,'mopso'),'db.sqlite3')
            #logger.debug("BD: {}".format(path_database))
            conn = psycopg2.connect("dbname=mopso user=mopso password=mopso host=mopso1.3_db port=5432")
            #conn = sqlite3.connect(path_database)
            logger.debug("Conexion exitosa")
            logger.debug("Procedemos a ejecutar la accion")
            r=funcion(conn,*args,**kargs)
            #print("===================================================================")
        except Exception as e :
            logger.debug("Ocurrio un error {}".format(e))
        else:
          conn.close()
        return r
    return nueva_funcion


@conexion_bd
def get_task_in_db(conn='',task=''):
    logger.debug("Iniciamos la Accion Consulta ")
    c = conn.cursor()
    logger.debug("declaracion del cursor de DB exitosa")
    logger.debug("construccion de la query")
    query = ("SELECT id FROM gestiontarea_tarea WHERE nombre='{tarea}'".format(tarea=task))
    logger.debug("la query a ejecutar es: {}".format(query))
    logger.debug("procedemos a la ejecucion")
    c.execute(query)
    logger.debug("ejecucion de la query fue exitosa")
    logger.debug("procedemos a almacenar datos en ram")
    salida=c.fetchone()
    #conn.commit()
    logger.debug("Retornamos los valores:{}".format(salida))
    return salida


@conexion_bd
def add_tareas(conn=''):
    pass
    logger.debug("(ADD_TAREAS) - INIT!!! ")
    c = conn.cursor()
    logger.debug("(ADD_TAREAS) - declaracion del cursor de DB exitosa")
    #campos gestiontarea_tarea
    #nombre=models.CharField(max_length=200)
    #descripcion=models.CharField(max_length=200)
    #test_conexion
    #
    for t in tareas:
        pass
        logger.debug("Construccion de la query ")
        query = "INSERT INTO gestiontarea_tarea (nombre,descripcion) VALUES ('{nombre}','{descripcion}');".format(nombre=t[0],descripcion=t[1])
        logger.debug("se va a ejecutar la siguiente query: {}".format(query))
        logger.debug("procedemos a la ejecucion")
        c.execute(query)
        logger.debug("ejecucion exitosa")
        logger.debug("procedemos a aplicar los cambios en BD")
        conn.commit()
        logger.debug("cambios aplicados satisfactoriamente")
    """
    logger.debug("Construccion de la query ")
    query = "INSERT INTO gestiontarea_tarea (nombre,descripcion) VALUES ('{nombre}','{descripcion}');".format(nombre='test_conexion',descripcion='Test de conectividad a los server')
    logger.debug("se va a ejecutar la siguiente query: {}".format(query))
    logger.debug("procedemos a la ejecucion")
    c.execute(query)
    logger.debug("ejecucion exitosa")
    logger.debug("procedemos a aplicar los cambios en BD")
    conn.commit()
    logger.debug("cambios aplicados satisfactoriamente")

    logger.debug("Construccion de la query ")
    query = "INSERT INTO gestiontarea_tarea (nombre,descripcion) VALUES ('{nombre}','{descripcion}');".format(nombre='sinc_users',descripcion='Sincronizacion de usuarios de OS')
    logger.debug("se va a ejecutar la siguiente query: {}".format(query))
    logger.debug("procedemos a la ejecucion")
    c.execute(query)
    logger.debug("ejecucion exitosa")
    logger.debug("procedemos a aplicar los cambios en BD")
    conn.commit()
    logger.debug("cambios aplicados satisfactoriamente")

    logger.debug("Construccion de la query ")
    query = "INSERT INTO gestiontarea_tarea (nombre,descripcion) VALUES ('{nombre}','{descripcion}');".format(nombre='sinc_users_db',descripcion='Sincronizacion de usuarios de DB')
    logger.debug("se va a ejecutar la siguiente query: {}".format(query))
    logger.debug("procedemos a la ejecucion")
    c.execute(query)
    logger.debug("ejecucion exitosa")
    logger.debug("procedemos a aplicar los cambios en BD")
    conn.commit()
    logger.debug("cambios aplicados satisfactoriamente")
    """
    print("ADD - TAREAS COMPLETE!!!")
    return "OK"


@conexion_bd
def add_user(conn=''):
    pass
    logger.debug("(ADD_USER) - INIT!!! ")
    c = conn.cursor()
    logger.debug("(ADD_USER) - declaracion del cursor de DB exitosa")

    logger.debug("Construccion de la query ")
    query = "INSERT INTO gestiontarea_usuario (nombre,apellido,departamento) VALUES ('{nombre}','{apellido}','{departamento}');".format(nombre='mopso',apellido='mopso',departamento='mopso')
    logger.debug("se va a ejecutar la siguiente query: {}".format(query))
    logger.debug("procedemos a la ejecucion")
    c.execute(query)
    logger.debug("ejecucion exitosa")
    logger.debug("procedemos a aplicar los cambios en BD")
    conn.commit()
    logger.debug("cambios aplicados satisfactoriamente")
    print("ADD USER COMPLETE!")
    return "OK"

@conexion_bd
def add_group(conn=''):
    pass
    logger.debug("(ADD_GROUP) - INIT!!! ")
    c = conn.cursor()
    logger.debug("(ADD_GROUP) - declaracion del cursor de DB exitosa")

    logger.debug("Construccion de la query ")
    query = "INSERT INTO auth_group (name) VALUES ('{name}');".format(name='mopso')
    logger.debug("se va a ejecutar la siguiente query: {}".format(query))
    logger.debug("procedemos a la ejecucion")
    c.execute(query)
    logger.debug("ejecucion exitosa")
    logger.debug("procedemos a aplicar los cambios en BD")
    conn.commit()
    logger.debug("cambios aplicados satisfactoriamente")
    print("ADD GROUP COMPLETE!")
    return "OK"

@conexion_bd
def add_usergroup(conn=''):
    pass
    logger.debug("(ADD_USERGROUP) - INIT!!! ")
    c = conn.cursor()
    logger.debug("(ADD_USERGROUP) - declaracion del cursor de DB exitosa")
    logger.debug("Construccion de la query ")
    query = "INSERT INTO auth_user_groups (user_id,group_id) VALUES ((select id from auth_user where username = '{username}'),(select id from auth_group where name = '{empresa}'));".format(username='mopsoadmin',empresa='mopso')
    logger.debug("se va a ejecutar la siguiente query: {}".format(query))
    logger.debug("procedemos a la ejecucion")
    c.execute(query)
    logger.debug("ejecucion exitosa")
    logger.debug("procedemos a aplicar los cambios en BD")
    conn.commit()
    logger.debug("cambios aplicados satisfactoriamente")
    print("ADD USERGROUP COMPLETE!")
    return "OK"

@conexion_bd
def add_rol(conn=''):
    pass
    logger.debug("(ADD_ROL) - INIT!!! ")
    c = conn.cursor()
    logger.debug("(ADD_ROL) - declaracion del cursor de DB exitosa")

    logger.debug("Construccion de la query ")
    query = "INSERT INTO gestionusuario_rol (rol,usuario_id) VALUES ('{rol}', (select id from auth_user where username like '{username}'));".format(rol='Ad',username='mopsoadmin')
    logger.debug("se va a ejecutar la siguiente query: {}".format(query))
    logger.debug("procedemos a la ejecucion")
    c.execute(query)
    logger.debug("ejecucion exitosa")
    logger.debug("procedemos a aplicar los cambios en BD")
    conn.commit()
    logger.debug("cambios aplicados satisfactoriamente")
    print("ADD ROL COMPLETE!")
    return "OK"

@conexion_bd
def add_politicas(conn=''):
    pass
    logger.debug("(ADD_POLITICAS) - INIT!!! ")
    c = conn.cursor()
    logger.debug("(ADD_POLITICAS) - declaracion del cursor de DB exitosa")
    pols=get_politicas()
    for p in pols:
        logger.debug("Construccion de la query ")
        query = "INSERT INTO gestionevaluacion_politica (nombre_politica,nombre_chequeo,chequeo_estado,chequeo_peso,chequeo_valor,chequeo_cod) VALUES ('{nombre_politica}','{nombre_chequeo}','true',100,'','{chequeo_cod}');".format(nombre_politica=clean_string(p["nombre_politica"]),nombre_chequeo=clean_string(p["alias_chequeo"]),chequeo_cod=p["chequeo_cod"])
        logger.debug("se va a ejecutar la siguiente query: {}".format(query))
        logger.debug("procedemos a la ejecucion")
        c.execute(query)
        logger.debug("ejecucion exitosa")
        logger.debug("procedemos a aplicar los cambios en BD")
        conn.commit()
    logger.debug("cambios aplicados satisfactoriamente")
    print("ADD POLITICAS COMPLETE!")
    return "OK"

@conexion_bd
def add_semaforo(conn=''):
    pass
    logger.debug("(ADD_SEMAFORO) - INIT!!! ")
    c = conn.cursor()
    logger.debug("(ADD_SEMAFORO) - declaracion del cursor de DB exitosa")
    modulos=["so","bd","ep"]
    for modulo in modulos:
        logger.debug("Construccion de la query ")
        query = "INSERT INTO cuadromando_semaforo (modulo,umbral_verde,umbral_amarillo) VALUES ('{modulo}',60,40);".format(modulo=modulo)
        logger.debug("se va a ejecutar la siguiente query: {}".format(query))
        logger.debug("procedemos a la ejecucion")
        c.execute(query)
        logger.debug("ejecucion exitosa")
        logger.debug("procedemos a aplicar los cambios en BD")
        conn.commit()
    logger.debug("cambios aplicados satisfactoriamente")
    print("ADD SEMAFORO COMPLETE!")
    return "OK"

def migrate_django():
    pass
    path_manage=os.path.join(os.path.join(dir_base,'mopso'),'manage.py')
    print("path_manage {}".format(path_manage))
    comando="/usr/bin/python3 {path_manage} migrate".format(path_manage=path_manage)
    proceso=subprocess.run(comando,stdout=subprocess.PIPE,stderr=subprocess.PIPE,shell=True)
    if proceso.returncode == 0:
        print("OK migrate")
    else:
        print("NOK")
        if re.search('UNIQUE constraint failed: auth_user.username',str(proceso.stderr)):
            print("NOK - Usuario ya Existe")

def migrations_django():
    pass
    path_manage=os.path.join(os.path.join(dir_base,'mopso'),'manage.py')
    comando="/usr/bin/python3  {path_manage} makemigrations".format(path_manage=path_manage)
    proceso=subprocess.run(comando,stdout=subprocess.PIPE,stderr=subprocess.PIPE,shell=True)
    if proceso.returncode == 0:
        print("OK migrations")
    else:
        print("NOK")
        if re.search('UNIQUE constraint failed: auth_user.username',str(proceso.stderr)):
            print("NOK - Usuario ya Existe")

def create_useradmin():
    pass
    path_manage=os.path.join(os.path.join(dir_base,'mopso'),'manage.py')
    comando="/usr/bin/python3  {path_manage} createsuperuser --username mopsoadmin --email vapc03@gmail.com --noinput".format(path_manage=path_manage)
    proceso=subprocess.run(comando,stdout=subprocess.PIPE,stderr=subprocess.PIPE,shell=True)
    if proceso.returncode == 0:
        print("OK create ADMIN")
    else:
        #print("NOK")
        if re.search('UNIQUE constraint failed: auth_user.username',str(proceso.stderr)):
            print("NOK - Usuario ya Existe")



def change_password_user():
    pass
    path_manage=os.path.join(os.path.join(dir_base,'mopso'),'manage.py')
    comando="/usr/bin/python3  {path_manage} changepassword  mopsoadmin".format(path_manage=path_manage)
    #proceso=subprocess.Popen(comando,stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE,shell=True)
    proceso=subprocess.run(comando)
    #proceso.stdin.write(b'Clave.23\n')
    #proceso.communicate(input=b'Clave.23')

def find_directory(d_base,dir):
    list_dir=[]
    list_dir_temp=[]
    for d in os.listdir(d_base):
        if d == dir :
            list_dir.append(os.path.join(d_base,d))
        else:
            if os.path.isdir(os.path.join(d_base,d)):
                pass
                abuscar=os.path.join(d_base,d)
                list_dir_temp.append(find_directory(abuscar,dir))
    if list_dir == [] and list_dir_temp == []:
        return 'vacio'
    else:
        if len(list_dir_temp) != 0:
            for i in list_dir_temp:
                if type(i) == list:
                    for j in i:
                        list_dir.append(j)
                else:
                    list_dir.append(i)
        for i in range(list_dir.count('vacio')):
            list_dir.remove('vacio')
        if list_dir == []:
            return 'vacio'
        else:
            return list_dir

def clean_proyecto():
    print("borro todo los archivos dentro de directorios __pycache__")
    for i in find_directory(dir_base,"__pycache__"):
        for f in os.listdir(i):
            if os.path.isfile(os.path.join(i,f)) and f != '__init__.py':
                os.remove(os.path.join(i,f))
    print("borro todos los archivos dentro de directorio migrations")
    for i in find_directory(dir_base,"migrations"):
        for f in os.listdir(i):
            if os.path.isfile(os.path.join(i,f)) and f != '__init__.py':
                os.remove(os.path.join(i,f))
    print("borro todos los archivos dentro de directorio dir_task_running ")
    for i in find_directory(dir_base,"dir_task_running"):
        for f in os.listdir(i):
            if os.path.isfile(os.path.join(i,f)) and f != '__init__.py' and not re.match(r'^\.',f):
                os.remove(os.path.join(i,f))
    print("borro todos los archivos dentro de directorio dir_task_new ")
    for i in find_directory(dir_base,"dir_task_new"):
        for f in os.listdir(i):
            if os.path.isfile(os.path.join(i,f)) and f != '__init__.py' and not re.match(r'^\.',f):
                os.remove(os.path.join(i,f))
    print("borro todos los archivos dentro de directorio resultados_tareas ")
    for i in find_directory(dir_base,"resultados_tareas"):
        for f in os.listdir(i):
            if os.path.isfile(os.path.join(i,f)) and f != '__init__.py' and not re.match(r'^\.',f):
                os.remove(os.path.join(i,f))
    print("borro todos los archivos dentro de directorio dir_data_raw ")
    for i in find_directory(dir_base,"dir_data_raw"):
        for f in os.listdir(i):
            if os.path.isfile(os.path.join(i,f)) and f != '__init__.py' and not re.match(r'^\.',f):
                os.remove(os.path.join(i,f))

if __name__ == '__main__':
    pass
    print(dir_base)
    #borro BD
    #DBNAME='db.sqlite3'
    #if os.path.isfile(os.path.join(os.path.join(dir_base,'mopso'),DBNAME)):
    #    print("borro {}".format(os.path.join(os.path.join(dir_base,'mopso'),DBNAME)))
    #    os.remove(os.path.join(os.path.join(dir_base,'mopso'),DBNAME))
    #borro migraciones y archivos .pyc
    clean_proyecto()
    # recreo la BD
    ## migrate
    print("ejecucion de migrate")
    migrate_django()
    ## makemigrations
    print("ejecucion de makemigrations")
    migrations_django()
    ## migrate
    print("ejecucion de migrate")
    migrate_django()
    #creacion de susperuser mopsoadmin
    print("creacion de administrador mopsoadmin")
    create_useradmin()
    #cambio de password
    #change_password_user()
    #agrego datos iniciales de las tablas Tarea , usuario y grupo
    print("se agrega usuario mopso en tabla usuario")
    add_user()
    print("se crea rol")
    add_rol()
    print("se agregan tareas bases")
    add_tareas()
    print("creacion de grupo mopso")
    add_group()
    print("agregar a mopsoadmin a grupo mopso")
    add_usergroup()
    print("se agregan las politicas")
    add_politicas()
    print("se agregan semaforos por modulos")
    add_semaforo()
