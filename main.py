from tkinter import *
import keyboard
import mouse
import time
import threading
#---classes---
class Autoclicker:
    def __init__(self,key,delay):
        key_list = key.split(" -> ")
        if(key_list[1]==""):
            #special keyboard character like shift
            match key_list[0]:
                case "Escape":
                    self.key="esc"
                case "Tab":
                    self.key="tab"
                case "Caps_Lock":
                    self.key="caps lock"
                case "Shift_L":
                    self.key="shift"
                case "Control_L":
                    self.key="ctrl"
                case "Win_L":
                    self.key="left windows"
                case "Alt_R":
                    self.key="right alt"
                case "Control_R":
                    self.key="right ctrl"
                case "Shift_R":
                    self.key="right shift"
                case "enter":
                    self.key="Return"
                case _:
                    self.key=key_list[0].lower().strip()     
        else:
            #regular keyboard character
            self.key=key_list[1].strip()

        self.delay=float(delay)
        self.thread = None
        self.active=False

    def make_thread(self):
        self.thread = threading.Thread(target=lambda:autoclick(self.delay,self), daemon=True)

#---methods---
#changes mode
def change_mode():
    global current_mode
    global list_of_active_items
    if(current_mode=="Edit"): # changing mode to running
        change_mode_button.config(text="Change mode to " + current_mode)
        current_mode="Running"
        #disable all settings while running
        for list in list_of_items:
            for frame in list:
                for child in frame.winfo_children(): 
                    child.configure(state="disabled")
        add_button.configure(state="disabled")
        type_selector.configure(state="disabled")

        #sets up list to hold object of the active items
        list_of_active_items=[]
        for index in range(len(list_of_checkbox_variables)): # todo -> when make macro will need another if to check if want an autoclicker or macro
            if list_of_checkbox_variables[index].get(): # if item is active
                toggle_key_frame = list_of_items[index][2]
                toggle_key = toggle_key_frame.winfo_children()[1].get()
                if(toggle_key==""):
                    continue
                set_delay_frame = list_of_items[index][3]
                delay = set_delay_frame.winfo_children()[1].get()
                if(delay==""):
                    continue
                obj = Autoclicker(toggle_key,delay)
                list_of_active_items.append(obj)
    else: # changing mode to edit
        change_mode_button.config(text="Change mode to " + current_mode)
        current_mode="Edit"
        #turns off any running items
        for item in list_of_active_items:
            item.active=False
        #enable all settings while editting
        for list in list_of_items:
            for frame in list:
                for child in frame.winfo_children(): 
                    child.configure(state="normal")
        add_button.configure(state="normal")
        type_selector.configure(state="normal")
    #update current_mode_label
    current_mode_label.config(text="Current Mode: " + current_mode)
    
#clicked a key
def clicked_key(event):
    print("event",event.name)
    if(current_mode=="Running"):
        for item in list_of_active_items:
            print("item key",item.key)
            if(item.key==event.name):
                print("active mode")
                if(item.active):
                    item.active=False
                else:
                    item.active=True
                    item.make_thread()
                    item.thread.start()
#autoclick
def autoclick(delay,item):
    while(True):
        mouse.click()
        print("clicked")
        time.sleep(delay/1000.0)
        if(not item.active):
           break
#delete autoclicker button
def delete_autoclicker(current_row):
    global list_of_items
    index_of_item_deleting=-1
    #finding the index in list of items of the item we are deleting and moving items below up
    for list in list_of_items:
        if(list[0].grid_info()["row"] <= current_row):
            index_of_item_deleting+=1
        for frame in list:
            if(frame.grid_info()["row"] > current_row+1):
                frame.grid_configure(row=frame.grid_info()["row"] -2)            
    #deleting the item
    for frame in list_of_items[index_of_item_deleting]:
        frame.grid_forget()
        frame.destroy()
    #removing item from list
    del list_of_items[index_of_item_deleting]
    del list_of_checkbox_variables[index_of_item_deleting]

    #moving the add_frame up
    add_frame.grid_configure(row=add_frame.grid_info()["row"] -2)

#sets toggle key
def set_toggle_key(event):
    print("keysym ",event.keysym)
    event.widget.delete(0,END)
    event.widget.insert(0,event.keysym + " -> ") #todo -> decide if want to display both keysym and the symbol

#makes sure can only type numbers in delay textbox
def validate_delay(S):
    if(S.isnumeric()):
        return True
    return False

#add new item
def add_new():     #todo -> make this work; create frame for label and checkbox to go in together
    #getting needed variables
    global list_of_items
    global list_of_checkbox_variables
    current_row = add_frame.grid_info()["row"]
    # current_col = add_frame.grid_info()["column"] # not needed???
    type = type_selector_string.get()
    #updating list
    list_of_items.append([])

    if(type=="Autoclicker"):
        #moving add_frame down two
        add_frame.grid_configure(row=current_row+2)

        #active label and active checkbox
        checkbox_name_frame = Frame(mainframe)
        checkbox_name_frame.grid(row=current_row,column=0, sticky=(N,E,S,W))
        checkbox_name_frame.config(background="black")
        list_of_items[len(list_of_items)-1].append(checkbox_name_frame)

        active_label = Label(checkbox_name_frame,text="Active: ",fg="white", bg="black",font=("Arial",15))
        active_label.grid(row=0,column=0)

        active_checkbox_var=BooleanVar()
        active_checkbox=Checkbutton(checkbox_name_frame, variable=active_checkbox_var, onvalue=True, offvalue=False,fg="white", bg="black", selectcolor="black",activeforeground="white",activebackground="black")
        active_checkbox.grid(row=0,column=1)
        list_of_checkbox_variables.append(active_checkbox_var)

       

        #name label and name textbox
        name_label = Label(checkbox_name_frame,text="Name: ",fg="white", bg="black",font=("Arial",15))
        name_label.grid(row=0,column=2)

        name_textbox=Entry(checkbox_name_frame,fg="white", bg="black",font=("Arial",15), insertbackground="white")
        name_textbox.grid(row=0,column=3)

        #Type text
        type_delete_frame = Frame(mainframe)
        type_delete_frame.grid(row=current_row,column=1, sticky=(N,E,S,W))
        type_delete_frame.config(background="black")
        list_of_items[len(list_of_items)-1].append(type_delete_frame)

        type_label = Label(type_delete_frame,text="Type: "+type,fg="white", bg="black",font=("Arial",15))
        type_label.grid(row=0,column=0, padx=5)

        #delete button
        delete_button = Button(type_delete_frame,text="Delete", command=lambda: delete_autoclicker(type_delete_frame.grid_info()["row"]))
        delete_button.grid(row=0, column=1, padx=10)

        #Set Toggle Key
        toggle_key_frame = Frame(mainframe)
        toggle_key_frame.grid(row=current_row+1,column=0, sticky=(N,E,S,W))
        toggle_key_frame.config(background="black")
        list_of_items[len(list_of_items)-1].append(toggle_key_frame)

        toggle_key_label = Label(toggle_key_frame,text="Toggle Key: ",fg="white", bg="black",font=("Arial",15))
        toggle_key_label.grid(row=0,column=0)

        toggle_key_textbox=Entry(toggle_key_frame,fg="white", bg="black",font=("Arial",15), insertbackground="white")
        toggle_key_textbox.bind("<Key>",set_toggle_key)
        toggle_key_textbox.grid(row=0,column=1)

        #Set Delay
        set_delay_frame = Frame(mainframe)
        set_delay_frame.grid(row=current_row+1,column=1, sticky=(N,E,S,W))
        set_delay_frame.config(background="black")
        list_of_items[len(list_of_items)-1].append(set_delay_frame)

        set_delay_label = Label(set_delay_frame,text="Delay: ",fg="white", bg="black",font=("Arial",15))
        set_delay_label.grid(row=0,column=0)

        set_delay_validate_command = (set_delay_frame.register(validate_delay),"%S")
        set_delay_textbox=Entry(set_delay_frame,fg="white", bg="black",font=("Arial",15), insertbackground="white", width=10, validate="key", validatecommand=set_delay_validate_command)
        set_delay_textbox.grid(row=0,column=1)

        set_delay_seconds_label = Label(set_delay_frame,text="miliseconds",fg="white", bg="black",font=("Arial",15))
        set_delay_seconds_label.grid(row=0,column=2)
    elif(type=="Macro"):
        pass

#---setting up window---
window = Tk() # instantiates an instance of a window
window.title("Jack's Macro App") # title of window
icon = PhotoImage(file='shedinja.png') # turning image into format tkinter can use. HAS TO BE PNG
window.iconphoto(True, icon)
window.geometry("700x400") # initial size of window

#---setting up mainframe---
mainframe = Frame(window)
mainframe.grid(row=0, column=0, sticky=(N,E,S,W)) # sticky means it will stick to sides of the window
window.columnconfigure(0, weight=1) # column 0 will strech to take up all available space 
window.rowconfigure(0,weight=1) # row 0 will strech to take up all available space #todo -> apply this for everything so they grow with window size
mainframe.config(background="black")

#---modes---
#todo -> make button always be in same spot regardless of current mode text
current_mode = "Edit"
#Text
current_mode_label = Label(mainframe, text="Current Mode: " + current_mode, fg="white", bg="black",font=("Arial",15))
current_mode_label.grid(row=0,column=0)
#Button to Change
change_mode_button = Button(mainframe, text="Change mode to " + "Running", command=change_mode, fg="white", bg="black", activeforeground="white",activebackground="black",font=("Arial",15))
change_mode_button.grid(row=0, column=1)

#---add button---
#frame so everything is next to each other
add_frame = Frame(mainframe)
add_frame.grid(row=1, column=0, sticky=(N,E,S,W))
add_frame.config(background="black")

#Add button
add_button = Button(add_frame,text="Add New", command=add_new)
add_button.grid(row=0, column=0)

#type selector
type_selector_label = Label(add_frame, text="Type: ", fg="white", bg="black",font=("Arial",15))
type_selector_label.grid(row=0, column=1, padx=(10,0))

type_selector_string=StringVar()
type_selector = OptionMenu(add_frame, type_selector_string, "Autoclicker","Macro")
type_selector_string.set("Autoclicker")

type_selector.grid(row=0, column=2)

#variables for stuff
list_of_items=[]
list_of_checkbox_variables=[]
list_of_active_items=[]

#---whatever---
#adds spacing to each widget
for child in mainframe.winfo_children(): 
    child.grid_configure(padx=5, pady=5)

    #todo -> maybe put other things here like bg, font, etc.

keyboard.on_press(clicked_key) # activates keyboard
window.mainloop() # activates the window