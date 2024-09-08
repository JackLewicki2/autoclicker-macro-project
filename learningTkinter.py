from tkinter import * # lets use gui
#video has checkboxes, choose one option out of multiple(radio buttons), moving sliders (scales), choose multiple options out of multiple (listbox),   if need them
#!!Use grid instead of pack once know what want layout to be!!

count=0
def click():
    global count
    print("you clciked button",count:=count+1,"times")

characterToActivate=""
def submit():
    global characterToActivate
    entry.delete(1,END) # deletes characters 1-END
    input = entry.get() # gets current string in entry
    entry.config(state=DISABLED) # turns off entrybox after submit
    characterToActivate = input[:1]
    print(characterToActivate)


window = Tk() # instantiates an instance of a window
window.geometry("700x400") # size of window
window.title("autoclicker") # title of window

icon = PhotoImage(file='shedinja.png') # turning image into format tkinter can use. HAS TO BE PNG
window.iconphoto(True, icon)

window.config(background="black") # !!config lets you change different aspects of the window!!

# button just to practice
button = Button(window,
                text="click me!", # text on button
                font=("comic sans",30), # sets font and size. Pass in tuple
                fg="white", # foreground color (font color)
                bg = "black", # background color
                activeforeground="white", # foreground color (font color) when button clicked
                activebackground="black", # background color when button clicked
                #State = Active, # can be active or disabled
                # image= photoImageName, # adds an image to the button
                # compound = "top/bottom/left/right", # lets have image and text. Location is where image goes relative to the text.
                command=click) #calls function when clicked
button.pack() # activates the button


#more practice setting up sort of actual stuff
frame = Frame(window, bg="black") # frames help keep widgets together # other options are bd=5 (border width) relief="kajwdawljd" (how border looks)
frame.pack()
#frame.place(x,y) #puts the frame at certain coordinates

entry = Entry(frame,
              font=("comic sans",20),
              fg="white",
              bg = "black")
#entry.insert(0,'Default Text') # Puts Default text at position in the entrybox
entry.pack(side=LEFT)

submit_button = Button(frame,
                       text="Submit",
                       font=("comic sans",30),
                       command=submit)
submit_button.pack(side=RIGHT)

#key events
def pressedKey(event):
    print("you pressed ",str(event),"!") # event.keysym gives symbol of key pressed
window.bind("<Key>",pressedKey) # put key event in <>. <Key> is basically all keys.

#mouse events
def pressedMouse(event):
    print("you pressed mouse ",str(event.x),str(event.y)) # event.keysym gives symbol of key pressed
window.bind("<Button-1>",pressedMouse) # <Button-1> is left click, <Button-1> is clicking scroll wheel, <Button-3> is right click, 
                                        #<ButtonRelease> is when stop clicking, <Enter> is when mouse first enters area of window, <Leave> is opposite of enter, 
                                        #<Motion> is while cursor is moving -> lets you get latest position of mouse. There are more mouse ones you can google.


window.mainloop() # activates the window