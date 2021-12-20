from tkinter import *
from enum import Enum
import numpy as np

# TODO: Make everything scalable according to the windows size
x_size_of_board = 300
y_size_of_board = 800

key_y_loc = 50

guess_y_first_loc = 100

guess_y_loc_list = list(range(150,650,50))

x_loc_list = [50, 100, 150, 200]

empty_peg_size = 5.0
score_peg_size = 6.5
color_peg_size = 10.0

score_peg_size = 2
peg_outline_color = "#0F0F0F"

class GameStates(Enum):
    SETTING_CODE = 0,
    COMPUTER_SETTING_CODE = 1,
    SCORING = 2,
    STANDARD_PLAY = 3

class PegStates(Enum):
    EMPTY = {"color":"#808080", "clickable":True, "size":empty_peg_size},
    HIDDEN = {"color":"#202020", "clickable":False, "size":color_peg_size},
    WHITE = {"color":"#FDFDFD", "clickable":True, "size":color_peg_size},
    BLACK = {"color":"#000000", "clickable":True, "size":color_peg_size},
    RED = {"color":"#FF2020", "clickable":True, "size":color_peg_size},
    GREEN = {"color":"#20FF20", "clickable":True, "size":color_peg_size},
    BLUE = {"color":"#2020FF", "clickable":True, "size":color_peg_size},
    YELLOW = {"color":"#20FFFF", "clickable":True, "size":color_peg_size}

# This dictionary defines state transition rules. The keys are the 
state_list = [PegStates.WHITE, PegStates.BLACK, PegStates.RED, 
              PegStates.GREEN, PegStates.BLUE,  PegStates.YELLOW]

class ColorPeg():
    def __init__(self, x_loc, y_loc):
        self.state = PegStates.EMPTY
        self.x_loc = x_loc
        self.y_loc = y_loc

    def cycle_states(self):
        curr_ind = 0
        print("start - self.state : " + self.state.name)
        if self.state in state_list:
            x = 0
            for state in state_list:
                if self.state == state:
                    curr_ind = x
                x += 1
            curr_ind += 1
        print("curr_ind : " + str(curr_ind))
        if curr_ind < len(state_list):
            self.state = state_list[curr_ind]
        else:
            self.state = state_list[0]
        print("end - self.state : " + self.state.name + " : " + str(curr_ind))

    def __str__(self):
        out_str = ""
        out_str += "state : " + self.state.name + "\n"
        out_str += "x_loc : " + str(self.x_loc) + "\n"
        out_str += "y_loc : " + str(self.y_loc) + "\n"
        return out_str

class Mastermind_Class():
    def __init__(self):
        self.window = Tk()
        self.window.title('Mastermind - Beta_0.1')
        self.canvas = Canvas(self.window, width=x_size_of_board, height=y_size_of_board)
        self.canvas.pack()
        self.window.bind('<Button-1>', self.click)
        self.game_state = GameStates.SETTING_CODE
        self.key_color_pegs = []
        self.guess_color_pegs = []

        self.initialize_board()
        self.refresh_board()
        self.play_again()
        
    def initialize_board(self):
        for x in x_loc_list:
            self.key_color_pegs.append(ColorPeg(x , key_y_loc))
        
        for y in guess_y_loc_list:
            for x in x_loc_list:
                self.guess_color_pegs.append(ColorPeg(x, y))        

    def refresh_board(self):
         # Put a line here befoe guess pegs
        self.canvas.create_line(10, 100, 
                                240, 100, fill="#777777", width=2)

        for k_peg in self.guess_color_pegs + self.key_color_pegs:
            if k_peg.state == PegStates.EMPTY:
                self.canvas.create_oval(k_peg.x_loc - empty_peg_size, 
                                        k_peg.y_loc - empty_peg_size, 
                                        k_peg.x_loc + empty_peg_size,
                                        k_peg.y_loc + empty_peg_size, 
                                        fill=k_peg.state.value["color"],
                                        outline=peg_outline_color)
            else:
                print(k_peg)
                self.canvas.create_oval(k_peg.x_loc - color_peg_size, 
                                        k_peg.y_loc - color_peg_size, 
                                        k_peg.x_loc + color_peg_size,
                                        k_peg.y_loc + color_peg_size, 
                                        fill=k_peg.state.value["color"],
                                        outline=peg_outline_color)
    def click(self, event):
        print("Event : " + str(event))
        if(event.num == 1):
            # Left clicked, figure out if they are clicking on a circle
            for k_peg in self.key_color_pegs + self.guess_color_pegs:
                # print("k_peg : " + str(k_peg))
                if event.x < k_peg.x_loc + color_peg_size and \
                   event.x > k_peg.x_loc - color_peg_size and \
                   event.y < k_peg.y_loc + color_peg_size and \
                   event.y > k_peg.y_loc - color_peg_size:
                    print("FOUND MATCH")
                    k_peg.cycle_states()

        self.refresh_board()


    def play_again(self):
        self.initialize_board()
        self.refresh_board()

    def mainloop(self):
        self.window.mainloop()

if __name__ == "__main__":
    mc = Mastermind_Class()
    mc.mainloop()