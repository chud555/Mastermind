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
        self.is_clickable = False        
        self.size = 0
        self.empty_size = 0       

    def cycle_states(self, reverse = False):
        curr_list = ColorPeg.state_list
        if reverse:
            curr_list = ColorPeg.state_list.reverse()
        curr_ind = 0
        # print("start - self.state : " + self.state.name)
        if self.state in ColorPeg.state_list:
            x = 0
            for state in ColorPeg.state_list:
                if self.state == state:
                    curr_ind = x
                x += 1
            curr_ind += 1
        # print("curr_ind : " + str(curr_ind))
        if curr_ind < len(ColorPeg.state_list):
            self.state = ColorPeg.state_list[curr_ind]
        else:
            self.state = ColorPeg.state_list[0]
        # print("end - self.state : " + self.state.name + " : " + str(curr_ind))

    def set_peg_size(self, p_size):        
        self.empty_size = (p_size/20.0) * 2
        self.size = (p_size/20.0) * 4

    def clicked_on_peg(self, x_coord, y_coord):
        clicked_on = False
        if x_coord < self.x_loc + self.size and \
           x_coord > self.x_loc - self.size and \
           y_coord < self.y_loc + self.size and \
           y_coord > self.y_loc - self.size and \
           self.is_clickable:            
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