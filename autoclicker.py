from tkinter import * #todo -> update readme to say ms means miliseconds and new meaning of delay
import keyboard
import mouse #todo -> type text option for macro where can type multiple regular keys; option is delay between keystrokes 
import time
import threading
from enum import Enum
#---classes---
class command_type(Enum):
    Mouse_Click=1
    Keyboard_Press=2
    Wait=3

class Autoclicker:
    def __init__(self,toggle_key,key_click,delay):
        self.toggle_key = toggle_key
        if("Click" in key_click): # if is a mouse press
            self.key_click = key_click.split(" ")[0].lower()
            self.type = command_type.Mouse_Click
        else: # otherwise is a keyboard press
            if(key_click in shift_symbols):
                self.key_click = key_click + " " # add space at the end to indicate needs a shift key
            else:
                self.key_click = key_click
            self.type=command_type.Keyboard_Press
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
            if(command[0]==""):
                key_click=""
                type=command_type.Wait
            elif("Click" in command[0]): # if is a mouse press
                key_click = command[0].split(" ")[0].lower()
                type = command_type.Mouse_Click
            else: # otherwise is a keyboard press
                if(command[0] in shift_symbols):
                    key_click = command[0] + " " # add space at the end to indicate needs a shift key
                else:
                    key_click = command[0]
                type=command_type.Keyboard_Press
           
            time_hold=int(command[1])
            times_repeat=int(command[2])
            delay=int(command[3])

            if(delay==0):
                delay=1
            self.command_list.append([type, key_click, time_hold, times_repeat, delay])
        self.thread = None
        self.active=False

    def make_thread(self):
        self.thread = threading.Thread(target=lambda:execute_macro(self.loop,self.command_list,self), daemon=True)

#---methods---
        
#changes mode
def change_mode():
    global current_mode
    global list_of_active_items
    global number_of_frames_in_macro_command
    if(current_mode=="Edit"): # changing mode to running
        change_mode_button.config(text="Change Mode to " + current_mode)
        current_mode="Running"
        #disable all settings while running
        for list in list_of_items:
            for frame in list:
                for child in frame.winfo_children(): 
                    child.configure(state="disabled")
        add_button.configure(state="disabled")
        type_selector_label.configure(state="disabled")
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
                    for i in range(5,len(list_of_items[index]),number_of_frames_in_macro_command):
                        key_click_frame = list_of_items[index][i]
                        widget_holding_key_click = key_click_frame.winfo_children()[2]
                        if(str(type(widget_holding_key_click)) == "<class 'tkinter.Entry'>"):
                            key_click = widget_holding_key_click.get()
                            if(key_click==""):
                                successful_add=False
                                break
                        elif(str(type(widget_holding_key_click)) == "<class 'tkinter.Label'>"):
                            key_click=""
                        else:
                            key_click = widget_holding_key_click.getvar(str(widget_holding_key_click.cget("textvariable")))
                        
                        
                        time_hold_repeat_frame = list_of_items[index][i+1]
                        time_hold = time_hold_repeat_frame.winfo_children()[1].get()
                        times_repeat = time_hold_repeat_frame.winfo_children()[4].get()

                        if(time_hold=="" or times_repeat==""):
                            successful_add=False
                            break

                        set_delay_frame = list_of_items[index][i+2]
                        delay = set_delay_frame.winfo_children()[1].get()
                        if(delay==""):
                            successful_add=False
                            break

                        command_list.append([key_click,time_hold,times_repeat,delay])

                    if(not successful_add):
                       continue
                        
                    obj = Macro(toggle_key,loop,command_list)
                    list_of_active_items.append(obj)
    else: # changing mode to edit
        change_mode_button.config(text="Change Mode to " + current_mode)
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
        type_selector_label.configure(state="normal")
        type_selector.configure(state="normal")
    #update current_mode_label
    current_mode_label.config(text="Current Mode: " + current_mode)

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
        if(item.type==command_type.Mouse_Click):
            mouse.click(button=item.key_click)
        elif(item.type==command_type.Keyboard_Press):
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
            for i in range(command[3]):
                if(not item.active):
                    return
                if(command[0]==command_type.Mouse_Click): # command is (type, key_click, hold time, repeat x times, delay)
                    mouse.press(button=command[1])
                    time.sleep(command[2]/1000.0)
                    mouse.release(button=command[1])
                    # mouse.click(button=command[1])
                elif(command[0]==command_type.Wait):
                    time.sleep(command[2]/1000.0)
                elif(command[0]==command_type.Keyboard_Press):
                    # print(item.key_click)
                    if(command[1][-1] == " "): #space at end means need a shift key
                        keyboard.press("shift")
                        keyboard.press(command[1][0])
                        time.sleep(command[2]/1000.0)
                        keyboard.release("shift")
                        keyboard.release(command[1][0])
                    else:
                        # keyboard.send(command[1])
                        keyboard.press(command[1])
                        time.sleep(command[2]/1000.0)
                        keyboard.release(command[1])
                        
                # print("clicked")
                time.sleep(command[4]/1000.0)
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
    global number_of_frames_in_macro_command
    index_of_item_deleting=-1
    number_of_commands=1
    #finding the index in list of items of the item we are deleting and moving items below up
    for list in list_of_items:
        if(list[0].grid_info()["row"] <= current_row):
            index_of_item_deleting+=1
        else:
            number_of_commands = (len(list_of_items[index_of_item_deleting])-5)//number_of_frames_in_macro_command
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

#makes sure can only type numbers in a textbox
def validate_so_only_numbers(S):
    if(S.isnumeric()):
        return True
    return False

#makes canvas take up all space mainframe does so can scroll through it. Is called when mainframe's size changes (from additions/deletions).
def update_canvas_for_scroll(canvas):
    canvas.configure(scrollregion=canvas.bbox("all"))

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
    elif (new_selection=="Keyboard"):
        click_key_string = StringVar()
        click_key_string.trace_add("write", lambda name, index, mode: strip_string_variable(click_key_string))
        click_key_textbox=Entry(current_frame,fg="white", bg="black",font=("Arial",15), insertbackground="white", width=14, textvariable=click_key_string)
        click_key_textbox.bind("<Key>",store_key_in_textbox)
        click_key_textbox.grid(row=0,column=2, padx=5)
    elif(new_selection=="Wait"):
        label_so_dont_crash = Label(current_frame,bg="black", text="")
        label_so_dont_crash.grid(row=0, column=2, padx=5)

#add new command
def add_new_command(current_row):
    global list_of_items
    global number_of_frames_in_macro_command
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

    number_of_commands = (len(list_of_items[index_of_item_adding])-5)//number_of_frames_in_macro_command + 1

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
    mouse_or_keyboard_selector = OptionMenu(set_click_key_frame, mouse_or_keyboard_selector_string, "Mouse","Keyboard","Wait", command= lambda new_selection: mouse_or_keyboard_selector_update(new_selection,set_click_key_frame))
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

    #Set Time Hold For
    set_time_hold_repeat_frame = Frame(mainframe)
    set_time_hold_repeat_frame.grid(row=current_row,column=1, sticky=(N,E,S,W))
    set_time_hold_repeat_frame.config(background="black")
    list_of_items[index_of_item_adding].append(set_time_hold_repeat_frame)
    
    set_time_hold_label = Label(set_time_hold_repeat_frame,text="Hold for: ",fg="white", bg="black",font=("Arial",15))
    set_time_hold_label.grid(row=0,column=0)
    
    only_numbers_validate_command = (set_time_hold_repeat_frame.register(validate_so_only_numbers),"%S")
    set_time_hold_textbox=Entry(set_time_hold_repeat_frame,fg="white", bg="black",font=("Arial",15), insertbackground="white", width=5, validate="key", validatecommand=only_numbers_validate_command)
    set_time_hold_textbox.grid(row=0,column=1)
    set_time_hold_textbox.insert(0,"0")

    set_time_hold_seconds_label = Label(set_time_hold_repeat_frame,text="ms",fg="white", bg="black",font=("Arial",15))
    set_time_hold_seconds_label.grid(row=0,column=2)
    
    #Set Times Repeat
    set_time_repeat_label = Label(set_time_hold_repeat_frame,text="Run: ",fg="white", bg="black",font=("Arial",15))
    set_time_repeat_label.grid(row=0,column=3, padx=(5,0))

    set_time_repeat_textbox=Entry(set_time_hold_repeat_frame,fg="white", bg="black",font=("Arial",15), insertbackground="white", width=5, validate="key", validatecommand=only_numbers_validate_command)
    set_time_repeat_textbox.grid(row=0,column=4)
    set_time_repeat_textbox.insert(0,"1")

    set_time_repeat_times_label = Label(set_time_hold_repeat_frame,text="times",fg="white", bg="black",font=("Arial",15))
    set_time_repeat_times_label.grid(row=0,column=5)

    #Set Delay
    set_delay_frame = Frame(mainframe)
    set_delay_frame.grid(row=current_row,column=2, sticky=(N,E,S,W))
    set_delay_frame.config(background="black")
    list_of_items[index_of_item_adding].append(set_delay_frame)

    set_delay_label = Label(set_delay_frame,text="Delay: ",fg="white", bg="black",font=("Arial",15))
    set_delay_label.grid(row=0,column=0,padx=(5,0))

    set_delay_validate_command = (set_delay_frame.register(validate_so_only_numbers),"%S")
    set_delay_textbox=Entry(set_delay_frame,fg="white", bg="black",font=("Arial",15), insertbackground="white", width=5, validate="key", validatecommand=set_delay_validate_command)
    set_delay_textbox.grid(row=0,column=1)

    set_delay_seconds_label = Label(set_delay_frame,text="ms",fg="white", bg="black",font=("Arial",15))
    set_delay_seconds_label.grid(row=0,column=2)

    #delete button
    delete_command_button_frame = Frame(mainframe)
    delete_command_button_frame.grid(row=current_row,column=3, sticky=(N,E,S,W))
    delete_command_button_frame.config(background="black")
    list_of_items[index_of_item_adding].append(delete_command_button_frame)

    delete_command_button = Button(delete_command_button_frame,text="Delete Command", fg="white", bg="black", activeforeground="white",activebackground="black")
    delete_command_button.grid(row=0, column=0, padx=5)
    delete_command_button.configure(command=lambda: delete_macro_command(delete_command_button_frame.grid_info()["row"]))

def delete_macro_command(row_to_delete):
    global list_of_items
    global number_of_frames_in_macro_command
    #finding index of where adding
    index_of_macro =-1
    #finding the index in list of items of the item we are deleting and moving items below up
    for list in list_of_items:
        if(list[0].grid_info()["row"] + 2 == row_to_delete and len(list) == 5 + number_of_frames_in_macro_command): #if only one command left
            return
        elif(list[0].grid_info()["row"] <= row_to_delete):
            index_of_macro+=1
        else:
            for frame in list:
                if(frame.grid_info()["row"] > row_to_delete):
                    frame.grid_configure(row=frame.grid_info()["row"] - 1) 
    
    #moving add frame
    add_frame.grid_configure(row=add_frame.grid_info()["row"] - 1)
    #moving add new command button
    list_of_items[index_of_macro][4].grid_configure(row=list_of_items[index_of_macro][4].grid_info()["row"] - 1)
    
    index_of_command_deleting =-1
    for index in range(5, len(list_of_items[index_of_macro]),number_of_frames_in_macro_command):
        if(list_of_items[index_of_macro][index].grid_info()["row"] == row_to_delete):
            index_of_command_deleting=index
        if(list_of_items[index_of_macro][index].grid_info()["row"] > row_to_delete): # this command is below the command want to delete
            #updating label for this command
            list_of_items[index_of_macro][index].winfo_children()[0].configure(text = str((index-5)//number_of_frames_in_macro_command) + ". Click Key: ")
            #updating positions for all frames in this command
            for command_frame_index in range(index,index+number_of_frames_in_macro_command):
                frame = list_of_items[index_of_macro][command_frame_index]
                frame.grid_configure(row=frame.grid_info()["row"] - 1)

    #deleting command want to and removing from list
    for i in range(number_of_frames_in_macro_command):
        frame = list_of_items[index_of_macro][index_of_command_deleting]
        frame.grid_forget()
        frame.destroy()
        del list_of_items[index_of_macro][index_of_command_deleting]

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
        set_delay_label.grid(row=0,column=0,padx=(5,0))

        set_delay_validate_command = (set_delay_frame.register(validate_so_only_numbers),"%S")
        set_delay_textbox=Entry(set_delay_frame,fg="white", bg="black",font=("Arial",15), insertbackground="white", width=5, validate="key", validatecommand=set_delay_validate_command)
        set_delay_textbox.grid(row=0,column=1)

        set_delay_seconds_label = Label(set_delay_frame,text="ms",fg="white", bg="black",font=("Arial",15))
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
        mouse_or_keyboard_selector = OptionMenu(set_click_key_frame, mouse_or_keyboard_selector_string, "Mouse","Keyboard","Wait", command= lambda new_selection: mouse_or_keyboard_selector_update(new_selection,set_click_key_frame))
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

        #Set Time Hold For
        set_time_hold_repeat_frame = Frame(mainframe)
        set_time_hold_repeat_frame.grid(row=current_row+2,column=1, sticky=(N,E,S,W))
        set_time_hold_repeat_frame.config(background="black")
        list_of_items[len(list_of_items)-1].append(set_time_hold_repeat_frame)

        set_time_hold_label = Label(set_time_hold_repeat_frame,text="Hold for: ",fg="white", bg="black",font=("Arial",15))
        set_time_hold_label.grid(row=0,column=0)

        only_numbers_validate_command = (set_time_hold_repeat_frame.register(validate_so_only_numbers),"%S")
        set_time_hold_textbox=Entry(set_time_hold_repeat_frame,fg="white", bg="black",font=("Arial",15), insertbackground="white", width=5, validate="key", validatecommand=only_numbers_validate_command)
        set_time_hold_textbox.grid(row=0,column=1)
        set_time_hold_textbox.insert(0,"0")#todo -> might need to change to 1? I don't think so, but I will leave this comment in case becomes a problem.

        set_time_hold_seconds_label = Label(set_time_hold_repeat_frame,text="ms",fg="white", bg="black",font=("Arial",15))
        set_time_hold_seconds_label.grid(row=0,column=2)

        #Set Times Repeat
        set_time_repeat_label = Label(set_time_hold_repeat_frame,text="Run: ",fg="white", bg="black",font=("Arial",15))
        set_time_repeat_label.grid(row=0,column=3, padx=(5,0))

        set_time_repeat_textbox=Entry(set_time_hold_repeat_frame,fg="white", bg="black",font=("Arial",15), insertbackground="white", width=5, validate="key", validatecommand=only_numbers_validate_command)
        set_time_repeat_textbox.grid(row=0,column=4)
        set_time_repeat_textbox.insert(0,"1")

        set_time_repeat_times_label = Label(set_time_hold_repeat_frame,text="times",fg="white", bg="black",font=("Arial",15))
        set_time_repeat_times_label.grid(row=0,column=5)

        #Set Delay
        set_delay_frame = Frame(mainframe)
        set_delay_frame.grid(row=current_row+2,column=2, sticky=(N,E,S,W))
        set_delay_frame.config(background="black")
        list_of_items[len(list_of_items)-1].append(set_delay_frame)

        set_delay_label = Label(set_delay_frame,text="Delay: ",fg="white", bg="black",font=("Arial",15))
        set_delay_label.grid(row=0,column=0,padx=(5,0))

        set_delay_validate_command = (set_delay_frame.register(validate_so_only_numbers),"%S")
        set_delay_textbox=Entry(set_delay_frame,fg="white", bg="black",font=("Arial",15), insertbackground="white", width=5, validate="key", validatecommand=set_delay_validate_command)
        set_delay_textbox.grid(row=0,column=1)

        set_delay_seconds_label = Label(set_delay_frame,text="ms",fg="white", bg="black",font=("Arial",15))
        set_delay_seconds_label.grid(row=0,column=2)

        #delete button
        delete_command_button_frame = Frame(mainframe)
        delete_command_button_frame.grid(row=current_row+2,column=3, sticky=(N,E,S,W))
        delete_command_button_frame.config(background="black")
        list_of_items[len(list_of_items)-1].append(delete_command_button_frame)

        delete_command_button = Button(delete_command_button_frame,text="Delete Command", fg="white", bg="black", activeforeground="white",activebackground="black")
        delete_command_button.grid(row=0, column=0, padx=5)

        #add another command button
        add_another_command_frame = Frame(mainframe)
        add_another_command_frame.grid(row=current_row+3,column=0, sticky=(N,E,S,W))
        add_another_command_frame.config(background="black")
        list_of_items[len(list_of_items)-1].insert(4,add_another_command_frame) # insert at 4 so that all command frames are at the end

        add_another_command_button = Button(add_another_command_frame,text="Add Another Command", command=lambda: add_new_command(add_another_command_frame.grid_info()["row"]), fg="white", bg="black", activeforeground="white",activebackground="black")
        add_another_command_button.grid(row=0, column=0)

        #setting up delete button
        delete_button.configure(command=lambda: delete_macro(type_delete_frame.grid_info()["row"]))
        delete_command_button.configure(command=lambda: delete_macro_command(delete_command_button_frame.grid_info()["row"]))



#---setting up window---
window = Tk() # instantiates an instance of a window
window.title("Macro App") # title of window
# icon = PhotoImage(file='mouseicon.png') # turning image into format tkinter can use. HAS TO BE PNG
# window.iconphoto(True, icon)
window.geometry("1100x400") # initial size of window

#---setting up canvas, scrollbar and mainframe---
canvas=Canvas(window, background='black',highlightthickness=0) # highlightthickness=0 prevents a white border around the screen
mainframe = Frame(canvas, background="black")
vbar=Scrollbar(window,orient=VERTICAL,command=canvas.yview)
canvas.config(yscrollcommand=vbar.set)  #sets canvas to scroll using the vbar

#use pack here because then don't have to set stuff with window.column/row configure and is just overall easier.
vbar.pack(side="right", fill="y") #basically vbar.grid(row=0, column=1,sticky=(N,S))
canvas.pack(side="left", fill="both", expand=True) # basically canvas.grid(row=0,column=0, sticky=(N,E,S,W))

canvas.create_window(0,0, window=mainframe, anchor="nw") #0,0 means make the window in the top left; anchor=nw makes mainframe go to top left like if grid 0,0
mainframe.bind("<Configure>", lambda event, canvas=canvas: update_canvas_for_scroll(canvas)) # will call updater when mainframe's width/height changes. 'event' contains width/height info but not needed.

#---modes---
current_mode = "Edit"
#Text
current_mode_label = Label(mainframe, text="Current Mode: " + current_mode, fg="white", bg="black",font=("Arial",15))
current_mode_label.grid(row=0,column=0)
#Button to Change
change_mode_button = Button(mainframe, text="Change Mode to " + "Running", command=change_mode, fg="white", bg="black", activeforeground="white",activebackground="black",font=("Arial",15))
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
number_of_frames_in_macro_command=4

#---whatever---
#adds spacing to each widget
for child in mainframe.winfo_children(): 
    child.grid_configure(padx=5, pady=5)

keyboard.on_press(clicked_key) # activates keyboard
window.mainloop() # activates the window