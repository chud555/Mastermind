from tkinter import *
from ColorPeg import ColorPeg
from ScorePeg import ScorePeg
from TextObj import TextObj
from Settings import Settings
from KeyPegs import KeyPegs
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
        self.guess_color_pegs = []
        self.submit_guess_text = []
        self.text_values = []
        self.round_text = list(range(10, 0, -1))
        self.title_text = None
        
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
        if initialize_key:
            KeyPegs.init_pegs(self.canvas)
        
        self.guess_color_pegs = []
        self.score_pegs = []
        # Build guess rows
        for y in self.canvas.guess_peg_y_loc_list:
            self.guess_color_pegs.append([])
            self.score_pegs.append(ScorePeg(0, y, 0))
            for x in self.canvas.peg_x_loc_list:
                self.guess_color_pegs[-1].append(ColorPeg(x, y))

        self.separator_line = self.canvas.curr_y_step * 2
        
        self.text_values = []
        self.text_values.append(TextObj(0, 0, "Random"))
        self.text_values.append(TextObj(0, 0, "Start"))
        self.title_text = TextObj(0, 0, "Round Number : N/A")

        self.submit_guess_text = []
        for y in self.canvas.guess_peg_y_loc_list:
            self.submit_guess_text.append(TextObj(0, 0, "X"))

    def refresh_board(self):
        self.canvas.set_sizes()
        KeyPegs.move_pegs()

        for y, guess_list, sub_text in zip(self.canvas.guess_peg_y_loc_list, self.guess_color_pegs, self.submit_guess_text):
            sub_text.move_text(self.canvas.text_menu_x_loc, y)
            for x, k_peg in zip(self.canvas.peg_x_loc_list, guess_list):
                k_peg.move_peg(x, y)

        for y, s_peg in zip(self.canvas.guess_peg_y_loc_list, self.score_pegs):
            s_peg.move_peg(self.canvas.score_pegs_x_loc, y)

        text_y = self.canvas.key_y_loc
        for text in self.text_values:
            text.move_text(self.canvas.text_menu_x_loc, text_y)
            text_y = text_y + self.canvas.curr_y_step / 2.0
        
        self.title_text.move_text(self.canvas.curr_x_step * 2, self.canvas.key_y_loc - 50)

        self.canvas.delete("all")

        # Put a line here before guess pegs
        self.canvas.create_line(self.canvas.curr_x_step / 2.0, self.separator_line, 
                                self.canvas.curr_x_step * 5, self.separator_line, fill="#777777", width=2)

        KeyPegs.draw_pegs(self.canvas)

        for guess_list, round_t, guess_text in zip(self.guess_color_pegs, self.round_text, self.submit_guess_text):
            make_guess_clickable = False
            if round_t == self.game_round:
                curr_color= "#20FD20"
                make_guess_clickable = True
            else:
                curr_color = "Black"
            if self.game_round != None and self.game_round != "win" and self.game_round != "lose":
                if round_t <= self.game_round:
                    self.canvas.create_text(self.canvas.curr_x_step / 2, guess_list[0].y_loc, font=("Courier New", int(self.canvas.curr_x_step / 5.0)), fill=curr_color, text=str(round_t))
                    self.canvas.create_text(guess_text.x_loc, guess_text.y_loc, font=("Courier New", int(self.canvas.curr_x_step / 2.0)), fill=guess_text.color, text=str(guess_text.text))
            for k_peg in guess_list:
                k_peg.set_peg_size(self.canvas.smallest_step)
                k_peg.is_clickable = make_guess_clickable               
                if k_peg.state == ColorPeg.States.EMPTY:
                    curr_size = k_peg.empty_size                    
                else:                
                    curr_size = k_peg.size
                self.canvas.create_oval(k_peg.x_loc - curr_size,
                                        k_peg.y_loc - curr_size, 
                                        k_peg.x_loc + curr_size,
                                        k_peg.y_loc + curr_size, 
                                        fill=k_peg.state.value["color"],
                                        outline=k_peg.peg_outline_color)

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

        for k_peg in self.score_pegs:
            k_peg.set_peg_size(self.canvas.smallest_step)
            if k_peg.state_1 == ScorePeg.States.EMPTY:
                self.canvas.create_oval(k_peg.p1_x_loc - k_peg.empty_size, 
                                        k_peg.p1_y_loc - k_peg.empty_size, 
                                        k_peg.p1_x_loc + k_peg.empty_size,
                                        k_peg.p1_y_loc + k_peg.empty_size, 
                                        fill=k_peg.state_1.value["color"],
                                        outline=k_peg.peg_outline_color)
            else:
                self.canvas.create_oval(k_peg.p1_x_loc - k_peg.size, 
                                        k_peg.p1_y_loc - k_peg.size, 
                                        k_peg.p1_x_loc + k_peg.size,
                                        k_peg.p1_y_loc + k_peg.size, 
                                        fill=k_peg.state_1.value["color"],
                                        outline=k_peg.peg_outline_color)

            if k_peg.state_2 == ScorePeg.States.EMPTY:
                self.canvas.create_oval(k_peg.p2_x_loc - k_peg.empty_size, 
                                        k_peg.p2_y_loc - k_peg.empty_size, 
                                        k_peg.p2_x_loc + k_peg.empty_size,
                                        k_peg.p2_y_loc + k_peg.empty_size, 
                                        fill=k_peg.state_2.value["color"],
                                        outline=k_peg.peg_outline_color)
            else:
                self.canvas.create_oval(k_peg.p2_x_loc - k_peg.size, 
                                        k_peg.p2_y_loc - k_peg.size, 
                                        k_peg.p2_x_loc + k_peg.size,
                                        k_peg.p2_y_loc + k_peg.size, 
                                        fill=k_peg.state_2.value["color"],
                                        outline=k_peg.peg_outline_color)

            if k_peg.state_3 == ScorePeg.States.EMPTY:
                self.canvas.create_oval(k_peg.p3_x_loc - k_peg.empty_size, 
                                        k_peg.p3_y_loc - k_peg.empty_size, 
                                        k_peg.p3_x_loc + k_peg.empty_size,
                                        k_peg.p3_y_loc + k_peg.empty_size, 
                                        fill=k_peg.state_3.value["color"],
                                        outline=k_peg.peg_outline_color)
            else:
                self.canvas.create_oval(k_peg.p3_x_loc - k_peg.size, 
                                        k_peg.p3_y_loc - k_peg.size, 
                                        k_peg.p3_x_loc + k_peg.size,
                                        k_peg.p3_y_loc + k_peg.size, 
                                        fill=k_peg.state_3.value["color"],
                                        outline=k_peg.peg_outline_color)

            if k_peg.state_4 == ScorePeg.States.EMPTY:
                self.canvas.create_oval(k_peg.p4_x_loc - k_peg.empty_size, 
                                        k_peg.p4_y_loc - k_peg.empty_size, 
                                        k_peg.p4_x_loc + k_peg.empty_size,
                                        k_peg.p4_y_loc + k_peg.empty_size, 
                                        fill=k_peg.state_4.value["color"],
                                        outline=k_peg.peg_outline_color)
            else:
                self.canvas.create_oval(k_peg.p4_x_loc - k_peg.size, 
                                        k_peg.p4_y_loc - k_peg.size, 
                                        k_peg.p4_x_loc + k_peg.size,
                                        k_peg.p4_y_loc + k_peg.size, 
                                        fill=k_peg.state_4.value["color"],
                                        outline=k_peg.peg_outline_color)
    
    def click(self, event):
        # print("Event : " + str(event))
        guess_color_pegs_flat = [item for items in self.guess_color_pegs for item in items]
        if(event.num == 1):
            # Left clicked, figure out if they are clicking on a peg
            KeyPegs.check_click(event.x, event.y, forward=True)
            for k_peg in guess_color_pegs_flat:
                if k_peg.clicked_on_peg(event.x, event.y):                        
                    k_peg.cycle_states()                    

            for text in self.text_values:
                if text.color == text.green:
                    self.option_click(text.text)

            for text in self.submit_guess_text:
                if text.color == text.green and self.game_round != "win" and self.game_round != "lose":
                    # At this point a real guess is put in
                    if self.score_round():
                        self.set_game_round("win")
                    elif self.game_round == 10:
                        self.set_game_round("lose")
                    else:
                        self.set_game_round(self.game_round + 1)

        elif(event.num == 3):
            KeyPegs.check_click(event.x, event.y, forward=False)
            # Left clicked, figure out if they are clicking on a circle
            for k_peg in guess_color_pegs_flat:
                if k_peg.clicked_on_peg(event.x, event.y):
                    k_peg.cycle_states(False)                    

        elif(event.delta == 120):
            KeyPegs.check_click(event.x, event.y, forward=True)
            for k_peg in guess_color_pegs_flat:
                if k_peg.clicked_on_peg(event.x, event.y):                    
                    k_peg.cycle_states()                    

        elif(event.delta == -120):
            KeyPegs.check_click(event.x, event.y, forward=False)
            for k_peg in guess_color_pegs_flat:
                if k_peg.clicked_on_peg(event.x, event.y):
                    k_peg.cycle_states(False)                    

        self.refresh_board()

    def cheat(self, event):        
        KeyPegs.set_hidden(False)
        self.refresh_board()

    def release_key(self, event):
        KeyPegs.set_hidden(True)
        self.refresh_board() 

    def score_round(self):
        correct_guess = False

        score_list = [ScorePeg.States.EMPTY, \
                      ScorePeg.States.EMPTY, \
                      ScorePeg.States.EMPTY, \
                      ScorePeg.States.EMPTY]

        if (self.game_round != "win" and self.game_round != "lose"):
            curr_ind = 10 - self.game_round
            white_check_list = []
            # Check for black peg matches first
            for i in list(range(1, 5, 1)):
                """
                print("i : " + str(i))
                print("self.guess_color_pegs[curr_ind] : " + str(self.guess_color_pegs[curr_ind]))
                print("self.guess_color_pegs[curr_ind][i - 1] : " + str(self.guess_color_pegs[curr_ind][i - 1]))
                """
                if self.guess_color_pegs[curr_ind][i - 1].state == KeyPegs.peg_list[i - 1].state:
                    score_list[i - 1] = ScorePeg.States.BLACK
                else:
                    white_check_list.append(KeyPegs.peg_list[i - 1].state)
            for i in list(range(1, 5, 1)):
                if score_list[i - 1] != ScorePeg.States.BLACK and self.guess_color_pegs[curr_ind][i - 1].state in white_check_list:
                    white_check_list.remove(self.guess_color_pegs[curr_ind][i - 1].state)
                    score_list[i - 1] = ScorePeg.States.WHITE

            # print("score_list : " + str(score_list))
            for x in score_list:
                if x == ScorePeg.States.BLACK:
                    if self.score_pegs[curr_ind].state_1 == ScorePeg.States.EMPTY:
                        self.score_pegs[curr_ind].state_1 = ScorePeg.States.BLACK
                    elif self.score_pegs[curr_ind].state_2 == ScorePeg.States.EMPTY:
                        self.score_pegs[curr_ind].state_2 = ScorePeg.States.BLACK
                    elif self.score_pegs[curr_ind].state_3 == ScorePeg.States.EMPTY:
                        self.score_pegs[curr_ind].state_3 = ScorePeg.States.BLACK
                    elif self.score_pegs[curr_ind].state_4 == ScorePeg.States.EMPTY:
                        self.score_pegs[curr_ind].state_4 = ScorePeg.States.BLACK
                elif x == ScorePeg.States.WHITE:
                    if self.score_pegs[curr_ind].state_1 == ScorePeg.States.EMPTY:
                        self.score_pegs[curr_ind].state_1 = ScorePeg.States.WHITE
                    elif self.score_pegs[curr_ind].state_2 == ScorePeg.States.EMPTY:
                        self.score_pegs[curr_ind].state_2 = ScorePeg.States.WHITE
                    elif self.score_pegs[curr_ind].state_3 == ScorePeg.States.EMPTY:
                        self.score_pegs[curr_ind].state_3 = ScorePeg.States.WHITE
                    elif self.score_pegs[curr_ind].state_4 == ScorePeg.States.EMPTY:
                        self.score_pegs[curr_ind].state_4 = ScorePeg.States.WHITE
            
            correct_guess = self.score_pegs[curr_ind].state_1 == ScorePeg.States.BLACK and \
                            self.score_pegs[curr_ind].state_2 == ScorePeg.States.BLACK and \
                            self.score_pegs[curr_ind].state_3 == ScorePeg.States.BLACK and \
                            self.score_pegs[curr_ind].state_4 == ScorePeg.States.BLACK

        return correct_guess
    
    def motion(self, event):
        """
        print("movement event : " + str(event))
        """
        # Check to see if any of the text is hovered over here
        # TODO: This whole file needs to be refactored at this poing        
        for text in self.text_values:
            if text.is_over_text(event.x, event.y):
                text.color = text.green
            else:
                text.color = text.black
        
        if self.game_round != None and self.game_round != "win" and self.game_round != "lose":
            for text in self.submit_guess_text:
                curr_ind = 10 - self.game_round
                if text.is_over_text(event.x, event.y):
                    # Can't click if there's empty spaces
                    if self.guess_color_pegs[curr_ind][0].state == ColorPeg.States.EMPTY or \
                       self.guess_color_pegs[curr_ind][1].state == ColorPeg.States.EMPTY or \
                       self.guess_color_pegs[curr_ind][2].state == ColorPeg.States.EMPTY or \
                       self.guess_color_pegs[curr_ind][3].state == ColorPeg.States.EMPTY:
                        text.color = text.red
                    else:
                        text.color = text.green
                else:
                    text.color = text.black
        self.refresh_board()

    def set_game_round(self, curr_round):
        self.game_round = curr_round
        if curr_round == "win":
            self.title_text.text = "YOU WIN!!!"
        elif curr_round == "lose":
            self.title_text.text = "YOU LOSE!!!"
        else:
            self.title_text.text = "Round Number : " + str(curr_round)

    def option_click(self, menu_option):        
        if menu_option == "Random":
            KeyPegs.set_random()

        elif menu_option == "Start":                  
            # If any of the pegs aren't defined, define them, then start (single player game)
            KeyPegs.set_random(blanks_only = True)                
            self.play_new_game()           

    def on_closing(self):
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