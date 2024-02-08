# coding=utf-8
import logging, time
import requests
import json
from websocket_server import WebsocketServer #pip install websocket_server

# Mantén un registro de los clientes conectados
connected_clients = {}
url_R = 'http://127.0.0.1:5005/webhooks/myio/webhook'

# Define callback functions for server events
def new_client(client, server):
    client_id = client['id']
    print(f"Client({client_id}) has joined.")
    
    # Agrega al cliente al registro
    connected_clients[client_id] = client

def client_left(client, server):
    client_id = client['id']
    print(f"Client({client_id}) disconnected")
    
    # Elimina al cliente del registro
    if client_id in connected_clients:
        del connected_clients[client_id]

def message_back(client, server, message):
    start_time = time.time()
    # Guarda el mensaje en json
    data = json.loads(message)
    # Tomamoes la respuesta
    respuesta = data['message']
    print(f"Message from client {client['id']}: {respuesta}")
    print(data)
    # Construimos el nuevo mensaje
    response = {
        "respuesta": f"{respuesta}"       
    }
    # El nuevo mensaje a JSON string
    response_json = json.dumps(response)

    if 'recipient' in data:
        recipient_id = data['recipient']
        if (recipient_id != 0):
            recipient = connected_clients.get(recipient_id)                   
            if recipient:
                # Send the JSON response to the recipient
                print(f"Mensaje del cliente {client['id']}(Rasa): '{respuesta}' para el cliente {recipient_id}(Unreal)")
                server.send_message(recipient, response_json)
        else:
            print("Unreal ha enviado algo")
            print(data)
            r = requests.post(url_R, json=data)
    print("--- %s seconds (server) ---" % (time.time() - start_time))

def run_websocket_server():
    # Create a new websocket server object
    server = WebsocketServer(port=5059, host='127.0.0.1')

    # Set callback functions for server events
    server.set_fn_new_client(new_client)
    server.set_fn_client_left(client_left)
    server.set_fn_message_received(message_back)

    # Run the server indefinitely
    server.run_forever()

if __name__ == "__main__":
    run_websocket_server()

