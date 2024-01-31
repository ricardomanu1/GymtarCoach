import requests

url = "http://ec2-16-170-250-70.eu-north-1.compute.amazonaws.com:5000/ejercicios"

try:
    # Realizar la solicitud GET a la URL
    response = requests.get(url)
    
    # Verificar si la solicitud fue exitosa (código de estado 200)
    if response.status_code == 200:
        # Obtener el contenido JSON como una lista de diccionarios
        usuarios_data = response.json()
        ids = [9,6,4,2,3]
        #usuarios_edades_especificas = [usuario for usuario in usuarios_data if usuario["u_age"] in [27, 32]]
        #u_names_edades_especificas = [usuario["u_name"] for usuario in usuarios_edades_especificas]
        ejercicios_seleccionados = [exercise for exercise in usuarios_data if exercise["e_id"] in ids]
        names,animations = zip(*[(exercise["e_name"],exercise["e_animation"]) for exercise in ejercicios_seleccionados])
        # Imprimir los valores de u_name
        print(names)
        print(animations)
        # Procesar cada diccionario en la lista
        for usuario in usuarios_data:
            u_id = usuario.get('u_id', 'N/A')
            u_name = usuario.get('u_name', 'N/A')
            u_lastname = usuario.get('u_lastname', 'N/A')
            u_email = usuario.get('u_email', 'N/A')
            u_age = usuario.get('u_age', 'N/A')
            u_rol = usuario.get('u_rol', 'N/A')

            # Hacer algo con la información, aquí se imprime en este ejemplo
            #print(f"ID: {u_id}, Nombre: {u_name}, Apellido: {u_lastname}, Email: {u_email}, Edad: {u_age}, Rol: {u_rol}")
    else:
        print(f"Error al hacer la solicitud. Código de estado: {response.status_code}")
except Exception as e:
    print(f"Error: {e}")
