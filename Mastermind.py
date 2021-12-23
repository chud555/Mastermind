from tkinter import *
from enum import Enum
import collections, traceback, random
from ColorPeg import ColorPeg
from ScorePeg import ScorePeg
from TextObj import TextObj

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
        self.hide_key = False

        self.load_settings()
        self.key_color_pegs = []
        self.guess_color_pegs = []
        self.submit_guess_text = []
        self.text_values = []
        self.round_text = list(range(10, 0, -1))
        self.title_text = None
        
        self.window = Tk()
        self.window.title('Mastermind - Beta_0.1')
        self.canvas = Canvas(self.window, width=self.x_size_of_board, height=self.y_size_of_board)
        self.canvas.pack()
        self.window.minsize(self.x_min_size, self.y_min_size)
        self.window.maxsize(self.x_max_size, self.y_max_size)
        self.p_start_button = Button(self.window, text = "Start", command=self.player_start)

        self.window.bind("<Configure>", self.configure)
        self.window.bind('<Button-1>', self.click)
        self.window.bind('<Button-2>', self.click)
        self.window.bind('<Button-3>', self.click)
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
        self.submit_guess_text = []        
        
        # Build key location, the top row
        for x in self.x_loc_list:
            self.key_color_pegs.append(ColorPeg(x , self.key_y_loc))
            self.key_color_pegs[-1].is_clickable = True
        
        # Build guess rows
        for y in self.guess_y_loc_list:
            self.guess_color_pegs.append([])
            self.score_pegs.append(ScorePeg(0, y, 0))
            for x in self.x_loc_list:
                self.guess_color_pegs[-1].append(ColorPeg(x, y))
        
        self.text_values.append(TextObj(0, 0, "Random"))
        self.text_values.append(TextObj(0, 0, "Start"))
        self.title_text = TextObj(0, 0, "Round Number : N/A")

        for y in self.guess_y_loc_list:
            self.submit_guess_text.append(TextObj(0, 0, "X"))

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

        for y, guess_list, sub_text in zip(self.guess_y_loc_list, self.guess_color_pegs, self.submit_guess_text):
            sub_text.move_text(self.x_start_text, y)
            for x, k_peg in zip(self.x_loc_list, guess_list):
                k_peg.move_peg(x, y)

        for y, s_peg in zip(self.guess_y_loc_list, self.score_pegs):
            s_peg.move_peg(self.score_pegs_x_location, y)

        text_y = self.key_y_loc
        for text in self.text_values:
            text.move_text(self.x_start_text, text_y)
            text_y = text_y + self.y_size / 2.0
        
        self.title_text.move_text(self.x_size * 2, self.key_y_loc - 50)

        self.canvas.delete("all")

        # Put a line here before guess pegs
        self.canvas.create_line(self.x_size / 2.0, self.separator_line, 
                                self.x_size * 5, self.separator_line, fill="#777777", width=2)

        guess_color_pegs_flat = [item for items in self.guess_color_pegs for item in items]
        
        for k_peg in self.key_color_pegs:
            k_peg.set_peg_size(self.peg_size_ref)
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

        for guess_list, round_t, guess_text in zip(self.guess_color_pegs, self.round_text, self.submit_guess_text):
            if round_t == self.game_round:
                curr_color= "#20FD20"
            else:
                curr_color = "Black"
            if self.game_round != None:
                if round_t <= self.game_round:
                    self.canvas.create_text(self.x_size / 2, guess_list[0].y_loc, font=("Courier New", int(self.x_size / 5.0)), fill=curr_color, text=str(round_t))
                    self.canvas.create_text(guess_text.x_loc, guess_text.y_loc, font=("Courier New", int(self.x_size / 2.0)), fill=guess_text.color, text=str(guess_text.text))
            for k_peg in guess_list:
                k_peg.set_peg_size(self.peg_size_ref)                
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

        # Cover the key if specified
        if self.hide_key:
            self.canvas.create_rectangle((self.x_loc_list[0] - self.x_size / 4),
                                         (self.key_y_loc - self.y_size / 4),
                                         (self.x_loc_list[3] + self.x_size / 4),
                                         (self.key_y_loc + self.y_size / 4),
                                         fill="#D0D0D0")

        # Draw the text stuff now        
        for text in self.text_values:
            self.canvas.create_text(text.x_loc, text.y_loc, font=("Courier New", int(self.x_size / 5.0)), fill=text.color, text=text.text)

        # Create title text
        self.canvas.create_text(self.title_text.x_loc, self.title_text.y_loc, font=("Courier New", int(self.x_size / 5.0)), text=self.title_text.text)

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
        # print("Event : " + str(event))
        guess_color_pegs_flat = [item for items in self.guess_color_pegs for item in items]
        if(event.num == 1):
            # Left clicked, figure out if they are clicking on a circle
            for k_peg in self.key_color_pegs + guess_color_pegs_flat:
                if k_peg.clicked_on_peg(event.x, event.y):
                    k_peg.cycle_states()

            for text in self.text_values:
                if text.color == text.green:
                    self.start_game(text.text)

        elif(event.num == 3):
            # Left clicked, figure out if they are clicking on a circle
            for k_peg in self.key_color_pegs + guess_color_pegs_flat:
                if k_peg.clicked_on_peg(event.x, event.y):
                    k_peg.cycle_states(False)

        elif(event.delta == 120):
            for k_peg in self.key_color_pegs + guess_color_pegs_flat:
                if k_peg.clicked_on_peg(event.x, event.y):
                    k_peg.cycle_states()

        elif(event.delta == -120):
            for k_peg in self.key_color_pegs + guess_color_pegs_flat:
                if k_peg.clicked_on_peg(event.x, event.y):
                    k_peg.cycle_states(False)

        self.refresh_board()

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
        
        for text in self.submit_guess_text:
            if text.is_over_text(event.x, event.y):
                text.color = text.green
            else:
                text.color = text.black
        self.refresh_board()

    def set_game_round(self, curr_round):
        self.game_round = curr_round
        self.title_text.text = "Round Number : " + str(curr_round)

    def start_game(self, game_to_start):
        print("game_to_start : " + game_to_start)
        if game_to_start == "Random":
            self.key_color_pegs[0].state = random.choice(ColorPeg.state_list)
            self.key_color_pegs[1].state = random.choice(ColorPeg.state_list)
            self.key_color_pegs[2].state = random.choice(ColorPeg.state_list)
            self.key_color_pegs[3].state = random.choice(ColorPeg.state_list)
        elif game_to_start == "Start":
            # If any of the pegs aren't defined, define them, then start (single player game)
            if self.key_color_pegs[0].state == ColorPeg.States.EMPTY or \
               self.key_color_pegs[1].state == ColorPeg.States.EMPTY or \
               self.key_color_pegs[2].state == ColorPeg.States.EMPTY or \
               self.key_color_pegs[3].state == ColorPeg.States.EMPTY:
                self.key_color_pegs[0].state = random.choice(ColorPeg.state_list)
                self.key_color_pegs[1].state = random.choice(ColorPeg.state_list)
                self.key_color_pegs[2].state = random.choice(ColorPeg.state_list)
                self.key_color_pegs[3].state = random.choice(ColorPeg.state_list)

            self.hide_key = True
            self.game_state = GameStates.STANDARD_PLAY
            self.set_game_round(1)

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