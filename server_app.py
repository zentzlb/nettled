import tkinter
from tkinter import messagebox, Button, Tk, mainloop, Label, StringVar, simpledialog
import socket
from server import Server
import time
from _thread import *
from game_engine import Engine, Player
import pickle


class ServerApp:
    def __init__(self):
        self.port = 5554
        self.root = Tk()
        self.server = None
        self.run = False

    def update_count(self, var: StringVar):
        """
        updates player count variable
        :param var: player count variable
        :return:
        """
        print('thread working')
        # print(self.root.winfo_exists())
        while self.root.winfo_exists():
            if type(self.server) is Server:
                var.set(f'player count: {self.server.conn_count}')
            time.sleep(0.1)
        print('closing')

    def main_loop(self):
        self.run = True
        print('starting')
        if type(self.server) is Server:
            players = [player for player in self.server.subscriber.values()\
                       if type(player) is Player]
            print(players)
            engine = Engine()
            engine.start(5, 90, players)
            print(engine.status)
            while self.run:
                # print('working')
                for player_name in self.server.subscriber.keys():
                    # if player_name != '':
                    # print(player_name)
                    seq = self.server.subscriber[player_name]
                    if type(seq) is list:
                        engine.check_sequence(seq, engine.status['players'][player_name])
                engine.update()
                self.server.publisher = engine.status
                # print(self.server.publisher)
        return

    def change_port(self, port_var: tkinter.StringVar) -> None:
        """
        update port variable and port number
        :param port_var: port string variable
        :return:
        """
        self.port = simpledialog.askinteger("Input",
                                            "Enter Port Number",
                                            parent=self.root,
                                            minvalue=0,
                                            maxvalue=10000)
        port_var.set(f'port: {self.port}')

    def launch_server(self) -> None:
        """
        launches server
        :return:
        """
        # if type(self.server) is None:
        self.server = Server(self.port)
        start_new_thread(self.server.main, tuple())

    def start_game(self) -> None:
        """
        start server
        :return:
        """
        if not self.run:
            print(self.run)
            start_new_thread(self.main_loop, tuple())

    def close_server(self) -> None:
        """
        closes server
        :return:
        """
        self.run = False
        self.server.run = False
        # if type(self.server) is Server:
        #     self.server.close()
        #     self.server = None

    def main(self) -> None:
        """
        app main loop
        :return:
        """
        self.root.title('SERVER')
        self.root.geometry('250x150')

        text_var = StringVar()
        text_var.set(f"IP: {socket.gethostbyname(socket.gethostname())}")
        port_var = StringVar()
        port_var.set(f'port: {self.port}')
        count_var = StringVar()
        count_var.set('')

        start_new_thread(self.update_count, (count_var,))

        lbl1 = Label(master=self.root, textvariable=count_var)
        lbl1.grid(row=2, column=0)
        lbl2 = Label(master=self.root, textvariable=text_var)
        lbl2.grid(row=1, column=0)
        lbl3 = Label(master=self.root, textvariable=port_var)
        lbl3.grid(row=0, column=0)

        button1 = Button(text='Launch Server', command=lambda: self.launch_server(), width=15, height=1)
        button1.grid(row=1, column=1)

        button2 = Button(text='Change Port', command=lambda: self.change_port(port_var), width=15, height=1)
        button2.grid(row=0, column=1)

        button4 = Button(text='Start Game', command=lambda: self.start_game(), width=15, height=1)
        button4.grid(row=2, column=1)

        button3 = Button(text='Close Server', command=lambda: self.close_server(), width=15, height=1)
        button3.grid(row=3, column=1)

        mainloop()


if __name__ == '__main__':
    app = ServerApp()
    app.main()
