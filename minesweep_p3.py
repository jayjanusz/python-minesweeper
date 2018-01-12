# -*- coding: utf-8 -*-
"""
Created on Thu Dec 14 19:09:54 2017

@author: Emma
"""

import tkinter
import random
from PIL import Image, ImageTk

gameOver = False #set to true when the game ends
score = 0
squaresToClear = 0
Flagged = False #set up flags (wont click square)

window = tkinter.Tk()
frame = tkinter.Frame(window)

#----------------------- mode select menu ------------------------------------
easy = tkinter.Button(frame, text = "easy", relief = 'raised') 
easy.config(command=lambda button=easy: mode(frame, button))
medium = tkinter.Button(frame, text = "medium", relief = 'raised') 
medium.config(command=lambda button=medium: mode(frame, button))
hard = tkinter.Button(frame, text = "hard", relief = 'raised') 
hard.config(command=lambda button=hard: mode(frame, button))

easy.pack()
medium.pack()
hard.pack()
frame.pack()
#-----------------------------------------------------------------------------
    
def mode(frame, button): #for setting mode (easy, medium, hard)
    var = button.cget("text") #gets which mode was selected by the player 
                                #(which button they pressed)
    frame.destroy() #destroys the mode select menu
    if var == "easy":
        no_rows = 9
        no_cols = 9
    elif var == "medium":
        no_rows= 16
        no_cols = 16
    elif var == "hard":
        no_rows= 16
        no_cols = 32
    frame = tkinter.Frame(window) #new frame created for the game
    create_minefield(minefield, no_rows, no_cols)
    
minefield = []

def create_minefield(minefield, no_rows, no_cols):
    global squaresToClear
    for row in range(0,int(no_rows)):
        rowList = []
        for column in range(0,int(no_cols)):
            if random.randint(1,100)<20:
                rowList.append(1)
            else:
                rowList.append(0)
                squaresToClear = squaresToClear +1
        minefield.append(rowList)
    #printfield(minefield) uncomment if you want to see the minefield
    layout_window(window)
    
def printfield(minefield):
    for rowList in minefield:
        print(rowList)
    
def layout_window(window):
    for rowNumber, rowList in enumerate(minefield):
        for columnNumber, columnEntry in enumerate(rowList):
            if random.randint(1,100)<25:
                square = tkinter.Label(window, text = "    ", bg="darkgreen", relief ='raised')
            elif random.randint(1,100) >75:
                square = tkinter.Label(window, text = "    ", bg="lightgreen", relief = 'raised')
            else:
                square = tkinter.Label(window, text = "    ", bg="green", relief = 'raised')
            square.grid(row=rowNumber, column =columnNumber)
            square.bind("<Button-1>", on_left_click)
            square.bind("<Button-3>", on_right_click)
            square.flagged = Flagged
            square.tile_flag = tkinter.PhotoImage(file = "tile_flag.gif")
          
def on_left_click(event):
    global score
    global gameOver
    global squaresToClear
    
    square = event.widget #creates a variable to represent the thing that's having an event
    row = int(square.grid_info()["row"]) #pulls out info about the square clicked (here row and column)
    column = int(square.grid_info()["column"]) #int makes sure the computer treats it as an integer
    currentText = square.cget("text") #looks up the existing text

    if gameOver == False:
        
            if minefield[row][column]==1:
                gameOver = True
                square.config(bg= "red", relief = 'sunken')
                print("Oh no! A mine has been detonated! Your body has been strewn across the ground in a bloody mess")
                print("Your score is:", score)
                
            elif currentText == "    ":
                square.config(bg="yellow", relief = 'sunken') #makes clear it has been pressed
                square.unbind("<Button-1>") #you will not be able to click on the square once
                square.unbind("<Button-3>") #it has been shown to have no mines
                totalMines = 0
                
                #below: checks the surrounding area of the square to count for
                #mines (if the square exists i.e. is less than the size of the 
                #minefield)
                for surrounding_col in range (column-1,column+2):
                    for surrounding_row in range (row-1,row+2):
                        if(0 <= surrounding_row <len(minefield) \
                           and 0<= surrounding_col <len(minefield[0])):
                            if minefield[surrounding_row][surrounding_col] == 1:
                                 totalMines = totalMines + 1
                             
                square.config(text = " " + str(totalMines) + " ") #shows the number of mines
                squaresToClear = squaresToClear-1 
                score = score+1
            
                if squaresToClear ==0:
                    gameOver = True
                    print("Congratulations! You survived death! ... For now")
                    print("Your score is:", score)
                     
def on_right_click(event):
    square = event.widget #creates a variable to represent the thing that's having an event

    if square.flagged == False: #if unflagged, make it flagged (no longer can click)
        square.config(image = square.tile_flag) 
        square.unbind("<Button-1>")
        square.flagged = True
   
    elif square.flagged == True: #if flagged, make unflagged (can click)
        square.bind("<Button-1>", on_left_click)
        square.config(image = '')
        square.flagged = False
        
window.mainloop()