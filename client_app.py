import tkinter
from tkinter import messagebox, Button, Tk, mainloop, Label, \
    StringVar, simpledialog, colorchooser, ttk as TKK
import socket
from server import Server
import random as rnd
from client import LocalState, Engine, Player
from _thread import *
import socket
from network import Network


class ClientApp:
    def __init__(self):
        self.port = 5554
        self.root = Tk()
        self.server = None
        self.name = f'player {rnd.randint(100, 999)}'
        self.color = (rnd.randint(0, 200), rnd.randint(0, 200), rnd.randint(0, 200))
        self.width = 700
        self.height = 600
        self.ip = socket.gethostbyname(socket.gethostname())

        self.root.title('Nettled')
        self.root.geometry('250x160')

        self.ip_var = StringVar()
        self.ip_var.set(f"IP: {socket.gethostbyname(socket.gethostname())}")

        self.port_var = StringVar()
        self.port_var.set(f'port: {self.port}')

        self.count_var = StringVar()
        self.count_var.set('')

        self.name_var = StringVar()
        self.name_var.set(self.name)

        self.lbl1 = Label(master=self.root, textvariable=self.name_var)
        self.lbl1.grid(row=2, column=0)
        # self.lbl1 = Label(master=self.root, textvariable=self.count_var)
        # self.lbl1.grid(row=2, column=0)
        self.lbl2 = Label(master=self.root, textvariable=self.ip_var)
        self.lbl2.grid(row=1, column=0)
        self.lbl3 = Label(master=self.root, textvariable=self.port_var)
        self.lbl3.grid(row=0, column=0)

        self.port_button = Button(text='Change Port',
                                  command=lambda:
                                  self.change_port(self.port_var),
                                  width=15,
                                  height=1)
        self.port_button.grid(row=0, column=1)

        self.ip_button = Button(text='Change IP',
                                command=lambda:
                                self.change_ip(self.ip_var),
                                width=15,
                                height=1)
        self.ip_button.grid(row=1, column=1)

        self.launch_button = Button(text='Change Name',
                                    command=lambda:
                                    self.change_name(self.name_var),
                                    width=15,
                                    height=1)
        self.launch_button.grid(row=2, column=1)

        self.launch_button = Button(text='Pick Color',
                                    command=lambda:
                                    self.change_color(),
                                    width=15,
                                    height=1)
        self.launch_button.grid(row=3, column=1)

        self.launch_button = Button(text='Launch Game',
                                    command=lambda:
                                    self.launch_client(),
                                    width=15,
                                    height=1)
        self.launch_button.grid(row=4, column=1)

        # button3 = Button(text='Close Server', command=lambda: self.close_server(), width=15, height=1)
        # button3.grid(row=2, column=1)

        self.gamemode_dropdown = TKK.Combobox(state='readonly',
                                              values=['single player', 'multiplayer'],
                                              width=15)
        self.gamemode_dropdown.set('single player')
        self.gamemode_dropdown.grid(row=5, column=1)

    def get_status(self, ls: LocalState):
        """
        get games status from network object
        :param ls: local state object
        :return:
        """
        while True:
            status = ls.network.receive()
            print(status)
            if type(status) is dict and 'grid' in status:

                ls.engine.status = status
                if len(ls.buttons) == 0:
                    ls.make_buttons(ls.engine.status['grid'])
            # else:
            #     break

    def change_port(self, port_var: tkinter.StringVar) -> None:
        """
        update port variable and port number
        :param port_var: port string variable
        :return:
        """
        port = simpledialog.askinteger("Input", "Enter Port Number",
                                       parent=self.root,
                                       minvalue=0,
                                       maxvalue=10000,
                                       initialvalue=self.port)
        if port:
            self.port = port
            port_var.set(f'port: {self.port}')

    def change_ip(self, ip_var: tkinter.StringVar) -> None:
        """
        update IP variable and ip number
        :param ip_var: port string variable
        :return:
        """
        ip = simpledialog.askstring("Input", "Enter IP Address", parent=self.root, initialvalue=self.ip)
        if ip:
            self.ip = ip
            ip_var.set(f'IP: {self.ip}')

    def change_name(self, name_var: tkinter.StringVar) -> None:
        """
        update IP variable and ip number
        :param name_var: player name
        :return:
        """
        name = simpledialog.askstring("Input", "Enter Player Name", parent=self.root, initialvalue=self.name)
        if name:
            self.name = name
            name_var.set(f'IP: {self.name}')

    def change_color(self) -> None:
        """
        change player color
        :return:
        """
        color = colorchooser.askcolor(title="Choose player color")
        if color:
            self.color = color[0]

    def launch_client(self) -> None:
        """
        launches client
        :return:
        """
        # if type(self.server) is None:
        player = Player(self.name, self.color)
        engine = Engine()

        if self.gamemode_dropdown.get() == 'single player':
            ls = LocalState(self.width, self.height, player, engine)
            engine.start(5, 90, [player])
            ls.game_loop(engine)

        else:
            ls = LocalState(self.width,
                            self.height,
                            player,
                            engine,
                            Network(self.port, self.ip, player.name, player))
            engine.run = True
            start_new_thread(self.get_status, (ls,))
            ls.game_loop(engine)

        # self.server = Server(self.port)
        # start_new_thread(self.server.main, tuple())

    def main(self) -> None:
        """
        app main loop
        :return:
        """

        mainloop()


if __name__ == '__main__':
    app = ClientApp()
    app.main()
