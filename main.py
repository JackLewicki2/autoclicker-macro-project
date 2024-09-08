from tkinter import *
from enum import Enum

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
window.rowconfigure(0,weight=1) # row 0 will strech to take up all available space
mainframe.config(background="black")

#---modes---
#todo -> make button always be in same spot regardless of current mode text
current_mode = "Edit"
def change_mode():
    global current_mode
    if(current_mode=="Edit"):
        change_mode_button.config(text="Change mode to " + current_mode)
        current_mode="Running"
        # todo -> disable all macro settings so can't change if running
    else:
        change_mode_button.config(text="Change mode to " + current_mode)
        current_mode="Edit"
    current_mode_label.config(text="Current Mode: " + current_mode)
    

#Text
current_mode_label = Label(mainframe, text="Current Mode: " + current_mode, fg="white", bg="black",font=("Arial",15))
current_mode_label.grid(row=0,column=0)
#Button to Change
change_mode_button = Button(mainframe, text="Change mode to " + "Running", command=change_mode, fg="white", bg="black", activeforeground="white",activebackground="black",font=("Arial",15))
change_mode_button.grid(row=0, column=1)

#---add button---
def add_new():     #todo -> make this work; create frame for label and checkbox to go in together
    #getting needed variables
    global list_of_items
    current_row = add_frame.grid_info()["row"]
    # current_col = add_frame.grid_info()["column"] # not needed???
    type = type_selector_string.get()
    #updating list and total_items
    list_of_items.append([])

    if(type=="Autoclicker"):
        add_frame.grid_configure(row=current_row+2)
        #active label and checkbox
        active_label = Label(mainframe,text="Active: ",fg="white", bg="black",font=("Arial",15))
        active_label.grid(row=current_row,column=0)
        list_of_items[len(list_of_items)-1].append(active_label)

    elif(type=="Macro"):
        pass


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

list_of_items=[]



#---whatever---
#adds spacing to each widget
for child in mainframe.winfo_children(): 
    child.grid_configure(padx=5, pady=5)

    #todo -> maybe put other things here like bg, font, etc.

window.mainloop() # activates the window