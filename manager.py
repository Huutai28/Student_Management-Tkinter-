import tkinter as tk
from tkinter import *
from tkinter import messagebox
import MySQLdb


root = tk.Tk()
root.title('LOGIN')
root.geometry('400x220')
root.config(bg='white')
root.resizable(False,False)

f = ('Time',14)

varUserName = StringVar()
varPassword = StringVar()


LUserName= Label(root,text='User Name',font=f).place(x=40,y=40)
LPassword= Label(root,text='Password',font=f).place(x=40,y=100)

txtUserName= Entry(root,font=f,textvariable= varUserName)
txtUserName.place(x= 150,y=40)
txtPassword= Entry(root,font=f,textvariable= varPassword)
txtPassword.place(x= 150,y=100)
def validate():
    name = varUserName.get()
    password = varPassword.get()
    if name == "":
        messagebox.showinfo("Thông báo !","Tên đăng nhập phải nhập !")
        txtUserName.focus()
        return
    if len(name) <= 3:
        messagebox.showinfo("Thông báo !", "Tên đăng nhập qúa ngắn !")
        txtUserName.focus()
        return
    if password == "":
        messagebox.showinfo("Thông báo !","Mật khẩu phải nhập")
        txtPassword.focus()
        return
    if len(password) <=7:
        messagebox.showinfo("Thông báo !", "Mật khẩu qúa ngắn !")
        txtPassword.focus()
        return
    login()

def login():
    db = MySQLdb.connect("localhost", "root", "", "quanly")
    cursor = db.cursor()
    cursor.execute("SELECT * FROM `user` WHERE username = '" + varUserName.get() + "' AND password = '" + varPassword.get() + "';")
    row = cursor.fetchall()

    if row:
        root.destroy()
        import TreeViewCRUD
    else:
        messagebox.showinfo("Thông báo !","Tên tài khoản hoặc mặt khẩu không đúng !")
        varUserName.set("")
        varPassword.set("")
def register():
    root.destroy()
    import Register
btnLogin = Button(root,font=f,text='Login',command=validate).place(x=60,y=160)
btnRegister = Button(root,font=f,text='Register',command=register).place(x=220,y=160)
root.mainloop()
