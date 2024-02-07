import mysql.connector
import requests
from datetime import datetime

class database:

    def login(self,id,password):
        url = f"http://ec2-16-170-250-70.eu-north-1.compute.amazonaws.com:5000/usuarios?id={id}"
        try:
            response = requests.get(url)
            if response.status_code == 200:        
                if response.content:                    
                    usuario_data = response.json()   
                    usuario_data = usuario_data[0]
                    contenido_user = {
                        'name': "",
                        'rol': ""
                    }                    
                    contenido_user['name'] = usuario_data.get('u_name', 'N/A')
                    contenido_user['rol'] = usuario_data.get('u_rol', 'N/A')    
                    return contenido_user
                else:
                    return
            else:
                print(f"Error al hacer la solicitud. Código de estado: {response.status_code}")
        except Exception as e:
            print(f"Error: {e}")
        return

    def select_routine(self,id,date):
        print(date)
        url = f"http://ec2-16-170-250-70.eu-north-1.compute.amazonaws.com:5000/sesion?id={id}"
        try:
            response = requests.get(url)
            if response.status_code == 200:        
                if response.content:
                    sesion_data = response.json() 
                    sesion_seleccionada = [sesion for sesion in sesion_data if  str(datetime.strptime(sesion.get("s_date"), '%a, %d %b %Y %H:%M:%S %Z').date()) == date]                     
                    if sesion_seleccionada:
                        sesion_seleccionada = sesion_seleccionada[0]
                        contenido_user = {
                            'ejercicios': "",
                            'repeticiones': "",
                            'tiempos': ""
                        }
                        contenido_user['ejercicios'] = sesion_seleccionada.get('s_exercises', 'N/A')
                        contenido_user['repeticiones'] = sesion_seleccionada.get('s_repetitions', 'N/A')
                        contenido_user['tiempos'] = sesion_seleccionada.get('s_time', 'N/A')
                        print(f"Ejercicios: {contenido_user['ejercicios']}, Repeticiones: {contenido_user['repeticiones']}, Tiempos: {contenido_user['tiempos']}")
                        return contenido_user                    
                else:
                    return
            else:
                print(f"Error al hacer la solicitud. Código de estado: {response.status_code}")
        except Exception as e:
            print(f"Error: {e}")
        return

    def select_exercise(self,id):
        url = f"http://ec2-16-170-250-70.eu-north-1.compute.amazonaws.com:5000/ejercicio?id={id}"
        try:
            response = requests.get(url)
            if response.status_code == 200:        
                if response.content:
                    ejercicio_data = response.json() 
                    ejercicio_data = ejercicio_data[0]
                    contenido_user = {
                        'name': ""
                    }
                    contenido_user['name'] = ejercicio_data.get('e_name', 'N/A')
                    #print(f"Ejercicio sql: {contenido_user['name']}")
                    return contenido_user
                else:
                    return
            else:
                print(f"Error al hacer la solicitud. Código de estado: {response.status_code}")
        except Exception as e:
            print(f"Error: {e}")
        return        
    #### Modificar para que tambien saque las animaciones
    def select_exercises(self,ids):
        url = f"http://ec2-16-170-250-70.eu-north-1.compute.amazonaws.com:5000/ejercicios"
        try:
            response = requests.get(url)
            if response.status_code == 200:        
                if response.content:
                    ejercicios_data = response.json() 
                    ejercicios_seleccionados = sorted([exercise for exercise in ejercicios_data if exercise["e_id"] in ids], key=lambda x: ids.index(x["e_id"]))
                    names,animations = zip(*[(exercise["e_name"],exercise["e_animation"]) for exercise in ejercicios_seleccionados])
                    return names,animations
                else:
                    return
            else:
                print(f"Error al hacer la solicitud. Código de estado: {response.status_code}")
        except Exception as e:
            print(f"Error: {e}")
        return                  

    def select_animation(self,id):
        url = f"http://ec2-16-170-250-70.eu-north-1.compute.amazonaws.com:5000/ejercicio?id={id}"
        try:
            response = requests.get(url)
            if response.status_code == 200:        
                if response.content:
                    ejercicio_data = response.json() 
                    ejercicio_data = ejercicio_data[0]
                    contenido_user = {
                        'name': ""
                    }
                    contenido_user['name'] = ejercicio_data.get('e_animation', 'N/A')
                    #print(f"animacion: {contenido_user['name']}")
                    return contenido_user
                else:
                    return
            else:
                print(f"Error al hacer la solicitud. Código de estado: {response.status_code}")
        except Exception as e:
            print(f"Error: {e}")
        return        
            