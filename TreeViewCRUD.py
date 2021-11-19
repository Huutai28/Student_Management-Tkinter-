from tkinter import *
from tkinter import ttk, colorchooser
from tkinter import messagebox
from tkinter.messagebox import askyesno
from configparser import ConfigParser
import mysql.connector


root = Tk()
root.title('quan ly')
root.geometry('1000x500')
root.resizable(False,False)
#add menu
my_menu = Menu(root)
root.config(menu=my_menu)
#menu he thong
system_menu = Menu(my_menu,tearoff=0)
my_menu.add_cascade(label="Hệ thống", menu=system_menu)
def logout():
    root.destroy()
    import login
system_menu.add_command(label="Đăng xuất",command=logout)
system_menu.add_command(label="Đổi mật khẩu")
system_menu.add_separator()
system_menu.add_command(label="Thoát",command=root.quit)
#cau hinh menu
option_menu = Menu(my_menu,tearoff=0)
my_menu.add_cascade(label="Tuỳ chọn", menu=option_menu)
#read our config file and get colors
parser = ConfigParser()
parser.read("treebase.ini")
save_odd_color = parser.get('colors','odd_color')
save_even_color = parser.get('colors','even_color')
save_selected_color = parser.get('colors','selected_color')
def odd_color():
    #pick color
    odd_color = colorchooser.askcolor()[1]
    #update treeview
    if odd_color:
        # creata striped row Tags
        my_tree.tag_configure('oldrow', background=odd_color)
        #config file
        parser = ConfigParser()
        parser.read("treebase.ini")
        #set the color change
        parser.set('colors','odd_color',odd_color)
        #save the config file
        with open('treebase.ini','w') as configfile:
            parser.write(configfile)
def even_color():
    # pick color
    even_color = colorchooser.askcolor()[1]
    # update treeview
    if even_color:
        # creata striped row Tags
        my_tree.tag_configure('evenrow', background=even_color)
        # config file
        parser = ConfigParser()
        parser.read("treebase.ini")
        # set the color change
        parser.set('colors', 'even_color', even_color)
        # save the config file
        with open('treebase.ini', 'w') as configfile:
            parser.write(configfile)
def selected_color():
    # pick color
    selected_color = colorchooser.askcolor()[1]
    # update treeview
    if selected_color:
        style.map('Treeview',
              background=[('selected', selected_color)])
        # config file
        parser = ConfigParser()
        parser.read("treebase.ini")
        # set the color change
        parser.set('colors', 'selected_color',selected_color )
        # save the config file
        with open('treebase.ini', 'w') as configfile:
            parser.write(configfile)
def reset_color():
    #save original color to config file
    parser = ConfigParser()
    parser.read("treebase.ini")
    parser.set('colors', 'odd_color', 'lightblue')
    parser.set('colors', 'even_color', 'white')
    parser.set('colors', 'selected_color', '#347083')
    with open('treebase.ini', 'w') as configfile:
        parser.write(configfile)
    #reset the colors
    my_tree.tag_configure('oldrow', background='lightblue')
    my_tree.tag_configure('evenrow', background='white')
    style.map('Treeview',
              background=[('selected', '#347083')])

#drop down menu
option_menu.add_command(label="Đổi màu dòng lẻ",command=odd_color)
option_menu.add_command(label="Đổi màu dòng chẵn",command=even_color)
option_menu.add_command(label="Đổi màu dòng chọn",command=selected_color)
option_menu.add_separator()
option_menu.add_command(label="Màu mặc định",command=reset_color)
def search_record():
    lockup_record = search_entry.get()
    if lockup_record == "":
        messagebox.showinfo("Thông báo !","Vui lòng nhập tên sinh viên !")
        search_entry.focus()
        return
    search.destroy()
    my_tree.delete(*my_tree.get_children())
    db = mysql.connector.connect(host ="localhost", user ="root", password ="", db ="quanly")
    cursor = db.cursor()
    cursor.execute("SELECT * FROM `sinhvien` WHERE `name` LIKE '" + lockup_record + "'")
    records = cursor.fetchall()
    global count
    count = 0
    for record in records:
        if count % 2 == 0:
            my_tree.insert(parent='', index='end', iid=count, text='',
                           values=(record[0], record[1], record[2], record[3], record[4], record[5], record[6]),
                           tags=('oldrow'))
        else:
            my_tree.insert(parent='', index='end', iid=count, text='',
                           values=(record[0], record[1], record[2], record[3], record[4], record[5], record[6]),
                           tags=('evenrow'))
        count += 1

def lockup_form():
    global search_entry, search
    search = Toplevel(root)
    search.title("Tìm kiếm theo tên")
    search.geometry("400x200")
    #create label frame
    search_frame = LabelFrame(search,text="Họ tên")
    search_frame.pack(padx=10,pady=10)
    #add entry box
    search_entry = Entry(search_frame,font=('Time',18))
    search_entry.pack(pady=20,padx=20)
    #add button
    search_button = Button(search,text="Tìm kiếm",command=search_record)
    search_button.pack(pady=20,padx=20)
#search menu
search_menu = Menu(my_menu,tearoff=0)
my_menu.add_cascade(label="Tìm kiếm", menu=search_menu)
search_menu.add_command(label="Tìm kiếm theo tên",command=lockup_form)
#thêm style
style = ttk.Style()
#chọn theme
style.theme_use('default')
#cấu hình màu cho tree view
style.configure("Treeview",
                background="#D3D3D3",
                rowheight=25,
                fielbackground="#D3D3D3")
#cấu hình màu khi chọn 1 dòng
style.map('Treeview',
          background=[('selected',save_selected_color)])
#Tạo treeview frame
tree_frame = Frame(root)
tree_frame.pack(pady=10)
#Tạo thanh cuộn cho treeview
tree_scroll = Scrollbar(tree_frame)
tree_scroll.pack(side=RIGHT, fill=Y)
#Tạo treeview
my_tree = ttk.Treeview(tree_frame, yscrollcommand=tree_scroll.set, selectmode="extended")
my_tree.pack()
#cấu hình thanh cuộn
tree_scroll.config(command=my_tree.yview)
#định nghĩa cho các cột
my_tree['columns'] = ("ID","Họ Tên","Giới tính","Lớp","Năm sinh","Địa chỉ","Quốc tịch")
#định kiểu cho các cột
my_tree.column("#0",width=0,stretch=NO)
my_tree.column("ID", anchor=CENTER,width=40)
my_tree.column("Họ Tên", anchor=W,width=140)
my_tree.column("Giới tính", anchor=CENTER,width=140)
my_tree.column("Lớp", anchor=CENTER,width=140)
my_tree.column("Năm sinh", anchor=CENTER,width=140)
my_tree.column("Địa chỉ", anchor=W,width=200)
my_tree.column("Quốc tịch", anchor=CENTER,width=140)
#tạo tiêu đề
my_tree.heading("#0",text="",anchor=W)
my_tree.heading("ID",text="ID",anchor=CENTER)
my_tree.heading("Họ Tên",text="Họ Tên",anchor=CENTER)
my_tree.heading("Giới tính",text="Giới tính",anchor=CENTER)
my_tree.heading("Lớp",text="Lớp",anchor=CENTER)
my_tree.heading("Năm sinh",text="Năm sinh",anchor=CENTER)
my_tree.heading("Địa chỉ",text="Địa chỉ",anchor=CENTER)
my_tree.heading("Quốc tịch",text="Quốc tịch",anchor=CENTER)
#lấy dữ liệu quốc tịch từ file countries.txt
countries = []
variable = StringVar()
world = open('countries.txt', 'r')
for country in world:
    country = country.rstrip('\n')
    countries.append(country)
#thiếp lập quốc tịnh mặc định
variable.set(country)
#creata striped row Tags
my_tree.tag_configure('oldrow',background= save_odd_color)
my_tree.tag_configure('evenrow',background= save_even_color)
#load record
def load_record():
    my_tree.delete(*my_tree.get_children())
    db = mysql.connector.connect(host ="localhost", user ="root", password ="", db ="quanly")
    cursor = db.cursor()
    cursor.execute("SELECT * FROM sinhvien")
    records = cursor.fetchall()
    global  count
    count = 0
    for record in records:
        if count % 2 == 0:
            my_tree.insert(parent='', index='end', iid=count, text='',
                           values=(record[0], record[1], record[2], record[3], record[4], record[5], record[6]),
                           tags=('oldrow'))
        else:
            my_tree.insert(parent='', index='end', iid=count, text='',
                           values=(record[0], record[1], record[2], record[3], record[4], record[5], record[6]),
                           tags=('evenrow'))
        count += 1
load_record()
#hộp nhập cho bản ghi
data_frame = LabelFrame(root,text="Thêm bản ghi mới")
data_frame.pack(fill="x",expand="yes",padx=20)

name_label = Label(data_frame,text="Họ Tên")
name_label.grid(row=0,column=0,padx=10,pady=10)
name_entry = Entry(data_frame)
name_entry.grid(row=0,column=1,padx=10,pady=10)

class_label = Label(data_frame,text="Lớp")
class_label.grid(row=0,column=2,padx=10,pady=10)
class_entry = Entry(data_frame)
class_entry.grid(row=0,column=3,padx=10,pady=10)

gender = StringVar()
gender.set("Nam")
gender_label = Label(data_frame,text="Giới tính")
gender_label.grid(row=0,column=4,padx=10,pady=10)
Radiobutton(data_frame,text="Nam",variable=gender,value="Nam").grid(row=0,column=5)
Radiobutton(data_frame,text="Nữ",variable=gender,value="Nữ").grid(row=0,column=6)

address_label = Label(data_frame,text="Địa chỉ")
address_label.grid(row=1,column=0,padx=10,pady=10)
address_entry = Entry(data_frame)
address_entry.grid(row=1,column=1,padx=10,pady=10)

birtyyear_label = Label(data_frame,text="Năm sinh")
birtyyear_label.grid(row=1,column=2,padx=10,pady=10)
birtyyear_entry = Entry(data_frame)
birtyyear_entry.grid(row=1,column=3,padx=10,pady=10)

countrie_label = Label(data_frame,text="Quốc tịch")
countrie_label.grid(row=1,column=4,padx=10,pady=10)
countrie_oMenu = OptionMenu(data_frame, variable,*countries)
countrie_oMenu.grid(row=1,column=5,padx=10,pady=10)

id = IntVar()
def clear_box():
    name_entry.delete(0, END)
    class_entry.delete(0, END)
    address_entry.delete(0, END)
    birtyyear_entry.delete(0, END)
    gender.set("Nam")
    variable.set(country)
#hàm chọn dòng
def select_record(e):
    global id
    #clear entry box
    name_entry.delete(0,END)
    class_entry.delete(0,END)
    address_entry.delete(0,END)
    birtyyear_entry.delete(0,END)
    #lấy số dòng
    selected = my_tree.focus()
    #lấy giá trị của dòng
    values = my_tree.item(selected,'values')
    #output
    id = values[0]
    name_entry.insert(0, values[1])
    class_entry.insert(0, values[3])
    address_entry.insert(0, values[5])
    birtyyear_entry.insert(0, values[4])
    gender.set(values[2])
    variable.set(values[6])
#chọn dòng set entry
my_tree.bind('<<TreeviewSelect>>', select_record)
my_tree.bind("ButtonRelease-1", select_record)
def up():
    rows = my_tree.selection()
    for row in rows:
        my_tree.move(row, my_tree.parent(row),my_tree.index(row)-1)
def down():
    rows = my_tree.selection()
    for row in reversed(rows):
        my_tree.move(row, my_tree.parent(row),my_tree.index(row)+1)
#validate form
def validate():
    if name_entry.get() == "":
        messagebox.showinfo("Thông báo lỗi !", "Bạn cần nhập họ tên !")
        name_entry.focus()
        return False
    if class_entry.get()== "":
        messagebox.showinfo("Thông báo lỗi !", "Bạn cần nhập lớp !")
        class_entry.focus()
        return False
    if address_entry.get()== "":
        messagebox.showinfo("Thông báo lỗi !", "Bạn cần nhập địa chỉ !")
        address_entry.focus()
        return False
    if birtyyear_entry.get()== "":
        messagebox.showinfo("Thông báo lỗi !", "Bạn cần nhập năm sinh!")
        birtyyear_entry.focus()
        return False
    a = birtyyear_entry.get()
    if len(a) <= 3 or len(a) >5:
        messagebox.showinfo("Thông báo lỗi !", "Năm sinh phải nhập 4 số !")
        birtyyear_entry.focus()
        return False
    try:
        int(birtyyear_entry.get())
    except ValueError:
        messagebox.showinfo("Thông Báo", "Năm sinh phải là số")
        return False
#add record
def add_record():
    if validate() == False:
        return
    try:
        db = mysql.connector.connect(host ="localhost", user ="root", password ="",  db ="quanly")
        cursor = db.cursor()
        cursor.execute("INSERT INTO sinhvien (name, gender, class, bitthyear,address,countrie) VALUES ('" + name_entry.get() + "','" + gender.get() + "','" + class_entry.get() + "','" + birtyyear_entry.get() + "','" + address_entry.get() + "','" + variable.get() + "')")
        db.commit()
        messagebox.showinfo('Thông báo !', 'Đã thêm mới sinh viên thành công !')
        load_record()
    except Exception as ep:
        messagebox.showerror("Thông báo !", ep)
def update_record():
    if validate() == False:
        return
    try:
        db = mysql.connector.connect(host ="localhost", user ="root", password ="", db ="quanly")
        cursor = db.cursor()
        cursor.execute("UPDATE sinhvien SET name = '" + name_entry.get() + "', gender = '" + gender.get() + "', class = '" + class_entry.get() + "', bitthyear = '" + birtyyear_entry.get() + "', address = '" + address_entry.get() + "', countrie = '" + variable.get() + "' WHERE id = '" + id + "'")
        db.commit()
        messagebox.showinfo('Thông báo !', 'Đã sửa sinh viên thành công !')
        load_record()
    except Exception as ep:
        messagebox.showerror("Thông báo !", ep)
def remove_one_record():
    answer = askyesno(title='Xác nhận',
                      message='Bạn có thực sự muốn xóa ?')
    if answer:
        try:
            db = mysql.connector.connect(host ="localhost", user ="root", password ="", db ="quanly")
            cursor = db.cursor()
            cursor.execute("DELETE from sinhvien WHERE id = " + id )
            db.commit()
            messagebox.showinfo('Thông báo !', 'Đã xóa sinh viên thành công !')
            load_record()
        except Exception as ep:
            messagebox.showerror("Thông báo !", ep)
def remove_all_record():
    answer = askyesno(title='Xác nhận',
                      message='Bạn có thực sự muốn xóa tất cả ?')
    if answer:
        try:
            db = mysql.connector.connect(host ="localhost", user ="root", password ="", db ="quanly")
            cursor = db.cursor()
            cursor.execute("DELETE from sinhvien ")
            db.commit()
            messagebox.showinfo('Thông báo !', 'Đã xóa  thành công !')
            load_record()
        except Exception as ep:
            messagebox.showerror("Thông báo !", ep)
#Thêm các nút
button_frame = LabelFrame(root,text="Chức năng")
button_frame.pack(fill="x",expand="yes",padx=20)

update_button = Button(button_frame,text="Sửa",command=update_record)
update_button.grid(row=0,column=0,padx=10,pady=10)

add_button = Button(button_frame,text="Thêm",command=add_record)
add_button.grid(row=0,column=1,padx=10,pady=10)

remove_all_button = Button(button_frame,text="Xóa Tất Cả",command=remove_all_record)
remove_all_button.grid(row=0,column=2,padx=10,pady=10)

remove_one_button = Button(button_frame,text="Xóa 1 Dòng",command=remove_one_record)
remove_one_button.grid(row=0,column=3,padx=10,pady=10)

remove_many_button = Button(button_frame,text="Xóa nhiều Dòng")
remove_many_button.grid(row=0,column=4,padx=10,pady=10)

move_up_button = Button(button_frame,text="Lên",command=up)
move_up_button.grid(row=0,column=5,padx=10,pady=10)

move_down_button = Button(button_frame,text="Xuống",command=down)
move_down_button.grid(row=0,column=6,padx=10,pady=10)

clear_button = Button(button_frame,text="Làm mới",command=clear_box)
clear_button.grid(row=0,column=7,padx=10,pady=10)

root.mainloop()