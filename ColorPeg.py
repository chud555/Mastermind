import pygame, random
from enum import Enum

class ColorPeg():
    class States(Enum):
        EMPTY = {"color":"#808080"}        
        WHITE = {"color":"#FDFDFD"}
        BLACK = {"color":"#000000"}
        RED = {"color":"#FF2020"}
        GREEN = {"color":"#20FF20"}
        BLUE = {"color":"#2020FF"}
        YELLOW = {"color":"#FFFF20"}

    # This list defines state transition rules.
    state_list = [States.WHITE, 
                  States.BLACK, 
                  States.RED, 
                  States.GREEN, 
                  States.BLUE,  
                  States.YELLOW]

    def __init__(self, x_loc, y_loc, is_clickable = False):
        self.peg_outline_color = "#0F0F0F"
        self.state = ColorPeg.States.EMPTY
        self.x_loc = x_loc
        self.y_loc = y_loc
        self.is_clickable = is_clickable        
        self.size = 0
        self.empty_size = 0

    def clicked_on_peg(self, x_coord, y_coord):
        clicked_on = False
        if self.is_clickable and \
           x_coord < self.x_loc + self.size and \
           x_coord > self.x_loc - self.size and \
           y_coord < self.y_loc + self.size and \
           y_coord > self.y_loc - self.size:
            clicked_on = True
        return clicked_on

    def cycle_states(self, forward = True):
        self.click_sound()
        curr_list = ColorPeg.state_list        
        curr_ind = 0
        if self.state in curr_list:
            x = 0
            for state in curr_list:
                if self.state == state:
                    curr_ind = x
                x += 1
            if forward:
                curr_ind += 1
            else:
                curr_ind -= 1
        if curr_ind < len(curr_list):
            self.state = curr_list[curr_ind]
        elif curr_ind < 0:
            self.state = curr_list[-1]
        else:
            self.state = curr_list[0]

    def check_click(self, x_pos, y_pos, forward):
        if self.clicked_on_peg(x_pos, y_pos):            
            self.cycle_states(forward)
        
    def set_peg_size(self, p_size):        
        self.empty_size = (p_size/20.0) * 2
        self.size = (p_size/20.0) * 4

    def move_peg(self, x_pos, y_pos):
        self.x_loc = x_pos
        self.y_loc = y_pos

    def draw_peg(self, canvas, base_size):
        self.set_peg_size(base_size)
        if self.state == ColorPeg.States.EMPTY:
            curr_size = self.empty_size
        else:                
            curr_size = self.size
        canvas.create_oval(self.x_loc - curr_size, 
                           self.y_loc - curr_size, 
                           self.x_loc + curr_size,
                           self.y_loc + curr_size, 
                           fill=self.state.value["color"],
                           outline=self.peg_outline_color)

    def click_sound(self):
        click = pygame.mixer.Sound("sounds/click_1.mp3")
        pygame.mixer.Sound.play(click)

    def click_sound_2(self):
        click = pygame.mixer.Sound("sounds/click_2.mp3")
        pygame.mixer.Sound.play(click)

    def set_random(self):
        self.state = random.choice(ColorPeg.state_list)        

    def __str__(self):
        out_str = ""
        out_str += "state        : " + self.state.name + "\n"
        out_str += "x_loc        : " + str(self.x_loc) + "\n"
        out_str += "y_loc        : " + str(self.y_loc) + "\n"
        out_str += "is_clickable : " + str(self.is_clickable) + "\n"
        out_str += "size         : " + str(self.size) + "\n"
        out_str += "empty_size   : " + str(self.empty_size) + "\n"        
        return out_str