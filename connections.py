import socket
import json

def connect_to_server():
    """returns a socket connetction to the server"""
    return socket.create_connection(address=( "localhost", 8800))


def get_json_from_server(sckt):
    """reads json from the socket and returns a dict containing"""
    chunks = []
    while True:
        chunk = sckt.recv(4096)
        if not chunk:
            raise ConnectionError("Server closed connection")
        chunks.append(chunk)
        try:
            return json.loads(b"".join(chunks))
        except json.JSONDecodeError:
            continue


def send_json_to_server(sckt, dict_output):
    """takes dict, converts it to json and then to bytes and sends it"""
    text = json.dumps(dict_output) 
    data = text.encode("utf-8")
    sckt.sendall(data)