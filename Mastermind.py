from tkinter import *
from enum import Enum
import collections, traceback, random

# References :
#
# Good starting tutorial with tutorial code:
# https://towardsdatascience.com/making-simple-games-in-python-f35f3ae6f31a - Aqeel Anwar (Dots and Boxes)
# https://github.com/aqeelanwar/Dots-and-Boxes
# 
# https://pythonguides.com/python-tkinter-events/

class GameStates(Enum):
    SETTING_CODE = 0
    COMPUTER_SETTING_CODE = 1
    SCORING = 2
    STANDARD_PLAY = 3

class ScorePeg():
    class States(Enum):
        EMPTY = {"color":"#808080"}
        WHITE = {"color":"#FDFDFD"}
        BLACK = {"color":"#FDFDFD"}

    def __init__(self, x_loc, y_loc, size_ref):
        self.peg_outline_color = "#0F0F0F"
        self.state = ScorePeg.States.EMPTY        
        self.x_loc = x_loc
        self.y_loc = y_loc
        self.set_peg_locations(size_ref)
        
        self.size = 0
        self.empty_size = 0       

    def set_peg_size(self, p_size):        
        self.set_peg_locations(p_size)
        self.empty_size = (p_size/20.0)
        self.size = (p_size/20.0) * 3

    def set_peg_locations(self, size_ref):
        self.size_ref = (size_ref / 5.0)
        self.p1_x_loc = self.x_loc - (self.size_ref)
        self.p1_y_loc = self.y_loc + (self.size_ref)
        self.p2_x_loc = self.x_loc + (self.size_ref)
        self.p2_y_loc = self.y_loc + (self.size_ref)
        self.p3_x_loc = self.x_loc - (self.size_ref)
        self.p3_y_loc = self.y_loc - (self.size_ref)
        self.p4_x_loc = self.x_loc + (self.size_ref)
        self.p4_y_loc = self.y_loc - (self.size_ref) 
    
    def move_peg(self, x_pos, y_pos):
        self.x_loc = x_pos
        self.y_loc = y_pos
        self.set_peg_locations(self.size_ref * 5.0)

class ColorPeg():
    class States(Enum):
        EMPTY = {"color":"#808080", "clickable":True, "size":None}        
        WHITE = {"color":"#FDFDFD", "clickable":True, "size":None}
        BLACK = {"color":"#000000", "clickable":True, "size":None}
        RED = {"color":"#FF2020", "clickable":True, "size":None}
        GREEN = {"color":"#20FF20", "clickable":True, "size":None}
        BLUE = {"color":"#2020FF", "clickable":True, "size":None}
        YELLOW = {"color":"#FFFF20", "clickable":True, "size":None}

    # This list defines state transition rules.
    state_list = [States.WHITE, 
                  States.BLACK, 
                  States.RED, 
                  States.GREEN, 
                  States.BLUE,  
                  States.YELLOW]

    def __init__(self, x_loc, y_loc):
        self.peg_outline_color = "#0F0F0F"
        self.state = ColorPeg.States.EMPTY
        self.x_loc = x_loc
        self.y_loc = y_loc
        self.isClickable = True
        self.isHidden = False
        self.size = 0
        self.empty_size = 0       

    def cycle_states(self, reverse = False):
        curr_list = ColorPeg.state_list
        if reverse:
            curr_list = ColorPeg.state_list.reverse()
        curr_ind = 0
        print("start - self.state : " + self.state.name)
        if self.state in ColorPeg.state_list:
            x = 0
            for state in ColorPeg.state_list:
                if self.state == state:
                    curr_ind = x
                x += 1
            curr_ind += 1
        print("curr_ind : " + str(curr_ind))
        if curr_ind < len(ColorPeg.state_list):
            self.state = ColorPeg.state_list[curr_ind]
        else:
            self.state = ColorPeg.state_list[0]
        print("end - self.state : " + self.state.name + " : " + str(curr_ind))

    def set_peg_size(self, p_size):        
        self.empty_size = (p_size/20.0) * 2
        self.size = (p_size/20.0) * 4

    def clicked_on_peg(self, x_coord, y_coord):
        clicked_on = False
        if x_coord < self.x_loc + self.size and \
           x_coord > self.x_loc - self.size and \
           y_coord < self.y_loc + self.size and \
           y_coord > self.y_loc - self.size and \
           self.isClickable:
            print("CLICKED PEG")
            clicked_on = True
        return clicked_on

    def move_peg(self, x_pos, y_pos):
        self.x_loc = x_pos
        self.y_loc = y_pos

    def __str__(self):
        out_str = ""
        out_str += "state : " + self.state.name + "\n"
        out_str += "x_loc : " + str(self.x_loc) + "\n"
        out_str += "y_loc : " + str(self.y_loc) + "\n"
        return out_str

class TextObj():
    def __init__(self, x_loc, y_loc, text_val):
        self.x_loc = x_loc
        self.y_loc = y_loc
        self.text = text_val
        self.x_loc_2 = self.x_loc + (len(text_val) * 20)
        self.y_loc_2 = self.y_loc + 20
        self.green = "#20FF20"
        self.black = "#000000"
        self.color = self.black
        
    def is_over_text(self, x_coord, y_coord):
        hovered_on = False
        """
        print("x_coord : " + str(x_coord))
        print("y_coord : " + str(y_coord))
        print("self.x_loc + (len(self.text) * 5) : " + str(self.x_loc + (len(self.text) * 5)))
        print("self.x_loc - (len(self.text) * 5) : " + str(self.x_loc - (len(self.text) * 5)))
        print("self.y_loc + 10: " + str(self.y_loc + 10))
        print("self.y_loc - 10 : " + str(self.y_loc - 10))
        """        
        
        if x_coord < self.x_loc + (len(self.text) * 5) and \
           x_coord > self.x_loc - (len(self.text) * 5) and \
           y_coord < self.y_loc + 10 and \
           y_coord > self.y_loc - 10:
            print("hovered over text : x_coord - " + str(x_coord) + " y_coord - " + str(y_coord))
            hovered_on = True
        return hovered_on

    def move_text(self, x_pos, y_pos):
        self.x_loc = x_pos
        self.y_loc = y_pos
        self.x_loc_2 = self.x_loc + (len(self.text) * 20)
        self.y_loc_2 = self.y_loc + 20

class Mastermind_Class():
    def __init__(self):
        self.game_state = GameStates.SETTING_CODE
        self.game_round = None
        self.resizing = False
        
        self.x_size_of_board = 400
        self.y_size_of_board = 800

        self.x_min_size = 200
        self.y_min_size = 400

        self.x_max_size = 600
        self.y_max_size = 1200

        self.load_settings()
        self.key_color_pegs = []
        self.guess_color_pegs = []
        
        self.window = Tk()
        self.window.title('Mastermind - Beta_0.1')
        self.canvas = Canvas(self.window, width=self.x_max_size, height=self.y_max_size)
        self.canvas.pack()
        self.window.minsize(self.x_min_size, self.y_min_size)
        self.window.maxsize(self.x_max_size, self.y_max_size)
        self.p_start_button = Button(self.window, text = "Player Start", command=self.player_start)

        self.window.bind("<Configure>", self.configure)
        self.window.bind('<Button-1>', self.click)
        self.window.bind('<Button-2>', self.click)
        self.window.bind('<MouseWheel>', self.click)
        self.window.bind('<Motion>', self.motion)

        self.set_sizes()
        self.initialize_board()
        self.play_again()

    def set_sizes(self):
        self.x_size = self.x_size_of_board / 8
        self.y_size = self.y_size_of_board / 13

        self.peg_size_ref = self.x_size
        if self.y_size < self.peg_size_ref:
            self.peg_size_ref = self.y_size

        self.key_y_loc = self.y_size
        self.separator_line = self.y_size * 2
        self.guess_y_first_loc = self.y_size * 3
        
        self.x_loc_list = [self.x_size, self.x_size * 2, self.x_size * 3, self.x_size * 4]

        self.score_pegs_x_location = self.x_size * 5
        self.x_start_text = self.x_size * 6

        self.guess_y_loc_list = list(range(int(self.guess_y_first_loc), int(self.y_size * 12), int(self.y_size)))

    def initialize_board(self):
        # Set all sizes used here, all based off the window sizes
        # 6 x columns, 12 y columns for now, base everything on that
        self.key_color_pegs = []
        self.guess_color_pegs = []
        self.score_pegs = []
        self.text_values = []
        
        # Build key location, the top row
        for x in self.x_loc_list:
            self.key_color_pegs.append(ColorPeg(x , self.key_y_loc))
        
        # Build guess rows
        for y in self.guess_y_loc_list:
            self.guess_color_pegs.append([])
            self.score_pegs.append(ScorePeg(0, y, 0))
            for x in self.x_loc_list:
                self.guess_color_pegs[-1].append(ColorPeg(x, y))
        
        self.text_values.append(TextObj(0, 0, "Comp Start"))
        self.text_values.append(TextObj(0, 0, "Man Start"))
        self.title_text = TextObj(0, 0, "Round Number : X")

    def refresh_board(self):
        self.set_sizes()
        
        """
        print("\n\nself.peg_size_ref : " + str(self.peg_size_ref))
        print("self.x_size : " + str(self.x_size))
        print("self.y_size : " + str(self.y_size))
        print("self.x_size_of_board : " + str(self.x_size_of_board))
        print("self.y_size_of_board : " + str(self.y_size_of_board))
        print("self.x_loc_list[0] : " + str(self.x_loc_list[0]))
        print("self.x_loc_list[1] : " + str(self.x_loc_list[1]))
        print("self.x_loc_list[2] : " + str(self.x_loc_list[2]))
        print("self.x_loc_list[3] : " + str(self.x_loc_list[3]))
        """
        
        for x, k_peg in zip(self.x_loc_list, self.key_color_pegs):
            k_peg.move_peg(x, self.key_y_loc)

        for y, guess_list in zip(self.guess_y_loc_list, self.guess_color_pegs):
            for x, k_peg in zip(self.x_loc_list, guess_list):
                k_peg.move_peg(x, y)

        for y, s_peg in zip(self.guess_y_loc_list, self.score_pegs):
            s_peg.move_peg(self.score_pegs_x_location, y)

        text_y = self.key_y_loc
        for text in self.text_values:
            text.move_text(self.x_start_text, text_y)
            text_y = text_y + self.y_size / 2.0

        self.title_text.move_text(self.x_size, self.key_y_loc - 50)

        self.canvas.delete("all")

        # Put a line here before guess pegs
        self.canvas.create_line(self.x_size / 2.0, self.separator_line, 
                                self.x_size * 5, self.separator_line, fill="#777777", width=2)

        guess_color_pegs_flat = [item for items in self.guess_color_pegs for item in items]
        
        for k_peg in self.key_color_pegs + guess_color_pegs_flat:
            k_peg.set_peg_size(self.peg_size_ref)
            if k_peg.state == ColorPeg.States.EMPTY:
                self.canvas.create_oval(k_peg.x_loc - k_peg.empty_size, 
                                        k_peg.y_loc - k_peg.empty_size, 
                                        k_peg.x_loc + k_peg.empty_size,
                                        k_peg.y_loc + k_peg.empty_size, 
                                        fill=k_peg.state.value["color"],
                                        outline=k_peg.peg_outline_color)
            else:
                print(k_peg)
                self.canvas.create_oval(k_peg.x_loc - k_peg.size, 
                                        k_peg.y_loc - k_peg.size, 
                                        k_peg.x_loc + k_peg.size,
                                        k_peg.y_loc + k_peg.size, 
                                        fill=k_peg.state.value["color"],
                                        outline=k_peg.peg_outline_color)

        # Draw the text stuff now        
        for text in self.text_values:
            self.canvas.create_text(text.x_loc, text.y_loc, font=16, fill=text.color, text=text.text)

        self.canvas.create_text(self.title_text.x_loc, self.title_text.y_loc, font = 18, text=self.title_text.text)

        for k_peg in self.score_pegs:
            k_peg.set_peg_size(self.peg_size_ref)
            if k_peg.state == ScorePeg.States.EMPTY:
                self.canvas.create_oval(k_peg.p1_x_loc - k_peg.empty_size, 
                                        k_peg.p1_y_loc - k_peg.empty_size, 
                                        k_peg.p1_x_loc + k_peg.empty_size,
                                        k_peg.p1_y_loc + k_peg.empty_size, 
                                        fill=k_peg.state.value["color"],
                                        outline=k_peg.peg_outline_color)
                self.canvas.create_oval(k_peg.p2_x_loc - k_peg.empty_size, 
                                        k_peg.p2_y_loc - k_peg.empty_size, 
                                        k_peg.p2_x_loc + k_peg.empty_size,
                                        k_peg.p2_y_loc + k_peg.empty_size, 
                                        fill=k_peg.state.value["color"],
                                        outline=k_peg.peg_outline_color)
                self.canvas.create_oval(k_peg.p3_x_loc - k_peg.empty_size, 
                                        k_peg.p3_y_loc - k_peg.empty_size, 
                                        k_peg.p3_x_loc + k_peg.empty_size,
                                        k_peg.p3_y_loc + k_peg.empty_size, 
                                        fill=k_peg.state.value["color"],
                                        outline=k_peg.peg_outline_color)
                self.canvas.create_oval(k_peg.p4_x_loc - k_peg.empty_size, 
                                        k_peg.p4_y_loc - k_peg.empty_size, 
                                        k_peg.p4_x_loc + k_peg.empty_size,
                                        k_peg.p4_y_loc + k_peg.empty_size, 
                                        fill=k_peg.state.value["color"],
                                        outline=k_peg.peg_outline_color)
            else:
                print(k_peg)
                self.canvas.create_oval(k_peg.p1_x_loc - k_peg.size, 
                                        k_peg.p1_y_loc - k_peg.size, 
                                        k_peg.p1_x_loc + k_peg.size,
                                        k_peg.p1_y_loc + k_peg.size, 
                                        fill=k_peg.state.value["color"],
                                        outline=k_peg.peg_outline_color)
                self.canvas.create_oval(k_peg.p2_x_loc - k_peg.size, 
                                        k_peg.p2_y_loc - k_peg.size, 
                                        k_peg.p2_x_loc + k_peg.size,
                                        k_peg.p2_y_loc + k_peg.size, 
                                        fill=k_peg.state.value["color"],
                                        outline=k_peg.peg_outline_color)
                self.canvas.create_oval(k_peg.p3_x_loc - k_peg.size, 
                                        k_peg.p3_y_loc - k_peg.size, 
                                        k_peg.p3_x_loc + k_peg.size,
                                        k_peg.p3_y_loc + k_peg.size, 
                                        fill=k_peg.state.value["color"],
                                        outline=k_peg.peg_outline_color)
                self.canvas.create_oval(k_peg.p4_x_loc - k_peg.size, 
                                        k_peg.p4_y_loc - k_peg.size, 
                                        k_peg.p4_x_loc + k_peg.size,
                                        k_peg.p4_y_loc + k_peg.size, 
                                        fill=k_peg.state.value["color"],
                                        outline=k_peg.peg_outline_color)
        
    def click(self, event):
        print("Event : " + str(event))
        guess_color_pegs_flat = [item for items in self.guess_color_pegs for item in items]
        if(event.num == 1):
            # Left clicked, figure out if they are clicking on a circle
            for k_peg in self.key_color_pegs + guess_color_pegs_flat:
                if k_peg.clicked_on_peg(event.x, event.y):
                    k_peg.cycle_states()

            for text in self.text_values:
                if text.color == text.green:
                    self.start_game(text.text)

        elif(event.num == 2):
            # Left clicked, figure out if they are clicking on a circle
            for k_peg in self.key_color_pegs + guess_color_pegs_flat:
                if k_peg.clicked_on_peg(event.x, event.y):
                    k_peg.cycle_states(False)

        self.refresh_board()

    def ignore(self, event):
        print("ignore")
        return "break"

    def configure(self, event):
        """
        print("configure event : " + str(event))        
        traceback.print_stack()
        """
        if not self.resizing and not (event.width == 404 and event.height == 804):
            print("in resizing")
            print("event.width : " + str(event.width))
            print("event.height : " + str(event.height))
            
            self.resizing = True   
            self.x_size_of_board = event.width
            self.y_size_of_board = event.height
            self.refresh_board()
            self.resizing = False

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
        self.refresh_board()

    def start_game(self, game_to_start):
        print("game_to_start : " + game_to_start)
        if game_to_start == "Comp Start":
            self.key_color_pegs[0].state = random.choice(ColorPeg.state_list)
            self.key_color_pegs[1].state = random.choice(ColorPeg.state_list)
            self.key_color_pegs[2].state = random.choice(ColorPeg.state_list)
            self.key_color_pegs[3].state = random.choice(ColorPeg.state_list)
        elif game_to_start == "Man Start":
            # Get this to work, it requires a bit more for game mode stuff 
            pass

        self.game_state = GameStates.STANDARD_PLAY
        self.game_round = 1

    def save_settings(self):
        # TODO: Save settings here
        pass

    def load_settings(self):
        pass

    def on_closing(self):
        self.save_settings()
        self.window.destroy()

    def play_again(self):        
        self.refresh_board()

    def player_start(self):
        for peg in self.key_color_pegs:
            peg.isClickable = True

if __name__ == "__main__":
    mc = Mastermind_Class()
    mc.window.mainloop()