from tkinter import Canvas
from Globals import Globals

class GridCanvas(Canvas):
    
    # Constants
    WIN_X_MIN_SIZE = 200
    WIN_Y_MIN_SIZE = 400

    WIN_X_MAX_SIZE = 600
    WIN_Y_MAX_SIZE = 1200

    DEFAULT_X_SIZE = 400
    DEFAULT_Y_SIZE = 800

    # Split the board into a grid with 13 rows and 8 columns (never use 0 or max vals, so 7 and 12)
    # X should be based on the number of pegs, which is 4
    NUM_X_COLS = Globals.NUM_OF_PEGS + 4
    NUM_Y_ROWS = 13    

    def __init__(self, parent):
        self.parent = parent
        # TODO: This can be restored from previous sessions eventually        
        self.curr_x_size = GridCanvas.DEFAULT_X_SIZE
        self.curr_y_size = GridCanvas.DEFAULT_Y_SIZE
        Canvas.__init__(self, self.parent.frame, width = self.curr_x_size, height = self.curr_y_size, highlightthickness = 0)
        self.bind("<Configure>", self.on_resize)

        self.x_scale = 0
        self.y_scale = 0

        # Keeps track of how many pixels are between each col/row
        self.curr_x_step = 0
        self.curr_y_step = 0

        # This is the number of pixels between rows or columns, whichever is smaller. 
        # Pegs or Text can use to figure out what size they should be.
        self.smallest_step = 0

        self.key_y_loc = 0
        self.separator_line_y_loc = 0
        self.first_guess_y_loc = 0

        self.peg_x_loc_list = []

        self.score_pegs_x_loc = 0
        self.text_menu_x_loc = 0

        self.guess_peg_y_loc_list = []

    def on_resize(self,event):
        # determine the ratio of old width/height to new width/height
        self.x_scale = float(event.width)/self.curr_x_size
        self.y_scale = float(event.height)/self.curr_y_size
        self.curr_x_size = event.width
        self.curr_y_size = event.height
        # resize the canvas 
        self.config(width=self.curr_x_size, height=self.curr_y_size)
        # rescale all the objects tagged with the "all" tag
        self.scale("all",0,0,self.x_scale,self.y_scale)
        self.set_sizes()
        self.parent.refresh_board()

    def set_sizes(self):
        self.curr_x_step = self.curr_x_size / GridCanvas.NUM_X_COLS
        self.curr_y_step = self.curr_y_size / GridCanvas.NUM_Y_ROWS

        self.smallest_step = self.curr_x_step
        if self.curr_y_step < self.smallest_step:
            self.smallest_step = self.curr_y_step

        self.key_y_loc = self.curr_y_step
        self.separator_line_y_loc = self.curr_y_step * 2
        self.first_guess_y_loc = self.curr_y_step * 3
        
        self.peg_x_loc_list = [self.curr_x_step,
                               self.curr_x_step * 2,
                               self.curr_x_step * 3,
                               self.curr_x_step * 4]

        self.score_pegs_x_loc = self.curr_x_step * 5
        self.text_menu_x_loc = self.curr_x_step * 6

        self.guess_peg_y_loc_list = list(range(int(self.first_guess_y_loc), 
                                               int(self.curr_y_step * 12), 
                                               int(self.curr_y_step)))

        while len(self.guess_peg_y_loc_list) < 10:
            self.guess_peg_y_loc_list.append(int(self.guess_peg_y_loc_list[-1] + self.curr_y_step))

        self.guess_peg_y_loc_list.reverse()

    def __str__(self):
        out_str = ""
        out_str += "self.curr_x_size : " + str(self.curr_x_size) + "\n"
        out_str += "self.curr_y_size : " + str(self.curr_y_size) + "\n"
        out_str += "self.curr_x_step : " + str(self.curr_x_step) + "\n"
        out_str += "self.curr_y_step : " + str(self.curr_y_step) + "\n"
        out_str += "self.x_scale     : " + str(self.x_scale) + "\n"
        out_str += "self.y_scale     : " + str(self.y_scale) + "\n"
        return out_str
