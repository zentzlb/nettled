import socket
import pickle
from pickle import UnpicklingError


def receive(conn: socket.socket) -> object:
    """
    :param conn: connected client
    :return: object
    """
    data = conn.recv(1048576)
    try:
        return pickle.loads(data)
    except UnpicklingError:
        return data.decode("utf-8")
    except EOFError:
        print('EOF error, get help')


def send_text(conn: socket.socket, text: str) -> None:
    """
    send string
    :param conn: connected client
    :param text: string message
    :return:
    """
    try:
        conn.sendall(text.encode())
    except socket.error as e:
        print(e)


def send_obj(conn: socket.socket, obj: object) -> None:
    """
    send pickled object
    :param conn: connected client
    :param obj: object of any type
    :return:
    """
    try:
        b = pickle.dumps(obj)
        b.__sizeof__()
        conn.send(b)
    except socket.error as e:
        print(e)


"""
data = conn.recv(2048)

                try:
                    keys = pickle.loads(data)
                    print(keys)
                    # player.scoot(keys)
                except UnpicklingError:

                    reply = data.decode("utf-8")
                    print(reply)
"""
