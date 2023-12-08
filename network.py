import socket
import pickle
from pickle import UnpicklingError
import tkinter
from typing import Union


class Network:
    def __init__(self, port: int, ip: str, my_id: str, first_obj: Union[bool, object] = False):
        """
        client side network
        :param port: port number
        :param ip: ip address of server
        :param my_id: identifier for network
        :param first_obj: optional object to pass to server on handshake
        """

        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server = ip #  socket.gethostbyname(socket.gethostname())
        self.port = port
        self.addr = (self.server, self.port)
        self.conn_status = self.connect(my_id)
        self.my_id = my_id
        print(self.conn_status)
        if first_obj:
            print('sending first object')
            self.send_obj(first_obj)

    # def get_pos(self):
    #     return self.pos

    def connect(self, my_id: str):
        try:
            self.client.connect(self.addr)
            self.send_text(my_id)
            print(self.addr)
            return self.receive()
        except socket.error as e:
            print(e)
        except EOFError as e:
            print(e)
            print('player already connected')
            del self

    def send_obj(self, obj: object) -> None:
        """
        send pickled object
        :param obj: object of any type
        :return:
        """
        try:
            b = pickle.dumps(obj)
            self.client.send(b)
            # return self.client.recv(2048).decode()
        except socket.error as e:
            print(e)

    def send_text(self, text: str) -> None:
        """
        send string
        :param text: string message
        :return:
        """
        print(text)
        try:
            self.client.sendall(text.encode())
        except socket.error as e:
            print(e)

    def receive(self) -> object:
        """
        receive and unpickle object of any type
        :return: object
        """
        data = self.client.recv(1048576)
        # print(data)
        try:
            return pickle.loads(data)
        except UnpicklingError:
            return data.decode("utf-8")
        except EOFError as e:
            print(e)
            return ''
        # except EOFError as e:
        #     print(e)


if __name__ == '__main__':
    n = Network(5554, socket.gethostbyname(socket.gethostname()), 'Logan')

    # n.send_obj('b')
    # n.client.send(str.encode("your mother"))
    # n.send_obj('waka waka')
