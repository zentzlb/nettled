import socket
import pickle
import time
from pickle import UnpicklingError
from _thread import *
import sys
from com import *


class Server:

    server = socket.gethostbyname(socket.gethostname())
    run = True
    conn_count = 0

    conn_ids = []

    subscriber = {}
    publisher = {}

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def __init__(self, port: int, max_conn_count: int = 4):

        self.port = port
        self.max_conn_count = max_conn_count

        try:
            self.s.bind((self.server, self.port))
        except socket.error as e:
            print(e)

        self.s.listen(2)
        print('waiting for connection, server started')

    def main(self) -> None:
        """
        look for new connections
        :return:
        """
        while self.run:
            try:
                if self.conn_count < self.max_conn_count and type(self.s) is socket.socket:
                    conn, addr = self.s.accept()
                    print(f"connected to: {addr}")
                    start_new_thread(self.threaded_client, (conn, ))
            except OSError as e:
                print(e)

    def close(self):
        """
        close server
        :return:
        """
        self.run = False
        self.s.close()
        # del self

    def threaded_client(self, conn: socket.socket) -> None:
        """
        make thread to handle interactions with connected client
        :param conn: client socket connection
        :return:
        """
        # conn.settimeout(1)
        conn_id = receive(conn)
        if conn_id in self.conn_ids:
            send_text(conn, 'player already connected')
            time.sleep(0.1)
            conn.close()
            return
        send_text(conn, "Connected")
        self.conn_ids.append(conn_id)
        self.conn_count += 1
        print(conn_id)
        print(self.conn_count)
        print(f"number of players: {self.conn_count}")

        while True:
            try:
                data = receive(conn)
                # print(data)
                if data:
                    self.subscriber[conn_id] = data
                #     pass
                    # print("Disconnected")
                    # break
                # else:
                b = pickle.dumps(self.publisher)
                print(b.__sizeof__())
                # print(b)
                conn.send(b)

            except socket.error as e:
                conn.close()
                print(e)
                break

        print('Lost Connection')
        # del player
        self.conn_count -= 1
        print(f"number of players: {self.conn_count}")
        conn.close()


if __name__ == '__main__':
    my_server = Server(5554)
    my_server.main()
