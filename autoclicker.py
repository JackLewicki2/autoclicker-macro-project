from tkinter import *
import keyboard
import mouse # todo -> add a way to delete individual macro commands
import time
import threading
#---classes---
class Autoclicker:
    def __init__(self,toggle_key,key_click,delay):
        self.toggle_key = toggle_key
        if("Click" in key_click): # if is a mouse press
            self.key_click = key_click.split(" ")[0].lower()
            self.click_mouse = True
        else: # otherwise is a keyboard press
            if(key_click in shift_symbols):
                self.key_click = key_click + " " # add space at the end to indicate needs a shift key
            else:
                self.key_click = key_click
            self.click_mouse=False
        self.delay=float(delay)
        if(self.delay==0):
            self.delay=1
        self.thread = None
        self.active=False

    def make_thread(self):
        self.thread = threading.Thread(target=lambda:autoclick(self.delay,self), daemon=True)

class Macro: #obj = Macro(toggle_key,loop,command_list)
    def __init__(self,toggle_key,loop, command_list):
        self.toggle_key = toggle_key
        self.loop=loop
        self.command_list=[]
        for command in command_list:
            if("Click" in command[0]): # if is a mouse press
                key_click = command[0].split(" ")[0].lower()
                click_mouse = True
            else: # otherwise is a keyboard press
                if(command[0] in shift_symbols):
                    key_click = command[0] + " " # add space at the end to indicate needs a shift key
                else:
                    key_click = command[0]
                click_mouse=False
            delay=float(command[1])
            if(delay==0):
                delay=1
            self.command_list.append([click_mouse,key_click,delay])
        self.thread = None
        self.active=False

    def make_thread(self):
        self.thread = threading.Thread(target=lambda:execute_macro(self.loop,self.command_list,self), daemon=True)

#---methods---
        
#changes mode
def change_mode():
    global current_mode
    global list_of_active_items
    if(current_mode=="Edit"): # changing mode to running
        change_mode_button.config(text="Change mode to " + current_mode) # todo -> capitalize mode
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
        for index in range(len(list_of_checkbox_variables)):
            if list_of_checkbox_variables[index].get(): # if item is active
                if(len(list_of_items[index])==5): # length 5 means is autoclicker. A bigger length means is a macro.
                    toggle_key_frame = list_of_items[index][2]
                    toggle_key = toggle_key_frame.winfo_children()[1].get()
                    if(toggle_key==""):
                        continue
                    
                    key_click_frame = list_of_items[index][3]
                    widget_holding_key_click = key_click_frame.winfo_children()[2]
                    if(str(type(widget_holding_key_click)) == "<class 'tkinter.Entry'>"):
                        key_click = widget_holding_key_click.get()
                    else:
                        key_click = widget_holding_key_click.getvar(str(widget_holding_key_click.cget("textvariable")))
                    if(key_click==""):
                        continue

                    set_delay_frame = list_of_items[index][4]
                    delay = set_delay_frame.winfo_children()[1].get()
                    if(delay==""):
                        continue

                    obj = Autoclicker(toggle_key,key_click,delay)
                    list_of_active_items.append(obj)
                else:
                    toggle_key_frame = list_of_items[index][2]
                    toggle_key = toggle_key_frame.winfo_children()[1].get()
                    if(toggle_key==""):
                        continue
                    
                    loop_checkbox_frame = list_of_items[index][3]
                    widget_holding_loop_checkbox = loop_checkbox_frame.winfo_children()[1]
                    loop = widget_holding_loop_checkbox.getvar(str(widget_holding_loop_checkbox.cget("variable")))
                    
                    command_list=[]
                    successful_add = True
                    for i in range(5,len(list_of_items[index]),2):
                        key_click_frame = list_of_items[index][i]
                        widget_holding_key_click = key_click_frame.winfo_children()[2]
                        if(str(type(widget_holding_key_click)) == "<class 'tkinter.Entry'>"):
                            key_click = widget_holding_key_click.get()
                        else:
                            key_click = widget_holding_key_click.getvar(str(widget_holding_key_click.cget("textvariable")))
                        if(key_click==""):
                            successful_add=False
                            break

                        set_delay_frame = list_of_items[index][i+1]
                        delay = set_delay_frame.winfo_children()[1].get()
                        if(delay==""):
                            successful_add=False
                            break

                        command_list.append([key_click,delay])

                    if(not successful_add):
                       continue
                        
                    obj = Macro(toggle_key,loop,command_list)
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

# #converts a key in bad format to one Keyboard class can use
# def convert_key(wrong_format_key):
#     key_list = wrong_format_key.split("->")
#     if(key_list[1].strip()==""):
#         #special keyboard character like shift
#         match key_list[0].strip():
#             case "Escape":
#                 return "esc"
#             case "Tab":
#                 return "tab"
#             case "Caps_Lock":
#                 return "caps lock"
#             case "Shift_L":
#                 return "shift"
#             case "Control_L":
#                 return "ctrl"
#             case "Win_L":
#                 return "left windows"
#             case "Alt_L":
#                 return "alt"
#             case " ":
#                 return "space"
#             case "Alt_R":
#                 return "right alt"
#             case "Control_R":
#                 return "right ctrl"
#             case "Shift_R":
#                 return "right shift"
#             case "Return":
#                 return "enter"
#             case "BackSpace":
#                 return "backspace"
#             case _:
#                 return key_list[0].lower().strip()     
#     else:
#         #regular keyboard character
#         return key_list[1].strip()

#clicked a key
def clicked_key(event):
    global most_recent_key_pressed
    most_recent_key_pressed=event.name
    # print("keyboard event",event.name,event.scan_code)
    if(current_mode=="Running"):
        for item in list_of_active_items:
            # print("item key",item.key)
            if(item.toggle_key==event.name):
                # print("active mode")
                if(item.active):
                    item.active=False
                else:
                    item.active=True
                    item.make_thread()
                    item.thread.start()
#autoclick
def autoclick(delay,item):
    while(item.active):
        if(item.click_mouse):
            mouse.click(button=item.key_click)
        else:
            if(item.key_click[-1] == " "):
                keyboard.press("shift")
                keyboard.send(item.key_click[0])
                keyboard.release("shift")
            else:
                keyboard.send(item.key_click)
        # print("clicked")
        time.sleep(delay/1000.0)

#executing macro
def execute_macro(loop,command_list,item):
    while(item.active):
        for command in command_list:
            if(not item.active):
                return
            if(command[0]): # command is (is_mouse, key_click, delay)
                mouse.click(button=command[1])
            else:
                # print(item.key_click)
                if(command[1][-1] == " "): #space at end means need a shift key
                    keyboard.press("shift")
                    keyboard.send(command[1][0])
                    keyboard.release("shift")
                else:
                    keyboard.send(command[1])
            # print("clicked")
            time.sleep(command[2]/1000.0)
        if(not loop):
            item.active=False

#delete autoclicker button
def delete_autoclicker(current_row):
    global list_of_items
    index_of_item_deleting=-1
    #finding the index in list of items of the item we are deleting and moving items below up
    for list in list_of_items:
        if(list[0].grid_info()["row"] <= current_row):
            index_of_item_deleting+=1
        else:
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

#delete macro button
def delete_macro(current_row):
    global list_of_items
    index_of_item_deleting=-1
    number_of_commands=1
    #finding the index in list of items of the item we are deleting and moving items below up
    for list in list_of_items:
        if(list[0].grid_info()["row"] <= current_row):
            index_of_item_deleting+=1
        else:
            number_of_commands = (len(list_of_items[index_of_item_deleting])-5)//2
            for frame in list:
                if(frame.grid_info()["row"] > current_row+1):
                    frame.grid_configure(row=frame.grid_info()["row"] - 3 - number_of_commands)            
    #deleting the item
    for frame in list_of_items[index_of_item_deleting]:
        frame.grid_forget()
        frame.destroy()
    #removing item from list
    del list_of_items[index_of_item_deleting]
    del list_of_checkbox_variables[index_of_item_deleting]

    #moving the add_frame up
    add_frame.grid_configure(row=add_frame.grid_info()["row"] - 3 - number_of_commands)

#gets rid of the ' ' when type space key in an entry box
def strip_string_variable(string_variable):
    string_variable.set(string_variable.get().strip())

#sets toggle key and click key
def store_key_in_textbox(event):
    # print("most recent pressed:",most_recent_key_pressed)
    # print("current textbox: ", event.widget.get())
    # print("keysym (thing on left)",event.keysym)
    event.widget.delete(0,END)
    if(len(most_recent_key_pressed)!=1): # if length is not 1 is something like control or tab which doesn't have a representation
        if(most_recent_key_pressed=="backspace"):
            event.widget.insert(0,most_recent_key_pressed + "e") # need extra character because backspace deletes a character
        else:
            event.widget.insert(0,most_recent_key_pressed)

#makes sure can only type numbers in delay textbox
def validate_delay(S):
    if(S.isnumeric()):
        return True
    return False

#updates frame to be mouse or keyboard selection
def mouse_or_keyboard_selector_update(new_selection, current_frame):
    old_thing = current_frame.winfo_children()[2]
    old_thing.grid_forget()
    old_thing.destroy()

    if(new_selection=="Mouse"):
        mouse_button_selector_string=StringVar()
        mouse_button_selector = OptionMenu(current_frame, mouse_button_selector_string, "Left Click","Right Click", "Middle Click")
        mouse_button_selector.configure(bg="black", fg="white", activebackground="black",activeforeground="white")
        mouse_button_selector["menu"].config(bg="black",fg="white")
        mouse_button_selector_string.set("Left Click")
        mouse_button_selector.grid(row=0, column=2, padx=5)
    else:
        click_key_string = StringVar()
        click_key_string.trace_add("write", lambda name, index, mode: strip_string_variable(click_key_string))
        click_key_textbox=Entry(current_frame,fg="white", bg="black",font=("Arial",15), insertbackground="white", width=14, textvariable=click_key_string)
        click_key_textbox.bind("<Key>",store_key_in_textbox)
        click_key_textbox.grid(row=0,column=2, padx=5)

#add new command
def add_new_command(current_row):
    global list_of_items
    #finding index of where adding
    index_of_item_adding=-1
    #finding the index in list of items of the item we are deleting and moving items below down
    for list in list_of_items:
        if(list[0].grid_info()["row"] <= current_row):
            index_of_item_adding+=1
        else:
            for frame in list:
                if(frame.grid_info()["row"] > current_row):
                    frame.grid_configure(row=frame.grid_info()["row"] + 1) 

    number_of_commands = (len(list_of_items[index_of_item_adding])-5)//2 + 1

    #moving add frame
    add_frame.grid_configure(row=add_frame.grid_info()["row"] + 1)
    #moving add new command button
    list_of_items[index_of_item_adding][4].grid_configure(row=current_row + 1)

    #Set click key
    set_click_key_frame = Frame(mainframe)
    set_click_key_frame.grid(row=current_row,column=0, sticky=(N,E,S,W))
    set_click_key_frame.config(background="black")
    list_of_items[index_of_item_adding].append(set_click_key_frame)

    set_click_key_label = Label(set_click_key_frame,text=str(number_of_commands) + ". Click Key: ",fg="white", bg="black",font=("Arial",15))
    set_click_key_label.grid(row=0,column=0)

    mouse_or_keyboard_selector_string=StringVar()
    mouse_or_keyboard_selector = OptionMenu(set_click_key_frame, mouse_or_keyboard_selector_string, "Mouse","Keyboard", command= lambda new_selection: mouse_or_keyboard_selector_update(new_selection,set_click_key_frame))
    mouse_or_keyboard_selector.configure(bg="black", fg="white", activebackground="black",activeforeground="white")
    mouse_or_keyboard_selector["menu"].config(bg="black",fg="white")
    mouse_or_keyboard_selector_string.set("Mouse")
    mouse_or_keyboard_selector.grid(row=0, column=1, padx=(0,5))

    # toggle_key_textbox=Entry(set_click_key_frame,fg="white", bg="black",font=("Arial",15), insertbackground="white")
    # toggle_key_textbox.bind("<Key>",store_key_in_textbox)
    # toggle_key_textbox.grid(row=0,column=2, padx=5)

    mouse_button_selector_string=StringVar()
    mouse_button_selector = OptionMenu(set_click_key_frame, mouse_button_selector_string, "Left Click","Right Click", "Middle Click")
    mouse_button_selector.configure(bg="black", fg="white", activebackground="black",activeforeground="white")
    mouse_button_selector["menu"].config(bg="black",fg="white")
    mouse_button_selector_string.set("Left Click")
    mouse_button_selector.grid(row=0, column=2, padx=5)

    #Set Delay
    set_delay_frame = Frame(mainframe)
    set_delay_frame.grid(row=current_row,column=1, sticky=(N,E,S,W))
    set_delay_frame.config(background="black")
    list_of_items[index_of_item_adding].append(set_delay_frame)

    set_delay_label = Label(set_delay_frame,text="Delay: ",fg="white", bg="black",font=("Arial",15))
    set_delay_label.grid(row=0,column=0)

    set_delay_validate_command = (set_delay_frame.register(validate_delay),"%S")
    set_delay_textbox=Entry(set_delay_frame,fg="white", bg="black",font=("Arial",15), insertbackground="white", width=10, validate="key", validatecommand=set_delay_validate_command)
    set_delay_textbox.grid(row=0,column=1)

    set_delay_seconds_label = Label(set_delay_frame,text="miliseconds",fg="white", bg="black",font=("Arial",15))
    set_delay_seconds_label.grid(row=0,column=2)

#add new item
def add_new():
    #getting needed variables
    global list_of_items
    global list_of_checkbox_variables
    current_row = add_frame.grid_info()["row"]
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
        delete_button = Button(type_delete_frame,text="Delete", command=lambda: delete_autoclicker(type_delete_frame.grid_info()["row"]), fg="white", bg="black", activeforeground="white",activebackground="black")
        delete_button.grid(row=0, column=1, padx=23)

        #Set Toggle Key
        toggle_key_frame = Frame(mainframe)
        toggle_key_frame.grid(row=current_row+1,column=0, sticky=(N,E,S,W))
        toggle_key_frame.config(background="black")
        list_of_items[len(list_of_items)-1].append(toggle_key_frame)

        toggle_key_label = Label(toggle_key_frame,text="Toggle Key: ",fg="white", bg="black",font=("Arial",15))
        toggle_key_label.grid(row=0,column=0)

        toggle_key_string = StringVar()
        toggle_key_string.trace_add("write", lambda name, index, mode: strip_string_variable(toggle_key_string))
        toggle_key_textbox=Entry(toggle_key_frame,fg="white", bg="black",font=("Arial",15), insertbackground="white", textvariable = toggle_key_string)
        toggle_key_textbox.bind("<Key>",store_key_in_textbox)
        toggle_key_textbox.grid(row=0,column=1)

        #Set click key
        set_click_key_frame = Frame(mainframe)
        set_click_key_frame.grid(row=current_row+1,column=1, sticky=(N,E,S,W))
        set_click_key_frame.config(background="black")
        list_of_items[len(list_of_items)-1].append(set_click_key_frame)

        set_click_key_label = Label(set_click_key_frame,text="Click Key: ",fg="white", bg="black",font=("Arial",15))
        set_click_key_label.grid(row=0,column=0)

        mouse_or_keyboard_selector_string=StringVar()
        mouse_or_keyboard_selector = OptionMenu(set_click_key_frame, mouse_or_keyboard_selector_string, "Mouse","Keyboard", command= lambda new_selection: mouse_or_keyboard_selector_update(new_selection,set_click_key_frame))
        mouse_or_keyboard_selector.configure(bg="black", fg="white", activebackground="black",activeforeground="white")
        mouse_or_keyboard_selector["menu"].config(bg="black",fg="white")
        mouse_or_keyboard_selector_string.set("Mouse")
        mouse_or_keyboard_selector.grid(row=0, column=1, padx=(0,5))

        # toggle_key_textbox=Entry(set_click_key_frame,fg="white", bg="black",font=("Arial",15), insertbackground="white")
        # toggle_key_textbox.bind("<Key>",store_key_in_textbox)
        # toggle_key_textbox.grid(row=0,column=2, padx=5)

        mouse_button_selector_string=StringVar()
        mouse_button_selector = OptionMenu(set_click_key_frame, mouse_button_selector_string, "Left Click","Right Click", "Middle Click")
        mouse_button_selector.configure(bg="black", fg="white", activebackground="black",activeforeground="white")
        mouse_button_selector["menu"].config(bg="black",fg="white")
        mouse_button_selector_string.set("Left Click")
        mouse_button_selector.grid(row=0, column=2, padx=5)

        #Set Delay
        set_delay_frame = Frame(mainframe)
        set_delay_frame.grid(row=current_row+1,column=2, sticky=(N,E,S,W))
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
        #moving add_frame down three
        add_frame.grid_configure(row=current_row+4)

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
        delete_button = Button(type_delete_frame,text="Delete", fg="white", bg="black", activeforeground="white",activebackground="black")
        delete_button.grid(row=0, column=1, padx=63)

        #Set Toggle Key
        toggle_key_frame = Frame(mainframe)
        toggle_key_frame.grid(row=current_row+1,column=0, sticky=(N,E,S,W))
        toggle_key_frame.config(background="black")
        list_of_items[len(list_of_items)-1].append(toggle_key_frame)

        toggle_key_label = Label(toggle_key_frame,text="Toggle Key: ",fg="white", bg="black",font=("Arial",15))
        toggle_key_label.grid(row=0,column=0)

        toggle_key_string = StringVar()
        toggle_key_string.trace_add("write", lambda name, index, mode: strip_string_variable(toggle_key_string))
        toggle_key_textbox=Entry(toggle_key_frame,fg="white", bg="black",font=("Arial",15), insertbackground="white", textvariable=toggle_key_string)
        toggle_key_textbox.bind("<Key>",store_key_in_textbox)
        toggle_key_textbox.grid(row=0,column=1)

        #loop checkbox
        loop_checkbox_frame = Frame(mainframe)
        loop_checkbox_frame.grid(row=current_row+1,column=1, sticky=(N,E,S,W))
        loop_checkbox_frame.config(background="black")
        list_of_items[len(list_of_items)-1].append(loop_checkbox_frame)

        loop_checkbox_label = Label(loop_checkbox_frame,text="Loop: ",fg="white", bg="black",font=("Arial",15))
        loop_checkbox_label.grid(row=0,column=0)

        loop_checkbox_var=BooleanVar()
        loop_checkbox=Checkbutton(loop_checkbox_frame, variable=loop_checkbox_var, onvalue=True, offvalue=False,fg="white", bg="black", selectcolor="black",activeforeground="white",activebackground="black")
        loop_checkbox.grid(row=0,column=1)
        # list_of_checkbox_variables.append(loop_checkbox_var)

        #Set click key
        set_click_key_frame = Frame(mainframe)
        set_click_key_frame.grid(row=current_row+2,column=0, sticky=(N,E,S,W))
        set_click_key_frame.config(background="black")
        list_of_items[len(list_of_items)-1].append(set_click_key_frame)

        set_click_key_label = Label(set_click_key_frame,text="1. Click Key: ",fg="white", bg="black",font=("Arial",15))
        set_click_key_label.grid(row=0,column=0)

        mouse_or_keyboard_selector_string=StringVar()
        mouse_or_keyboard_selector = OptionMenu(set_click_key_frame, mouse_or_keyboard_selector_string, "Mouse","Keyboard", command= lambda new_selection: mouse_or_keyboard_selector_update(new_selection,set_click_key_frame))
        mouse_or_keyboard_selector.configure(bg="black", fg="white", activebackground="black",activeforeground="white")
        mouse_or_keyboard_selector["menu"].config(bg="black",fg="white")
        mouse_or_keyboard_selector_string.set("Mouse")
        mouse_or_keyboard_selector.grid(row=0, column=1, padx=(0,5))

        # toggle_key_textbox=Entry(set_click_key_frame,fg="white", bg="black",font=("Arial",15), insertbackground="white")
        # toggle_key_textbox.bind("<Key>",store_key_in_textbox)
        # toggle_key_textbox.grid(row=0,column=2, padx=5)

        mouse_button_selector_string=StringVar()
        mouse_button_selector = OptionMenu(set_click_key_frame, mouse_button_selector_string, "Left Click","Right Click", "Middle Click")
        mouse_button_selector.configure(bg="black", fg="white", activebackground="black",activeforeground="white")
        mouse_button_selector["menu"].config(bg="black",fg="white")
        mouse_button_selector_string.set("Left Click")
        mouse_button_selector.grid(row=0, column=2, padx=5)

        #Set Delay
        set_delay_frame = Frame(mainframe)
        set_delay_frame.grid(row=current_row+2,column=1, sticky=(N,E,S,W))
        set_delay_frame.config(background="black")
        list_of_items[len(list_of_items)-1].append(set_delay_frame)

        set_delay_label = Label(set_delay_frame,text="Delay: ",fg="white", bg="black",font=("Arial",15))
        set_delay_label.grid(row=0,column=0)

        set_delay_validate_command = (set_delay_frame.register(validate_delay),"%S")
        set_delay_textbox=Entry(set_delay_frame,fg="white", bg="black",font=("Arial",15), insertbackground="white", width=10, validate="key", validatecommand=set_delay_validate_command)
        set_delay_textbox.grid(row=0,column=1)

        set_delay_seconds_label = Label(set_delay_frame,text="miliseconds",fg="white", bg="black",font=("Arial",15))
        set_delay_seconds_label.grid(row=0,column=2)

        #add another command button
        add_another_command_frame = Frame(mainframe)
        add_another_command_frame.grid(row=current_row+3,column=0, sticky=(N,E,S,W))
        add_another_command_frame.config(background="black")
        list_of_items[len(list_of_items)-1].insert(4,add_another_command_frame) # insert at 4 so that all command frames are at the end

        add_another_command_button = Button(add_another_command_frame,text="Add Another Command", command=lambda: add_new_command(add_another_command_frame.grid_info()["row"]), fg="white", bg="black", activeforeground="white",activebackground="black")
        add_another_command_button.grid(row=0, column=0)

        #setting up delete button
        delete_button.configure(command=lambda: delete_macro(type_delete_frame.grid_info()["row"]))



#---setting up window---
window = Tk() # instantiates an instance of a window
window.title("Macro App") # title of window
# icon = PhotoImage(file='mouseicon.png') # turning image into format tkinter can use. HAS TO BE PNG
# window.iconphoto(True, icon)
window.geometry("1100x400") # initial size of window

#---setting up mainframe---
mainframe = Frame(window)
mainframe.grid(row=0, column=0, sticky=(N,E,S,W)) # sticky means it will stick to sides of the window
window.columnconfigure(0, weight=1) # column 0 will strech to take up all available space 
window.rowconfigure(0,weight=1) # row 0 will strech to take up all available space
mainframe.config(background="black")

#---modes---
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
add_button = Button(add_frame,text="Add New", command=add_new, fg="white", bg="black", activeforeground="white",activebackground="black",font=("Arial",15))
add_button.grid(row=0, column=0)

#type selector
type_selector_label = Label(add_frame, text="Type: ", fg="white", bg="black",font=("Arial",15))
type_selector_label.grid(row=0, column=1, padx=(10,0))

type_selector_string=StringVar()
type_selector = OptionMenu(add_frame, type_selector_string, "Autoclicker","Macro")
type_selector.configure(bg="black", fg="white", activebackground="black",activeforeground="white")
type_selector["menu"].config(bg="black",fg="white")
type_selector_string.set("Autoclicker")
type_selector.grid(row=0, column=2)



#variables for stuff
list_of_items=[]
list_of_checkbox_variables=[]
list_of_active_items=[]
most_recent_key_pressed=""
shift_symbols = '~!@#$%^&*()_+QWERTYUIOP{}|ASDFGHJKL:"ZXCVBNM<>?'

#---whatever---
#adds spacing to each widget
for child in mainframe.winfo_children(): 
    child.grid_configure(padx=5, pady=5)

keyboard.on_press(clicked_key) # activates keyboard
window.mainloop() # activates the window