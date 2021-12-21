from tkinter import *
from enum import Enum

# References :
#
# Good starting tutorial with clean code:
# https://towardsdatascience.com/making-simple-games-in-python-f35f3ae6f31a - Aqeel Anwar (Dots and Boxes)
# https://github.com/aqeelanwar/Dots-and-Boxes
# 
# https://pythonguides.com/python-tkinter-events/

class GameStates(Enum):
    SETTING_CODE = 0
    COMPUTER_SETTING_CODE = 1
    SCORING = 2
    STANDARD_PLAY = 3

class PegStates(Enum):
    EMPTY = {"color":"#808080", "clickable":True, "size":None}
    HIDDEN = {"color":"#202020", "clickable":False, "size":None}
    WHITE = {"color":"#FDFDFD", "clickable":True, "size":None}
    BLACK = {"color":"#000000", "clickable":True, "size":None}
    RED = {"color":"#FF2020", "clickable":True, "size":None}
    GREEN = {"color":"#20FF20", "clickable":True, "size":None}
    BLUE = {"color":"#2020FF", "clickable":True, "size":None}
    YELLOW = {"color":"#FFFF20", "clickable":True, "size":None}

# This list defines state transition rules.
state_list = [PegStates.WHITE, 
              PegStates.BLACK, 
              PegStates.RED, 
              PegStates.GREEN, 
              PegStates.BLUE,  
              PegStates.YELLOW]

class ColorPeg():
    def __init__(self, x_loc, y_loc):
        self.peg_outline_color = "#0F0F0F"
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

    get 

    def __str__(self):
        out_str = ""
        out_str += "state : " + self.state.name + "\n"
        out_str += "x_loc : " + str(self.x_loc) + "\n"
        out_str += "y_loc : " + str(self.y_loc) + "\n"
        return out_str

class Mastermind_Class():
    def __init__(self):
        self.game_state = GameStates.SETTING_CODE
        
        self.x_size_of_board = 300
        self.y_size_of_board = 800

        self.load_settings()
        self.key_color_pegs = []
        self.guess_color_pegs = []

        self.window = Tk()
        self.window.title('Mastermind - Beta_0.1')
        self.canvas = Canvas(self.window, width=self.x_size_of_board, height=self.y_size_of_board)
        self.canvas.pack()

        self.window.bind('<Button-1>', self.click)
        self.initialize_board()
        self.refresh_board()
        self.play_again()
        
    def initialize_board(self):
        # Set all sizes used here, all based off the window sizes
        # 6 x columns, 12 y columns for now, base everything on that
        self.x_size = self.x_size_of_board / 6
        self.y_size = self.y_size_of_board / 13

        self.peg_size_ref = self.x_size
        if self.y_size < self.peg_size_ref:
            self.peg_size_ref = self.y_size

        self.key_y_loc = self.y_size
        self.separator_line = self.y_size * 2
        self.guess_y_first_loc = self.y_size * 3
        
        # Might want to move these into peg classes... probably
        self.score_peg_size = self.peg_size_ref / 30
        self.score_peg_size = self.score_peg_size * 2
        self.empty_color_peg_size = self.score_peg_size * 1.5
        self.color_peg_size = self.score_peg_size * 3    

        self.x_loc_list = [self.x_size, self.x_size * 2, self.x_size * 3, self.x_size * 4]

        self.guess_y_loc_list = list(range(int(self.guess_y_first_loc), int(self.y_size * 12), int(self.y_size)))

        # Build key location, the top row
        for x in self.x_loc_list:
            self.key_color_pegs.append(ColorPeg(x , self.key_y_loc))
        
        # Build guess rows
        for y in self.guess_y_loc_list:
            for x in self.x_loc_list:
                self.guess_color_pegs.append(ColorPeg(x, y))      

    def refresh_board(self):
         # Put a line here befoe guess pegs
        self.canvas.create_line(10, 100, 
                                240, 100, fill="#777777", width=2)

        for k_peg in self.guess_color_pegs + self.key_color_pegs:
            if k_peg.state == PegStates.EMPTY:
                self.canvas.create_oval(k_peg.x_loc - self.empty_color_peg_size, 
                                        k_peg.y_loc - self.empty_color_peg_size, 
                                        k_peg.x_loc + self.empty_color_peg_size,
                                        k_peg.y_loc + self.empty_color_peg_size, 
                                        fill=k_peg.state.value["color"],
                                        outline=k_peg.peg_outline_color)
            else:
                print(k_peg)
                self.canvas.create_oval(k_peg.x_loc - self.color_peg_size, 
                                        k_peg.y_loc - self.color_peg_size, 
                                        k_peg.x_loc + self.color_peg_size,
                                        k_peg.y_loc + self.color_peg_size, 
                                        fill=k_peg.state.value["color"],
                                        outline=k_peg.peg_outline_color)
    def click(self, event):
        print("Event : " + str(event))
        if(event.num == 1):
            # Left clicked, figure out if they are clicking on a circle
            for k_peg in self.key_color_pegs + self.guess_color_pegs:
                # print("k_peg : " + str(k_peg))
                if event.x < k_peg.x_loc + self.color_peg_size and \
                   event.x > k_peg.x_loc - self.color_peg_size and \
                   event.y < k_peg.y_loc + self.color_peg_size and \
                   event.y > k_peg.y_loc - self.color_peg_size:
                    print("FOUND PEG")
                    k_peg.cycle_states()

        elfif(event.num == 2):

        self.refresh_board()

    def save_settings(self):
        # TODO: Save settings here
        pass

    def load_settings(self):
        pass

    def on_closing(self):
        self.save_settings()
        self.window.destroy()

    def play_again(self):
        self.initialize_board()
        self.refresh_board()

    def mainloop(self):
        self.window.mainloop()

    

if __name__ == "__main__":
    mc = Mastermind_Class()
    mc.mainloop()