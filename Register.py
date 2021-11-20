from tkinter import *
from PIL import ImageTk
from tkinter.messagebox import askyesno
from tkinter import messagebox
import mysql.connector

root=Tk()
root.title="LOGIN"
root.geometry("1200x700")
root.resizable(False,False)

f = ('Time',14)

varUserName = StringVar()
varPassword = StringVar()
varEmail = StringVar()

image_bg = ImageTk.PhotoImage(file="images/background.png")
label = Label(root,image=image_bg)
label.pack()

frame = Frame(root,)
frame.place(x=390,y=170,width=420,height=400)

LUserName = Label(frame,text="Tên tài khoản",font = f, bg='white',fg='gray').place(x=40, y=40)
LPassword = Label(frame,text="Mặt khẩu",font = f, bg='white',fg='gray').place(x=40, y=100)
LEmail = Label(frame, text='Email', font=f, bg='white',fg='gray').place(x=40, y=160)

txtUserNameRegister = Entry(frame, font=f, textvariable=varUserName)
txtUserNameRegister.place(x=180, y=40)
txtPasswordRegister = Entry(frame,show="•", font=f,textvariable=varPassword)
txtPasswordRegister.place(x=180, y=100)
txtEmailRegister = Entry(frame, font=f,textvariable=varEmail)
txtEmailRegister.place(x=180, y=160)

def validate():
    name = varUserName.get()
    password = varPassword.get()
    email = varEmail.get()

    if name == "":
        messagebox.showinfo("Thông báo !", "Tên đăng nhập phải nhập !")
        txtUserNameRegister.focus()
        return
    if len(name) <= 3:
        messagebox.showinfo("Thông báo !", "Tên đăng nhập qúa ngắn !")
        txtUserNameRegister.focus()
        return
    if password == "":
        messagebox.showinfo("Thông báo !", "Mật khẩu phải nhập")
        txtPasswordRegister.focus()
        return
    if len(password) <= 7:
        messagebox.showinfo("Thông báo !", "Mật khẩu qúa ngắn !")
        txtPasswordRegister.focus()
        return
    if email == "":
        messagebox.showinfo("Thông báo !", "Mật khẩu qúa ngắn !")
        txtEmailRegister.focus()
        return
    Register()
def Register():
    db = mysql.connector.connect(host ="localhost", user ="root", password ="",  db ="quanly")
    cursor = db.cursor()
    cursor.execute("INSERT INTO `user` (`username`, `password`, `email`) VALUES ('" + varUserName.get() + "', '" + varPassword.get() +"', '" + varEmail.get() +"');")
    db.commit()
    answer = askyesno(title='Thông báo !', message='Đã đăng ký thành công hãy quay lại đăng nhập !')
    if answer:
        root.destroy()
        import login
def close():
    root.destroy()
btnRegister = Button(frame,text="Đăng ký",font = f,activebackground="#00FF66",activeforeground="white",fg='gray', command=validate).place(x=65, y=240,width=300)
btnClose = Button(frame,text="Thoát",font = f,activebackground="#00FF66",activeforeground="white",fg='gray',command=close).place(x=65, y=310,width=300)

root.mainloop()