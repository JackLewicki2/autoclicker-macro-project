from tkinter import *
from tkinter import filedialog
import keyboard
import mouse
import time
import threading
from enum import Enum
#---classes---
class command_type(Enum):
    Mouse_Click=1
    Keyboard_Press=2
    Wait=3
    Text=4
    Move_Mouse=5

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

class Macro: #obj = Macro(type_of_command, toggle_key,loop,command_list)
    def __init__(self,toggle_key,loop, command_list):
        self.toggle_key = toggle_key
        self.loop=loop
        self.command_list=[]
        for command in command_list:
            if(command[0]==command_type.Text): #[type_of_command, text_in_textbox, time_per_char, times_repeat]
                type=command[0]
                character_list=[]
                for character in command[1]:
                   if(character in shift_symbols):
                        if(character=="+"):
                            character="="
                        character_list.append(character.lower()+" ")  # add space at the end to indicate needs a shift key
                   elif(character==" "):
                        character_list.append("space")
                   else:
                        character_list.append(character)
                time_per_char=int(command[2])
                times_repeat=int(command[3])
                self.command_list.append([type, character_list, time_per_char, times_repeat,0])
            elif(command[0]==command_type.Move_Mouse):
                type=command[0]
                isAbsolute=command[1]
                x=int(command[2])
                y=int(command[3])
                duration=int(command[4])
                self.command_list.append([type, x, y, 1, 0, isAbsolute, duration])
            else:
                if(command[0]==command_type.Wait):
                    key_click=""
                elif(command[0]==command_type.Mouse_Click): # if is a mouse press
                    key_click = command[1].split(" ")[0].lower()
                elif(command[0]==command_type.Keyboard_Press): # if is a keyboard press
                    if(command[1] in shift_symbols):
                        if(command[1]=="+"):
                            command[1]="="
                        key_click = command[1].lower() + " " # add space at the end to indicate needs a shift key
                    else:
                        key_click = command[1]
            
                type=command[0]
                time_hold=int(command[2])
                times_repeat=int(command[3])
                delay=int(command[4])

                if(delay==0): # bad things happen when delay=0
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
    global num_caps_lock_presses
    if(current_mode=="Edit"): # changing mode to running
        num_caps_lock_presses=0
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
        file_load_button.configure(state="disabled")
        file_save_button.configure(state="disabled")

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
                else: # macro
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
                        widget_holding_type = key_click_frame.winfo_children()[1]
                        type_of_command_string = widget_holding_type.getvar(str(widget_holding_type.cget("textvariable")))
                        widget_holding_key_click = key_click_frame.winfo_children()[2]
                        
                        if(type_of_command_string=="Text"):
                            type_of_command = command_type.Text
                            text_in_textbox = widget_holding_key_click.get()

                            if(text_in_textbox==""):
                                successful_add=False
                                break

                            time_hold_repeat_frame = list_of_items[index][i+1]
                            time_per_char = time_hold_repeat_frame.winfo_children()[1].get()

                            if(time_per_char==""):
                                successful_add=False
                                break

                            set_delay_frame = list_of_items[index][i+2]
                            times_repeat = set_delay_frame.winfo_children()[1].get()
                            if(times_repeat==""):
                                successful_add=False
                                break
                            
                            command_list.append([type_of_command, text_in_textbox, time_per_char, times_repeat])
                        elif(type_of_command_string=="Move Mouse"):
                            type_of_command=command_type.Move_Mouse
                            isAbsolute=widget_holding_key_click.getvar(str(widget_holding_key_click.cget("textvariable")))=="Absolute Position"
                            time_hold_repeat_frame = list_of_items[index][i+1]
                            x = time_hold_repeat_frame.winfo_children()[1].get()
                            if(x==""):
                                    successful_add=False
                                    break
                            y = time_hold_repeat_frame.winfo_children()[3].get()
                            if(y==""):
                                    successful_add=False
                                    break
                            try:
                                int(x)
                                int(y)
                            except:
                                successful_add=False
                                break
                            duration = time_hold_repeat_frame.winfo_children()[5].get()
                            if(duration==""):
                                    successful_add=False
                                    break
                            command_list.append([type_of_command, isAbsolute, x, y, duration])
                        else:
                            if(type_of_command_string=="Keyboard"):
                                type_of_command=command_type.Keyboard_Press
                                key_click = widget_holding_key_click.get()
                                if(key_click==""):
                                    successful_add=False
                                    break
                            elif(type_of_command_string=="Wait"):
                                type_of_command=command_type.Wait
                                key_click=""
                            elif(type_of_command_string=="Mouse"):
                                type_of_command=command_type.Mouse_Click
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
                            
                            command_list.append([type_of_command, key_click,time_hold,times_repeat,delay])

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
        file_load_button.configure(state="normal")
        file_save_button.configure(state="normal")
    #update current_mode_label
    current_mode_label.config(text="Current Mode: " + current_mode)

#clicked a key
def clicked_key(event):
    global most_recent_key_pressed
    global num_caps_lock_presses
    most_recent_key_pressed=event.name
    if(most_recent_key_pressed=="caps lock"):
        num_caps_lock_presses+=1
    else:
        num_caps_lock_presses=0
    if(current_mode=="Running"):
        if(num_caps_lock_presses>=3):
            num_caps_lock_presses=0
            change_mode()
        else:
            for item in list_of_active_items:
                if(item.toggle_key==event.name):
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
                keyboard.send(item.key_click[0].lower())
                # if (not keyboard.is_pressed("shift")):
                keyboard.release("shift")
            else:
                keyboard.press(item.key_click)
                # if(not keyboard.is_pressed(item.key_click)): # Needed if command[1] is shift
                keyboard.release(item.key_click)
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
                    time.sleep(command[2]/1000.0) # I don't think the if(not is pressed) is needed with the mouse
                    mouse.release(button=command[1])
                elif(command[0]==command_type.Wait):
                    time.sleep(command[2]/1000.0)
                elif(command[0]==command_type.Keyboard_Press):
                    if(command[1][-1] == " "): #space at end means need a shift key
                        keyboard.press("shift+"+command[1][0])
                        time.sleep(command[2]/1000.0)
                        # if(not keyboard.is_pressed("shift")): # this doesn't count the shift it pressed down right above; just if actual shift is pressed down
                        keyboard.release("shift")
                        # if(not keyboard.is_pressed(command[1][0])):
                        keyboard.release(command[1][0])
                    else:
                        # keyboard.send(command[1])
                        keyboard.press(command[1])
                        time.sleep(command[2]/1000.0)
                        # if(not keyboard.is_pressed(command[1])): # Needed if command[1] is shift
                        keyboard.release(command[1])
                elif(command[0]==command_type.Text):#[type, character_list, time_per_char, times_repeat, 0]
                    for character in command[1]:
                        if(not item.active):
                            return
                        if(character[-1] == " "): #space at end means need a shift key
                            keyboard.press("shift+"+character[0])
                            # if(not keyboard.is_pressed("shift")): # this doesn't count the shift it pressed down right above; just if actual shift is pressed down
                            keyboard.release("shift")
                            # if(not keyboard.is_pressed(command[1][0])):
                            keyboard.release(character[0])
                        else:
                            keyboard.press(character)
                            # if(not keyboard.is_pressed(character)): # Needed if command[1] is shift
                            keyboard.release(character)
                        time.sleep(command[2]/1000.0)
                elif(command[0]==command_type.Move_Mouse): #[type, x, y, 1, 0, isAbsolute, duration]
                    mouse.move(command[1],command[2],command[5],command[6]/1000.0)

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

    #moving the add_frame and file_load_save_frame up
    add_frame.grid_configure(row=add_frame.grid_info()["row"] -2)
    file_load_save_frame.grid_configure(row=file_load_save_frame.grid_info()["row"] -2)

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

    #moving the add_frame and file_load_save_frame up
    add_frame.grid_configure(row=add_frame.grid_info()["row"] - 3 - number_of_commands)
    file_load_save_frame.grid_configure(row=file_load_save_frame.grid_info()["row"] - 3 - number_of_commands)

#gets rid of the ' ' when type space key in an entry box
def strip_string_variable(string_variable):
    string_variable.set(string_variable.get().strip())

#sets toggle key and click key
def store_key_in_textbox(event):
    global most_recent_key_pressed
    print("most recent pressed:",most_recent_key_pressed) #I have no idea why but having this uncommented fixes a bug with hitting different keys too fast
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

#makes sure can only type numbers (negative okay) in a textbox
def validate_so_only_numbers_or_negative(S):
    if(S.isnumeric() or "-" in S):
        return True
    return False

def record_position(set_x_textbox, set_y_textbox):
    mouse.wait(button="left")
    position = mouse.get_position()
    set_x_textbox.delete(0,END)
    set_x_textbox.insert(0,position[0])
    set_y_textbox.delete(0,END)
    set_y_textbox.insert(0,position[1])

#makes canvas take up all space mainframe does so can scroll through it. Is called when mainframe's size changes (from additions/deletions).
def update_canvas_for_scroll(canvas):
    canvas.configure(scrollregion=canvas.bbox("all"))

#updates frame to be mouse or keyboard selection
def mouse_or_keyboard_selector_update(isAutoclicker, new_selection, set_click_key_frame,set_time_hold_repeat_frame,set_delay_frame):
    old_thing = set_click_key_frame.winfo_children()[2] 
    old_thing.grid_forget()
    old_thing.destroy()
    if(not isAutoclicker):
        for child in set_time_hold_repeat_frame.winfo_children(): 
            child.grid_forget()
            child.destroy()
        for child in set_delay_frame.winfo_children(): 
            child.grid_forget()
            child.destroy()
    if(new_selection=="Text"):
        #text input textbox    
        text_textbox=Entry(set_click_key_frame,fg="white", bg="black",font=("Arial",15), insertbackground="white", width=17)
        text_textbox.grid(row=0,column=2)
        
        #time between button presses
        time_between_button_presses_label1 = Label(set_time_hold_repeat_frame,text="Type a character every ",fg="white", bg="black",font=("Arial",15))
        time_between_button_presses_label1.grid(row=0, column=0) #padx=(19,0) would align with the Run entrybox of other commands

        set_time_between_presses_validate_command = (set_time_hold_repeat_frame.register(validate_so_only_numbers),"%S")
        set_time_between_presses_textbox=Entry(set_time_hold_repeat_frame,fg="white", bg="black",font=("Arial",15), insertbackground="white", width=5, validate="key", validatecommand=set_time_between_presses_validate_command)
        set_time_between_presses_textbox.grid(row=0,column=1)
        
        time_between_button_presses_label2= Label(set_time_hold_repeat_frame, text="ms",fg="white", bg="black",font=("Arial",15))
        time_between_button_presses_label2.grid(row=0, column=2)
        
        #set time repeat
        set_time_repeat_label = Label(set_delay_frame,text="Run: ",fg="white", bg="black",font=("Arial",15))
        set_time_repeat_label.grid(row=0,column=0, padx=(5,0))

        only_numbers_validate_command = (set_delay_frame.register(validate_so_only_numbers),"%S")
        set_time_repeat_textbox=Entry(set_delay_frame,fg="white", bg="black",font=("Arial",15), insertbackground="white", width=5, validate="key", validatecommand=only_numbers_validate_command)
        set_time_repeat_textbox.grid(row=0,column=1)
        set_time_repeat_textbox.insert(0,"1")

        set_time_repeat_times_label = Label(set_delay_frame,text="times",fg="white", bg="black",font=("Arial",15))
        set_time_repeat_times_label.grid(row=0,column=2)
    elif(new_selection=="Move Mouse"):
        #option menu for absolute/relative position
        move_mouse_absolute_relative_selector_string=StringVar()
        move_mouse_absolute_relative_selector = OptionMenu(set_click_key_frame, move_mouse_absolute_relative_selector_string, "Absolute Position", "Relative Position")
        move_mouse_absolute_relative_selector.configure(bg="black", fg="white", activebackground="black",activeforeground="white")
        move_mouse_absolute_relative_selector["menu"].config(bg="black",fg="white")
        move_mouse_absolute_relative_selector_string.set("Absolute Position")
        move_mouse_absolute_relative_selector.grid(row=0, column=2, padx=5)
        
        #label/entry for x (can be negative)
        set_x_label = Label(set_time_hold_repeat_frame,text="x: ",fg="white", bg="black",font=("Arial",15))
        set_x_label.grid(row=0,column=0)
        
        only_numbers_or_negative_validate_command = (set_time_hold_repeat_frame.register(validate_so_only_numbers_or_negative),"%S")
        set_x_textbox=Entry(set_time_hold_repeat_frame,fg="white", bg="black",font=("Arial",15), insertbackground="white", width=5, validate="key", validatecommand=only_numbers_or_negative_validate_command)
        set_x_textbox.grid(row=0,column=1)
        #label/entry for y (can be negative)
        set_y_label = Label(set_time_hold_repeat_frame,text="y: ",fg="white", bg="black",font=("Arial",15))
        set_y_label.grid(row=0,column=2,padx=(5,0))
        
        set_y_textbox=Entry(set_time_hold_repeat_frame,fg="white", bg="black",font=("Arial",15), insertbackground="white", width=5, validate="key", validatecommand=only_numbers_or_negative_validate_command)
        set_y_textbox.grid(row=0,column=3)
        #label entry for time
        set_move_time_label = Label(set_time_hold_repeat_frame,text="Duration: ",fg="white", bg="black",font=("Arial",15))
        set_move_time_label.grid(row=0,column=4,padx=(5,0))
        
        set_move_time_validate_command = (set_time_hold_repeat_frame.register(validate_so_only_numbers),"%S")
        set_move_time_textbox=Entry(set_time_hold_repeat_frame,fg="white", bg="black",font=("Arial",15), insertbackground="white", width=5, validate="key", validatecommand=set_move_time_validate_command)
        set_move_time_textbox.grid(row=0,column=5)
        
        set_move_time_units_label = Label(set_time_hold_repeat_frame,text="ms",fg="white", bg="black",font=("Arial",15))
        set_move_time_units_label.grid(row=0,column=6)

        #button to record then set position from click
        record_position_button = Button(set_delay_frame,text="Record Mouse x/y on Click", fg="white", bg="black", activeforeground="white",activebackground="black")
        record_position_button.grid(row=0, column=0, padx=(10,5))
        record_position_button.configure(command=lambda: record_position(set_x_textbox, set_y_textbox))
    else:
        if(new_selection=="Mouse"):
            mouse_button_selector_string=StringVar()
            mouse_button_selector = OptionMenu(set_click_key_frame, mouse_button_selector_string, "Left Click","Right Click", "Middle Click")
            mouse_button_selector.configure(bg="black", fg="white", activebackground="black",activeforeground="white")
            mouse_button_selector["menu"].config(bg="black",fg="white")
            mouse_button_selector_string.set("Left Click")
            mouse_button_selector.grid(row=0, column=2, padx=5)
        elif (new_selection=="Keyboard"):
            click_key_string = StringVar()
            click_key_string.trace_add("write", lambda name, index, mode: strip_string_variable(click_key_string))
            click_key_textbox=Entry(set_click_key_frame,fg="white", bg="black",font=("Arial",15), insertbackground="white", width=14, textvariable=click_key_string)
            if(isAutoclicker):
                click_key_textbox.configure(width=12)
            click_key_textbox.bind("<Key>",store_key_in_textbox)
            click_key_textbox.grid(row=0,column=2, padx=5)
        elif(new_selection=="Wait"):
            label_so_dont_crash = Label(set_click_key_frame,bg="black", text="")
            label_so_dont_crash.grid(row=0, column=2, padx=5)
            
        if(not isAutoclicker):
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
            set_delay_label = Label(set_delay_frame,text="Delay: ",fg="white", bg="black",font=("Arial",15))
            set_delay_label.grid(row=0,column=0,padx=(5,0))

            set_delay_validate_command = (set_delay_frame.register(validate_so_only_numbers),"%S")
            set_delay_textbox=Entry(set_delay_frame,fg="white", bg="black",font=("Arial",15), insertbackground="white", width=5, validate="key", validatecommand=set_delay_validate_command)
            set_delay_textbox.grid(row=0,column=1)

            set_delay_seconds_label = Label(set_delay_frame,text="ms",fg="white", bg="black",font=("Arial",15))
            set_delay_seconds_label.grid(row=0,column=2,padx=(0,5))

def load_file():
    global list_of_items
    global type_selector_string
    global number_of_frames_in_macro_command

    file_path = filedialog.askopenfilename(title = "Choose file to load", filetypes=(("Text Files",".txt"),))
    if(file_path == ""):
        return
    file = open(file_path, "r")
    items = file.read().split("\n")
    for item in items:
        item_data = item.split(" ")
        if(item_data[2]=="Autoclicker"):
            #adding the autoclicker
            type_selector_string.set("Autoclicker")
            add_new()

            item_just_added = list_of_items[len(list_of_items)-1]
            #setting active checkbox
            checkbox_name_frame = item_just_added[0]
            if(item_data[0] == "True"):
                checkbox_name_frame.winfo_children()[1].select()
            #setting name
            checkbox_name_frame.winfo_children()[3].insert(0, item_data[1].replace("_$$$_"," "))
            
            #setting toggle key
            toggle_key_frame=item_just_added[2]
            if(item_data[3]!="_"):
                toggle_key_frame.winfo_children()[1].insert(0, item_data[3].replace("_"," "))
            else:
                toggle_key_frame.winfo_children()[1].insert(0, item_data[3])

            #setting click key
            set_click_key_frame=item_just_added[3]
            type_selector = set_click_key_frame.winfo_children()[1]
            type_selector.setvar(name=str(type_selector.cget("textvariable")), value=item_data[4])
            mouse_or_keyboard_selector_update(True, item_data[4], set_click_key_frame, set_click_key_frame, set_click_key_frame)
            if (item_data[4]=="Mouse"):
                button_click_selector = set_click_key_frame.winfo_children()[2]
                button_click_selector.setvar(name=str(button_click_selector.cget("textvariable")), value=item_data[5].replace("_"," "))
            elif (item_data[4]=="Keyboard"):
                if(item_data[5]!="_"):
                    set_click_key_frame.winfo_children()[2].insert(0, item_data[5].replace("_"," "))
                else:
                    set_click_key_frame.winfo_children()[2].insert(0, item_data[5])

            #setting delay
            set_delay_frame=item_just_added[4]
            set_delay_frame.winfo_children()[1].insert(0, item_data[6])
        elif(item_data[2]=="Macro"):
            #adding the macro
            type_selector_string.set("Macro")
            add_new()

            item_just_added = list_of_items[len(list_of_items)-1]
            #setting active checkbox
            checkbox_name_frame = item_just_added[0]
            if(item_data[0] == "True"):
                checkbox_name_frame.winfo_children()[1].select()
            #setting name
            checkbox_name_frame.winfo_children()[3].insert(0, item_data[1].replace("_$$$_"," "))
            
            #setting toggle key
            toggle_key_frame=item_just_added[2]
            if(item_data[3]!="_"):
                toggle_key_frame.winfo_children()[1].insert(0, item_data[3].replace("_"," "))
            else:
                toggle_key_frame.winfo_children()[1].insert(0, item_data[3])

            #setting loop checkbox
            loop_frame = item_just_added[3]
            if(item_data[4] == "True"):
                loop_frame.winfo_children()[1].select()

            for command_index in range(5, len(item_data)):
                #calling add new command if have more than one command
                if(command_index>5):
                    add_new_command(1+item_just_added[5 + (command_index-6)*number_of_frames_in_macro_command].grid_info()["row"])

                command_data = item_data[command_index].split("_$$$_")
                
                #setting click key selector and getting all the frames
                set_click_key_frame=item_just_added[5 + (command_index-5)*number_of_frames_in_macro_command]
                set_time_hold_repeat_frame=item_just_added[6 + (command_index-5)*number_of_frames_in_macro_command]
                set_delay_frame=item_just_added[7 + (command_index-5)*number_of_frames_in_macro_command]
                type_selector = set_click_key_frame.winfo_children()[1]
                type_selector.setvar(name=str(type_selector.cget("textvariable")), value=command_data[0].replace("_"," "))
                mouse_or_keyboard_selector_update(False, command_data[0].replace("_"," "), set_click_key_frame, set_time_hold_repeat_frame,set_delay_frame)
                if(command_data[0]=="Text"):
                    text_textbox = set_click_key_frame.winfo_children()[2]
                    text_textbox.insert(0,command_data[1].replace("_$$$$$_"," "))

                    time_between_button_presses_textbox = set_time_hold_repeat_frame.winfo_children()[1]
                    time_between_button_presses_textbox.insert(0,command_data[2])

                    times_repeat_textbox = set_delay_frame.winfo_children()[1]
                    times_repeat_textbox.delete(0,END)
                    times_repeat_textbox.insert(0, command_data[3])
                elif(command_data[0]=="Move_Mouse"): #Type, absolute, x, y, duration
                    absolute_selector = set_click_key_frame.winfo_children()[2]
                    absolute_selector.setvar(name=str(absolute_selector.cget("textvariable")), value=command_data[1].replace("_"," "))
                    
                    x_textbox = set_time_hold_repeat_frame.winfo_children()[1]
                    x_textbox.insert(0,command_data[2])
                    
                    y_textbox = set_time_hold_repeat_frame.winfo_children()[3]
                    y_textbox.insert(0,command_data[3])

                    duration_textbox = set_time_hold_repeat_frame.winfo_children()[5]
                    duration_textbox.insert(0,command_data[4])
                else:
                    if (command_data[0]=="Mouse"):
                        button_click_selector = set_click_key_frame.winfo_children()[2]
                        button_click_selector.setvar(name=str(button_click_selector.cget("textvariable")), value=command_data[1].replace("_"," "))
                    elif (command_data[0]=="Keyboard"):
                        if(command_data[1]!="_"):
                            set_click_key_frame.winfo_children()[2].insert(0, command_data[1].replace("_"," "))
                        else:
                            set_click_key_frame.winfo_children()[2].insert(0, command_data[1])
                    elif(command_data[0]=="Wait"):
                        pass # don't need to do anything

                    #setting time hold for
                    set_time_hold_repeat_frame.winfo_children()[1].delete(0, END)
                    set_time_hold_repeat_frame.winfo_children()[1].insert(0, command_data[2])

                    #setting time repeat
                    set_time_hold_repeat_frame.winfo_children()[4].delete(0, END)
                    set_time_hold_repeat_frame.winfo_children()[4].insert(0, command_data[3])

                    #setting delay
                    set_delay_frame.winfo_children()[1].insert(0, command_data[4])
    file.close()

def save_file():
    if(len(list_of_items)==0):
        return
    file_text=""
    for index in range(len(list_of_items)):
        file_text+=str(list_of_checkbox_variables[index].get())+" " #checkbox
        file_text+=list_of_items[index][0].winfo_children()[3].get().replace(" ","_$$$_")+" " # name
        
        if(len(list_of_items[index])==5): # length 5 means is autoclicker. A bigger length means is a macro.
            file_text+="Autoclicker "

            toggle_key_frame = list_of_items[index][2]
            toggle_key = toggle_key_frame.winfo_children()[1].get().replace(" ","_")
            file_text+=toggle_key+" "
            
            key_click_frame = list_of_items[index][3]
            widget_holding_type = key_click_frame.winfo_children()[1]
            type_of_command_string = widget_holding_type.getvar(str(widget_holding_type.cget("textvariable")))
            widget_holding_key_click = key_click_frame.winfo_children()[2]
            if(type_of_command_string=="Keyboard"):
                key_click = widget_holding_key_click.get()
                key_click = key_click.replace(" ","_")
                file_text+="Keyboard "
            elif(type_of_command_string=="Mouse"):
                key_click = widget_holding_key_click.getvar(str(widget_holding_key_click.cget("textvariable")))
                key_click = key_click.replace(" ","_")
                file_text+="Mouse "
            file_text+=key_click+" "

            set_delay_frame = list_of_items[index][4]
            delay = set_delay_frame.winfo_children()[1].get()
            file_text+=delay
        else:
            file_text+="Macro "
            
            toggle_key_frame = list_of_items[index][2]
            toggle_key = toggle_key_frame.winfo_children()[1].get()
            file_text+=toggle_key+" "
            
            loop_checkbox_frame = list_of_items[index][3]
            widget_holding_loop_checkbox = loop_checkbox_frame.winfo_children()[1]
            widget_holding_loop_checkbox.configure(state="disabled") # if havent interacted with checkbox yet will crash unless set state to disabled beforehand for some reason???
            loop = widget_holding_loop_checkbox.getvar(str(widget_holding_loop_checkbox.cget("variable")))
            widget_holding_loop_checkbox.configure(state="normal")
            if loop==1: # this is just so loop and active are both stored as True/False instead of being stored differently
                loop="True"
            else:
                loop="False"
            file_text+=loop+" "

            for i in range(5,len(list_of_items[index]),number_of_frames_in_macro_command):
                key_click_frame = list_of_items[index][i]
                widget_holding_type = key_click_frame.winfo_children()[1]
                type_of_command_string = widget_holding_type.getvar(str(widget_holding_type.cget("textvariable")))
                widget_holding_key_click = key_click_frame.winfo_children()[2]
                
                if(type_of_command_string=="Text"):
                    file_text+="Text_$$$_"

                    text= widget_holding_key_click.get().replace(" ","_$$$$$_")
                    file_text+=text+"_$$$_"

                    time_hold_repeat_frame = list_of_items[index][i+1]
                    time_between_button_presses = time_hold_repeat_frame.winfo_children()[1].get()
                    file_text+=time_between_button_presses+"_$$$_"

                    set_delay_frame = list_of_items[index][i+2]
                    times_repeat = set_delay_frame.winfo_children()[1].get()
                    file_text+=times_repeat

                elif(type_of_command_string=="Move Mouse"):
                    file_text+="Move_Mouse_$$$_"

                    absolute= widget_holding_key_click.getvar(str(widget_holding_key_click.cget("textvariable"))).replace(" ","_")
                    file_text+=absolute+"_$$$_"

                    time_hold_repeat_frame = list_of_items[index][i+1]
                    x = time_hold_repeat_frame.winfo_children()[1].get()
                    file_text+=x+"_$$$_"

                    y=time_hold_repeat_frame.winfo_children()[3].get()
                    file_text+=y+"_$$$_"

                    duration=time_hold_repeat_frame.winfo_children()[5].get()
                    file_text+=duration
                else:
                    if(type_of_command_string=="Keyboard"):
                        key_click = widget_holding_key_click.get()
                        file_text+="Keyboard_$$$_"
                    elif(type_of_command_string=="Wait"):
                        key_click=""
                        file_text+="Wait_$$$_"
                    elif(type_of_command_string=="Mouse"):
                        key_click = widget_holding_key_click.getvar(str(widget_holding_key_click.cget("textvariable")))
                        key_click = key_click.replace(" ","_")
                        file_text+="Mouse_$$$_"
                    file_text+=key_click+"_$$$_"

                    time_hold_repeat_frame = list_of_items[index][i+1]
                    time_hold = time_hold_repeat_frame.winfo_children()[1].get()
                    file_text+=time_hold+"_$$$_"
                    times_repeat = time_hold_repeat_frame.winfo_children()[4].get()
                    file_text+=times_repeat+"_$$$_"
                        
                    set_delay_frame = list_of_items[index][i+2]
                    delay = set_delay_frame.winfo_children()[1].get()
                    file_text+=delay

                if(i!=len(list_of_items[index])-number_of_frames_in_macro_command):#add a space for the next command if are not the last command
                    file_text+=" "
        if(index!=len(list_of_items)-1):#add a new line for next item if are not the last item
            file_text+="\n"

    file=filedialog.asksaveasfile(defaultextension=".txt", filetypes=[("Text File",".txt")])
    if(file is None):
        return
    file.write(file_text)
    file.close()

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

    #moving add frame and file_load_save_frame
    add_frame.grid_configure(row=add_frame.grid_info()["row"] + 1)
    file_load_save_frame.grid_configure(row=file_load_save_frame.grid_info()["row"] + 1)
    #moving add new command button
    list_of_items[index_of_item_adding][4].grid_configure(row=current_row + 1)

    #Set click key
    set_click_key_frame = Frame(mainframe)
    set_click_key_frame.grid(row=current_row,column=0, sticky=(N,E,S,W))
    set_click_key_frame.config(background="black")
    list_of_items[index_of_item_adding].append(set_click_key_frame)

    set_click_key_label = Label(set_click_key_frame,text=str(number_of_commands) + ". Click Key: ",fg="white", bg="black",font=("Arial",15))
    set_click_key_label.grid(row=0,column=0)

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
    set_delay_seconds_label.grid(row=0,column=2,padx=(0,5))

    #doing this now because have all frames in scope so can put in the lambda
    mouse_or_keyboard_selector_string=StringVar()
    mouse_or_keyboard_selector = OptionMenu(set_click_key_frame, mouse_or_keyboard_selector_string, "Mouse","Move Mouse","Keyboard","Text","Wait", command= lambda new_selection: mouse_or_keyboard_selector_update(False, new_selection,set_click_key_frame,set_time_hold_repeat_frame,set_delay_frame))
    mouse_or_keyboard_selector.configure(bg="black", fg="white", activebackground="black",activeforeground="white")
    mouse_or_keyboard_selector["menu"].config(bg="black",fg="white")
    mouse_or_keyboard_selector_string.set("Mouse")
    mouse_or_keyboard_selector.grid(row=0, column=1, padx=(0,5))

    mouse_button_selector_string=StringVar() # need this one with the thing above so is always the 2nd child of the frame
    mouse_button_selector = OptionMenu(set_click_key_frame, mouse_button_selector_string, "Left Click","Right Click", "Middle Click")
    mouse_button_selector.configure(bg="black", fg="white", activebackground="black",activeforeground="white")
    mouse_button_selector["menu"].config(bg="black",fg="white")
    mouse_button_selector_string.set("Left Click")
    mouse_button_selector.grid(row=0, column=2, padx=5)

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
    
    #moving add frame and file_load_save_frame
    add_frame.grid_configure(row=add_frame.grid_info()["row"] - 1)
    file_load_save_frame.grid_configure(row=file_load_save_frame.grid_info()["row"] - 1)
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
        #moving add_frame and file_load_save_frame down two
        add_frame.grid_configure(row=current_row+2)
        file_load_save_frame.grid_configure(row=current_row+2)
        

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
        mouse_or_keyboard_selector = OptionMenu(set_click_key_frame, mouse_or_keyboard_selector_string, "Mouse","Keyboard", command= lambda new_selection: mouse_or_keyboard_selector_update(True, new_selection,set_click_key_frame, set_click_key_frame, set_click_key_frame))
        mouse_or_keyboard_selector.configure(bg="black", fg="white", activebackground="black",activeforeground="white")
        mouse_or_keyboard_selector["menu"].config(bg="black",fg="white")
        mouse_or_keyboard_selector_string.set("Mouse")
        mouse_or_keyboard_selector.grid(row=0, column=1, padx=(0,5))

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
        set_delay_seconds_label.grid(row=0,column=2,padx=(0,5))
    elif(type=="Macro"):
        #moving add_frame and file_load_save_frame down
        add_frame.grid_configure(row=current_row+4)
        file_load_save_frame.grid_configure(row=current_row+4)

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

        #Set click key
        set_click_key_frame = Frame(mainframe)
        set_click_key_frame.grid(row=current_row+2,column=0, sticky=(N,E,S,W))
        set_click_key_frame.config(background="black")
        list_of_items[len(list_of_items)-1].append(set_click_key_frame)

        set_click_key_label = Label(set_click_key_frame,text="1. Click Key: ",fg="white", bg="black",font=("Arial",15))
        set_click_key_label.grid(row=0,column=0)

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
        set_time_hold_textbox.insert(0,"0")#I think having this set to 0 is fine, but I will leave this comment in case becomes a problem and need to set to 1.

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
        set_delay_seconds_label.grid(row=0,column=2,padx=(0,5))

        #doing this now because have all frames in scope so can put in the lambda
        mouse_or_keyboard_selector_string=StringVar()
        mouse_or_keyboard_selector = OptionMenu(set_click_key_frame, mouse_or_keyboard_selector_string, "Mouse","Move Mouse","Keyboard","Text","Wait", command= lambda new_selection: mouse_or_keyboard_selector_update(False, new_selection,set_click_key_frame,set_time_hold_repeat_frame,set_delay_frame))
        mouse_or_keyboard_selector.configure(bg="black", fg="white", activebackground="black",activeforeground="white")
        mouse_or_keyboard_selector["menu"].config(bg="black",fg="white")
        mouse_or_keyboard_selector_string.set("Mouse")
        mouse_or_keyboard_selector.grid(row=0, column=1, padx=(0,5))

        mouse_button_selector_string=StringVar() # need this one with the thing above so is always the 2nd child of the frame
        mouse_button_selector = OptionMenu(set_click_key_frame, mouse_button_selector_string, "Left Click","Right Click", "Middle Click")
        mouse_button_selector.configure(bg="black", fg="white", activebackground="black",activeforeground="white")
        mouse_button_selector["menu"].config(bg="black",fg="white")
        mouse_button_selector_string.set("Left Click")
        mouse_button_selector.grid(row=0, column=2, padx=5)

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
window.geometry("1100x500") # initial size of window

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

#add button
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

#file load/save frame
file_load_save_frame = Frame(mainframe)
file_load_save_frame.grid(row=1, column=1, sticky=(N,E,S,W))
file_load_save_frame.configure(background="black")

#file load button
file_load_button = Button(file_load_save_frame,text="Load File", command=load_file, fg="white", bg="black", activeforeground="white",activebackground="black",font=("Arial",15))
file_load_button.grid(row=0, column=0)

#file save button
file_save_button = Button(file_load_save_frame,text="Save File", command=save_file, fg="white", bg="black", activeforeground="white",activebackground="black",font=("Arial",15))
file_save_button.grid(row=0, column=1)

#global variables for various things
list_of_items=[]
list_of_checkbox_variables=[]
list_of_active_items=[]
most_recent_key_pressed=""
shift_symbols = '~!@#$%^&*()_+QWERTYUIOP{}|ASDFGHJKL:"ZXCVBNM<>?'
number_of_frames_in_macro_command=4
num_caps_lock_presses=0

#---whatever---
#adds spacing to each widget
for child in mainframe.winfo_children(): 
    child.grid_configure(padx=5, pady=5)

keyboard.on_press(clicked_key) # activates keyboard
window.mainloop() # activates the window