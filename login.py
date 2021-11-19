from tkinter import *
from PIL import ImageTk
from tkinter import messagebox
import mysql.connector

root=Tk()
root.title="LOGIN"
root.geometry("1200x700")
root.resizable(False,False)

varUserName = StringVar()
varPassword = StringVar()

image_bg = ImageTk.PhotoImage(file="images/background.png")
label = Label(root,image=image_bg)
label.pack()

frame = Frame(root,)
frame.place(x=390,y=170,width=400,height=450)

f = 'Time',14

def login():
    db =mysql.connector.connect(host ="localhost", user ="root", password ="", db ="quanly")
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
def validate():
    name = varUserName.get()
    password = varPassword.get()
    if name == "":
        messagebox.showinfo("Thông báo !","Tên đăng nhập phải nhập !")
        username_entry.focus()
        return
    if len(name) <= 3:
        messagebox.showinfo("Thông báo !", "Tên đăng nhập qúa ngắn !")
        username_entry.focus()
        return
    if password == "":
        messagebox.showinfo("Thông báo !","Mật khẩu phải nhập")
        password_entry.focus()
        return
    if len(password) <=7:
        messagebox.showinfo("Thông báo !", "Mật khẩu qúa ngắn !")
        password_entry.focus()
        return
    login()

username_lebel = Label(frame,text="Tên tài khoản",font = f, bg='white',fg='gray')
username_lebel.place(x=80,y=50)
username_entry = Entry(frame,font=f,textvariable= varUserName)
username_entry.place(x=80,y=100,width=250)

password_lebel = Label(frame,text="Mặt khẩu",font = f, bg='white',fg='gray')
password_lebel.place(x=80,y=170)
password_entry = Entry(frame,font=f,show="•",textvariable= varPassword)
password_entry.place(x=80,y=220,width=250)

login_btn= Button(frame,text="Đăng nhập",font = f,activebackground="#00FF66",activeforeground="white",fg='gray',command=validate)
login_btn.place(x=80,y=290,width=250)

register_btn= Button(frame,text="Đăng ký",font = f,activebackground="#00FF66",activeforeground="white",fg='gray')
register_btn.place(x=80,y=360,width=250)
root.mainloop()