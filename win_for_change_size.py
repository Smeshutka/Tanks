import tkinter

def create_dialog_window():
    def increase1():
        value = int(lbl_value["text"])
        lbl_value["text"] = f"{value + 1}"
    
    def increase10():
        value = int(lbl_value["text"])
        lbl_value["text"] = f"{value + 10}"
     
    def decrease1():
        value = int(lbl_value["text"])
        lbl_value["text"] = f"{value - 1}"
    
    def decrease10():
        value = int(lbl_value["text"])
        lbl_value["text"] = f"{value - 10}"
        
    def increase1_2():
        value = int(lbl_value2["text"])
        lbl_value2["text"] = f"{value + 1}"
    
    def increase10_2():
        value = int(lbl_value2["text"])
        lbl_value2["text"] = f"{value + 10}"
     
    def decrease1_2():
        value = int(lbl_value2["text"])
        lbl_value2["text"] = f"{value - 1}"
    
    def decrease10_2():
        value = int(lbl_value2["text"])
        lbl_value2["text"] = f"{value - 10}"
    
    def submit():
        value = int(lbl_value["text"])
        value2 = int(lbl_value2["text"])
        file = open('new_size.txt','w')
        file.write(str(value)+' '+str(value2))
        file.close()
        window.destroy()
        
        
    window = tkinter.Tk()
    window.title("Изменение размеров карты")
    window.rowconfigure([0,1,2,3,4], minsize=50, weight=1)
    window.columnconfigure([0, 1, 2, 3, 4], minsize=50, weight=1)
    
    btn_decrease10 = tkinter.Button(master=window,text="-10",command=decrease10)
    btn_decrease1 = tkinter.Button(master=window,text="-1",command=decrease1)
    btn_increase1 = tkinter.Button(master=window,text="+1",command=increase1)
    btn_increase10 = tkinter.Button(master=window,text="+10",command=increase10)
    lbl_value = tkinter.Label(master=window, text="0")
    
    btn_decrease10_2 = tkinter.Button(master=window,text="-10",command=decrease10_2)
    btn_decrease1_2 = tkinter.Button(master=window,text="-1",command=decrease1_2)
    btn_increase1_2 = tkinter.Button(master=window,text="+1",command=increase1_2)
    btn_increase10_2 = tkinter.Button(master=window,text="+10",command=increase10_2)
    lbl_value2 = tkinter.Label(master=window, text="0")
     
    lbl1 = tkinter.Label(master=window, text="кол-во столбцов")
    lbl2 = tkinter.Label(master=window, text="кол-во строк")
     
    lbl1.grid(row=0, column=2)
    btn_decrease10.grid(row=1, column=0, sticky="nsew")
    btn_decrease1.grid(row=1, column=1, sticky="nsew")
    lbl_value.grid(row=1, column=2)    
    btn_increase1.grid(row=1, column=3, sticky="nsew")
    btn_increase10.grid(row=1, column=4, sticky="nsew")
    
    lbl2.grid(row=2, column=2)
    btn_decrease10_2.grid(row=3, column=0, sticky="nsew")
    btn_decrease1_2.grid(row=3, column=1, sticky="nsew")
    lbl_value2.grid(row=3, column=2)    
    btn_increase1_2.grid(row=3, column=3, sticky="nsew")
    btn_increase10_2.grid(row=3, column=4, sticky="nsew")
    
    submit_but = tkinter.Button(master=window, text="Создать", command=submit)
    submit_but.grid(row=4, column=2)
    
    window.mainloop()
    
