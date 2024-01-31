import mysql.connector

class database:
    def __init__(self):
        # Establece los detalles de conexión
        self.config = {
            'user': 'root',
            'password': 'gymtar',
            'host': '127.0.0.1',
            'database': 'gymtar',
            'port': 3306,
            'raise_on_warnings': True
        }
        self.conn = None
        self.cursor = None

    def connection(self):
        try:
            print("intentando conectar")
            # Crea una conexión a la base de datos
            self.conn = mysql.connector.connect(**self.config)
            # Crea un cursor para ejecutar consultas
            self.cursor = self.conn.cursor()
        except mysql.connector.Error as error:
            print(f'Error al conectar a la base de datos: {error}')

    def disconnection(self):
        # Cierra el cursor
        self.cursor.close()
        if self.conn.is_connected():
            self.conn.close()

    def login(self,id,password):
        if id is None:
            print("No hay datos")
            return
        else:
            #print("hay datos")
            # Ejecutar una consulta SELECT
            consulta = "SELECT u_name,u_rol FROM usuarios where u_id = %s"
            # Ejecuta la consulta con el parámetro pasado
            self.cursor.execute(consulta, (id,))
            # Obtiene los resultados
            result = self.cursor.fetchone()
            contenido_user = {
                'name': "",
                'rol': ""
            }
            if result:
                contenido_user['name'] = str(result[0])
                contenido_user['rol'] = str(result[1])
                return contenido_user
            else:
                return

    def select_routine(self,id,date):
        if id is None:
            print("No hay datos")
            return
        else:
            #print("hay datos")
            # Ejecutar una consulta SELECT
            consulta = "SELECT r_exercises,r_repetitions,r_time FROM rutina where r_id = %s AND r_date =%s"
            # Ejecuta la consulta con el parámetro pasado
            self.cursor.execute(consulta, (id,date))
            # Obtiene los resultados
            result = self.cursor.fetchone()
            contenido_user = {
                'ejercicios': "",
                'repeticiones': "",
                'tiempos': ""
            }
            if result:
                contenido_user['ejercicios'] = str(result[0])
                contenido_user['repeticiones'] = str(result[1])
                contenido_user['tiempos'] = str(result[2])
                return contenido_user
            else:
                return

    def select_exercise(self,id):
        if id is None:
            print("No hay datos")
            return
        else:
            #print("hay datos")
            # Ejecutar una consulta SELECT
            consulta = "SELECT e_name FROM ejercicios where e_id = %s"
            # Ejecuta la consulta con el parámetro pasado
            self.cursor.execute(consulta, (id,))
            # Obtiene los resultados
            result = self.cursor.fetchone()
            contenido_user = {
                'name': ""
            }
            if result:
                contenido_user['name'] = str(result[0])
                return contenido_user
            else:
                return
        

    def select_exercises(self,ids):
        if ids is None:
            print("No hay datos")
            return
        else:
            print("llega "+str(tuple(ids)))
            query = "SELECT e_name FROM ejercicios WHERE e_id IN (%s)"
            placeholders = ', '.join(['%s'] * len(ids))  # Crear marcadores de posición
            query = query % placeholders
            self.cursor.execute(query, ids)
            result = self.cursor.fetchall()
            # Obtiene los resultados            
            if result:
                lista_plana = [tupla[0] for tupla in result]
                return lista_plana
            else:
                return
            

    def select_animation(self,id):
        if id is None:
            print("No hay datos")
            return
        else:
            #print("hay datos")
            # Ejecutar una consulta SELECT
            consulta = "SELECT e_animation FROM ejercicios where e_id = %s"
            # Ejecuta la consulta con el parámetro pasado
            self.cursor.execute(consulta, (id,))
            # Obtiene los resultados
            result = self.cursor.fetchone()
            contenido_user = {
                'name': ""
            }
            if result:
                contenido_user['name'] = str(result[0])
                return contenido_user
            else:
                return
            