from tkinter import *
from ColorPeg import ColorPeg
from ScorePeg import ScorePeg
from TextObj import TextObj
from Settings import Settings
from KeyPegs import KeyPegs
from GuessRows import GuessRows
from GridCanvas import GridCanvas
import pygame, random

##############################################################################################################
# References :
#
# Good starting tutorial with tutorial code:
# https://towardsdatascience.com/making-simple-games-in-python-f35f3ae6f31a - Aqeel Anwar (Dots and Boxes)
# https://github.com/aqeelanwar/Dots-and-Boxes
# 
# https://pythonguides.com/python-tkinter-events/
#
# Not sure if I'll ever use this, but it seems useful (all bindings in tkinter, or most)
# https://www.tcl.tk/man/tcl8.6/TkCmd/keysyms.html
# 
##############################################################################################################

GAME_VERSION = "Beta_0.1"

class Mastermind_Class():
    def __init__(self):
        # This is used for sound effects. Probably could have programmed all of this using this library
        pygame.init()
        Settings.load()
        
        self.game_round = None                
        self.title_text = None
        self.music_on = False
        
        self.window = Tk()
        self.window.title("Mastermind - " + GAME_VERSION)
        self.window.bind("<Button-1>", self.click)
        self.window.bind("<Button-2>", self.click)
        self.window.bind("<Button-3>", self.click)
        self.window.bind("<MouseWheel>", self.click)
        self.window.bind("<Motion>", self.motion)
        self.window.bind("<Control-Key-c>", self.cheat)
        self.window.bind("<KeyRelease>", self.release_key)        
        self.window.protocol("WM_DELETE_WINDOW", self.on_closing)

        self.window.minsize(GridCanvas.WIN_X_MIN_SIZE, GridCanvas.WIN_Y_MIN_SIZE)
        self.window.maxsize(GridCanvas.WIN_X_MAX_SIZE, GridCanvas.WIN_Y_MAX_SIZE)
        
        self.frame = Frame(self.window)
        self.frame.pack(fill=BOTH, expand=YES)
        
        self.canvas = GridCanvas(self)
        self.canvas.pack(fill=BOTH, expand=YES)
        
        self.canvas.set_sizes()
        self.initialize_board()
        self.refresh_board()

    def initialize_board(self, initialize_key = True):
        self.canvas.set_sizes()
        
        if initialize_key:
            KeyPegs.init_pegs(self.canvas)

        GuessRows.init_rows(self.canvas, self)
        
        self.text_values = []
        self.text_values.append(TextObj(0, 0, "Random"))
        self.text_values.append(TextObj(0, 0, "Start"))
        self.text_values.append(TextObj(0, 0, "Music"))
        self.title_text = TextObj(0, 0, "Round Number : N/A")

    def refresh_board(self):
        # Recalculate basic grid locations and sizes
        self.canvas.set_sizes()

        text_y = self.canvas.key_y_loc
        for text in self.text_values:
            text.move_text(self.canvas.text_menu_x_loc, text_y)
            text_y = text_y + self.canvas.curr_y_step / 2.0
        
        self.title_text.move_text(self.canvas.curr_x_step * 2, self.canvas.key_y_loc - 50)

        self.canvas.delete("all")

        # Put a line here before guess pegs
        self.canvas.create_line(self.canvas.curr_x_step / 2.0, self.canvas.curr_y_step * 2, 
                                self.canvas.curr_x_step * 5, self.canvas.curr_y_step * 2, fill="#777777", width=2)

        KeyPegs.draw_pegs()        
        GuessRows.draw_rows()

        # Draw the text stuff now        
        for text in self.text_values:
            self.canvas.create_text(text.x_loc, text.y_loc, font=("Courier New", int(self.canvas.curr_x_step / 5.0)), fill=text.color, text=text.text)

        # Create title text
        if self.game_round == "win":
            self.canvas.create_text(self.title_text.x_loc, self.title_text.y_loc, font=("Courier New", int(self.canvas.curr_x_step / 5.0)), fill="Green", text=self.title_text.text)
            KeyPegs.set_hidden(False)
        elif self.game_round == "lose":
            self.canvas.create_text(self.title_text.x_loc, self.title_text.y_loc, font=("Courier New", int(self.canvas.curr_x_step / 5.0)), fill="Red", text=self.title_text.text)
            KeyPegs.set_hidden(False)
        else:
            self.canvas.create_text(self.title_text.x_loc, self.title_text.y_loc, font=("Courier New", int(self.canvas.curr_x_step / 5.0)), text=self.title_text.text)

    
    def click(self, event):
        # print("Event : " + str(event))        
        if(event.num == 1):
            # Left clicked, figure out if they are clicking on a peg
            KeyPegs.check_click(event.x, event.y)
            GuessRows.check_click(event.x, event.y)                              

            for text in self.text_values:
                if text.color == text.green:                    
                    self.option_click(text.text)

        elif(event.num == 3):
            KeyPegs.check_click(event.x, event.y, forward=False)
            GuessRows.check_click(event.x, event.y, forward=False)                            

        elif(event.delta == 120):
            KeyPegs.check_click(event.x, event.y)
            GuessRows.check_click(event.x, event.y)                

        elif(event.delta == -120):
            KeyPegs.check_click(event.x, event.y, forward=False)
            GuessRows.check_click(event.x, event.y, forward=False)                   

        self.refresh_board()

    def cheat(self, event):        
        KeyPegs.set_hidden(False)
        self.refresh_board()

    def release_key(self, event):
        KeyPegs.set_hidden(True)
        self.refresh_board() 

    def motion(self, event):
        """
        print("movement event : " + str(event))
        """
        # Check to see if any of the text is hovered over here
        # TODO: This whole file needs to be refactored at this point       
        for text in self.text_values:
            if text.is_over_text(event.x, event.y):
                text.color = text.green
            else:
                text.color = text.black

        GuessRows.check_motion(event.x, event.y)

        self.refresh_board()

    def set_game_round(self, curr_round):
        self.game_round = curr_round
        if curr_round == "win":
            self.title_text.text = "YOU WIN!!!"
            KeyPegs.set_hidden(False)
        elif curr_round == "lose":
            self.title_text.text = "YOU LOSE!!!"
            KeyPegs.set_hidden(False)
        else:
            if curr_round != None:
                self.title_text.text = "Round Number : " + str(curr_round)                
                self.refresh_board()
            else:
                self.title_text.text = "Round Number : N/A"
                KeyPegs.set_hidden(False)
        if(self.is_playable_round()):
            GuessRows.set_curr_round(self.game_round)
    
    def is_playable_round(self):
        return self.game_round != None and self.game_round != "win" and self.game_round != "lose"

    def option_click(self, menu_option):        
        if menu_option == "Random":
            if self.game_round == None or self.game_round == "win" or self.game_round == "lose" or self.game_round == 1:
                print("Randomizing pegs...")
                KeyPegs.set_random()

        elif menu_option == "Start":                  
            # If any of the pegs aren't defined, define them, then start (single player game)
            KeyPegs.set_random(blanks_only = True)                
            self.play_new_game()

        elif menu_option == "Music":
            if self.music_on:
                pygame.mixer.music.stop()
                self.music_on = False
            else:
                pygame.mixer.music.load("sounds/music_for_mastermind.mp3")
                pygame.mixer.music.play(-1, 0.0)
                self.music_on = True

    def on_closing(self):
        pygame.quit()
        Settings.save(self.canvas)
        self.window.destroy() 

    def play_new_game(self):
        self.initialize_board(initialize_key = False)

        KeyPegs.set_hidden(True)        
        self.set_game_round(1)
        self.refresh_board()

if __name__ == "__main__":
    mc = Mastermind_Class()
    mc.window.mainloop()