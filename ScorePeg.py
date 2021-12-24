from enum import Enum

class ScorePeg():
    class States(Enum):
        EMPTY = {"color":"#808080"}
        WHITE = {"color":"#FDFDFD"}
        BLACK = {"color":"#000000"}

    def __init__(self, x_loc, y_loc, size_ref):
        self.peg_outline_color = "#0F0F0F"
        self.state_1 = ScorePeg.States.EMPTY
        self.state_2 = ScorePeg.States.EMPTY
        self.state_3 = ScorePeg.States.EMPTY
        self.state_4 = ScorePeg.States.EMPTY
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
        self.p1_y_loc = self.y_loc - (self.size_ref)

        self.p2_x_loc = self.x_loc + (self.size_ref)
        self.p2_y_loc = self.y_loc - (self.size_ref)

        self.p3_x_loc = self.x_loc - (self.size_ref)
        self.p3_y_loc = self.y_loc + (self.size_ref)

        self.p4_x_loc = self.x_loc + (self.size_ref)
        self.p4_y_loc = self.y_loc + (self.size_ref) 
    
    def move_peg(self, x_pos, y_pos):
        self.x_loc = x_pos
        self.y_loc = y_pos
        self.set_peg_locations(self.size_ref * 5.0)