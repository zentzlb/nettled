from tkinter import messagebox, Button, Tk, mainloop, Label, StringVar, simpledialog
import socket


def launch_server():
    pass


def change_port(port_var):
    port_var.set(f'port: {simpledialog.askinteger("Input", "Enter Port Number", parent=root, minvalue=0, maxvalue=10000)}')

port = 5555
root = Tk()
root.title('SERVER')
root.geometry('300x60')

text_var = StringVar()
text_var.set(f"IP: {socket.gethostbyname(socket.gethostname())}")
port_var = StringVar()
port_var.set(f'port: {port}')

lbl = Label(master=root, textvariable=text_var)
lbl.grid(row=0, column=0)
lbl = Label(master=root, textvariable=port_var)
lbl.grid(row=1, column=0)
button1 = Button(text='Launch Server', command=lambda: launch_server())
button1.grid(row=0, column=1)
button1 = Button(text='Change Port', command=lambda: change_port(port_var))
button1.grid(row=1, column=1)


mainloop()
