--What to Download--<br/>
Downloading the autoclicker.exe file will allow you to run the app. Alternatively, you can download autoclicker.py and run the app like you would any other Python program.<br/>
<br/>

--Setting Up Autoclickers/Macros--<br/>
The 'Add New' button allows you to add a new autoclicker/macro. You can select which to add by using the 'Type' selector.<br/>
The 'Active' checkbox indicates whether an autoclicker/macro can turn on when the mode is changed to running.<br/>
The 'Name' textbox lets you name your autoclicker/macro.<br/>
The 'Delete' button removes the corresponding autoclicker/macro.<br/>
The 'Toggle Key' textbox allows you to set the key that turns the autoclicker/macro on/off. Typing a key into it will display the key you chose in the textbox.<br/>
The 'Click Key' selector lets you choose whether to have the mouse or the keyboard click a key.<br/>
&ensp;  If you choose 'Mouse,' another selector appears to let you choose which mouse button will be clicked.<br/>
&ensp;  If you choose 'Keyboard,' a textbox similar to the 'Toggle Key' textbox appears, allowing you to set the keyboard key to be clicked.<br/>
--Autoclicker Specific--<br/>
The 'Delay' textbox lets you set the delay in milliseconds between clicks.<br/>
--Macro Specific--<br/>
The 'Loop' checkbox indicates whether the macro will loop back to its first command after completing all of its commands.<br/>
The 'Add Another Command' button allows you to add another command for the macro to execute.<br/>
You can delete a macro command by clicking the 'Delete Command' button on the very right of the command you wish to delete.<br/>
The 'Hold For' textbox sets the time the selected key should be held down in milliseconds.<br/>
The 'Run' textbox sets the number of times that a command will run before moving onto the next command.<br/>
The 'Delay' textbox sets the time to wait after each iteration of a command.<br/>

The 'Click Key' selector has an addition field 'Move Mouse' in which you can set the mouse to move in a certain way.<br/>
&ensp; There is a selector right after the 'Click Key' selector that lets you pick between moving the mouse to an 'Absolute Position' or 'Relative Position' on the screen.<br/>
&ensp; &ensp; 'Absolute Position' means the mouse will go directly to the x and y coordinates selected.<br/>
&ensp; &ensp; 'Relative Position' means the mouse will add the x and y coordinates selected to its current position.<br/>
&ensp; The 'x' and 'y' textboxes allow you to set the x and y coordinates as described above. They can contain negative values.<br/>
&ensp; The 'Duration' textbox allows you to set the time it will take the mouse to complete its move.<br/>
&ensp; The 'Record Mouse x/y on Click' button lets you automatically set the x/y textboxes. After clicking the button, click anywhere on the screen, and the x/y textboxes will be set to the coordinates of the location you clicked. A warning: if you click on a component of the app, the component will be interacted with. For example, if you click a 'Delete' button, the x/y textboxes will be set to the coordinates of the click, but then the delete button will trigger. I recommend moving the application window out of the way of where you want to click to avoid accidentally interacting with something.<br/>

The 'Click Key' selector has an addition field 'Text' where you can set a string of characters to be typed out.<br/>
&ensp; There is a textbox right after the 'Click Key' selector where you may enter the characters you wish to be typed.<br/>
&ensp; The 'Type a character every' textbox lets you set the delay in milliseconds after each character is typed.<br/>

The 'Click Key' selector has an addition field 'Wait' in which no key will be clicked. The total time waited for equals (Run) * (HoldFor + Delay). <br/>
--Running the Autoclickers/Macros--
Once you have set up your autoclickers/macros, you can click the 'Change mode to Running' button at the top to disable editing and start executing the autoclickers/macros.<br/>
When you press the assigned Toggle Key, the corresponding autoclicker/macro will turn on/off.<br/>
You can click the 'Change mode to Edit' button at the top to disable all active autoclickers/macros and begin editing.<br/>
An autoclicker/macro will not execute if any of its textboxes are empty (except for the name, which is not necessary) or if they have invalid values.<br/>
***In an emergency, you can change the mode to Edit by clicking the "CapsLock" key three times. It works best if you spam click "CapsLock" because the inputs can be dropped sometimes depending on what autoclickers/macros you are executing.<br/>
--Saving/Loading--<br/>
Clicking the 'Save File' button at the bottom allows you to save your current autoclickers/macros to a file.<br/>
Clicking the 'Load File' button at the bottom allows you to load previously saved autoclickers/macros. The autoclickers/macros in the file will be added to the bottom of any you currently have in the application. <br/>
--Miscellaneous--<br/>
There is a scrollbar located on the right side of the window. You can use it to scroll through the application if the size of the autoclickers/macros exceeds the window size.<br/>
There is no way to stop a mouse from moving once it has begun, even when the mode is changed to Edit.<br/>
'Text' commands in macros will not always send all of the characters they are supposed to if the 'Type a character every' textbox has too small a value. <br/>
If you hold the 'shift' key down and a macro/autoclicker clicks a key that involves using the 'shift' key (such as A or !), after the key click finishes, the computer will interpret the 'shift' key as not being pressed down even if you are still holding it down. You can fix this just by releasing and then repressing the 'shift' key.<br/>
Please do not include the string '_$$$_' in a 'Name' textbox because then the autoclicker/macro will not save properly.<br/>
Please do not include the string '_$$$_' or '_$$$$$_' in a 'Text' command's textbox because then the macro will not save properly.<br/>
Running multiple autoclickers/macros at the same time is possible, but overlapping output types (like if multiple click keys) can cause the output to be in a seemingly random order and can lead to unintentional side effects (like accidentally getting uppercase letters if a macro presses shift and another presses lowercase letters). <br/>
If delay is set to 0ms, it will be increased to 1ms. This happens because when delay is 0ms, the application severely lags and can be difficult to stop. <br/>
<br/>
--Possible Future Improvements--<br/>
I am content with where the project is at, so there probably won't be anymore updates. However, if I get an idea for an improvement or find a bug, I will do my best to add the idea/fix the bug.<br/>