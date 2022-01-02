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

    curr_x_size = DEFAULT_X_SIZE
    curr_y_size = DEFAULT_Y_SIZE

    # Keeps track of how many pixels are between each col/row
    curr_x_step = 0
    curr_y_step = 0

    # This is the number of pixels between rows or columns, whichever is smaller. 
    # Pegs or Text can use to figure out what size they should be.
    smallest_step = 0

    key_y_loc = 0
    separator_line_y_loc = 0
    first_guess_y_loc = 0

    peg_x_loc_list = []

    score_pegs_x_loc = 0
    text_menu_x_loc = 0

    guess_peg_y_loc_list = []

    def set_sizes():
        GridCanvas.curr_x_step = GridCanvas.curr_x_size / GridCanvas.NUM_X_COLS
        GridCanvas.curr_y_step = GridCanvas.curr_y_size / GridCanvas.NUM_Y_ROWS

        GridCanvas.smallest_step = GridCanvas.curr_x_step
        if GridCanvas.curr_y_step < GridCanvas.smallest_step:
            GridCanvas.smallest_step = GridCanvas.curr_y_step

        GridCanvas.key_y_loc = GridCanvas.curr_y_step
        GridCanvas.separator_line_y_loc = GridCanvas.curr_y_step * 2
        GridCanvas.first_guess_y_loc = GridCanvas.curr_y_step * 3
        
        GridCanvas.peg_x_loc_list = [GridCanvas.curr_x_step,
                                     GridCanvas.curr_x_step * 2,
                                     GridCanvas.curr_x_step * 3,
                                     GridCanvas.curr_x_step * 4]

        GridCanvas.score_pegs_x_loc = GridCanvas.curr_x_step * 5
        GridCanvas.text_menu_x_loc = GridCanvas.curr_x_step * 6

        GridCanvas.guess_peg_y_loc_list = list(range(int(GridCanvas.first_guess_y_loc), 
                                                     int(GridCanvas.curr_y_step * 12), 
                                                     int(GridCanvas.curr_y_step)))

    def __init__(self,parent):
        Canvas.__init__(self,parent, width = GridCanvas.curr_x_size, height = GridCanvas.curr_y_size, highlightthickness = 0)
        self.bind("<Configure>", self.on_resize)
        self.height = self.winfo_reqheight()
        self.width = self.winfo_reqwidth()

    def __str__(self):
        out_str = ""
        out_str += "self.width  : " + str(self.width) + "\n"
        out_str += "self.height : " + str(self.height) + "\n"
        return out_str

    def on_resize(self,event):
        # determine the ratio of old width/height to new width/height
        wscale = float(event.width)/self.width
        hscale = float(event.height)/self.height
        self.width = event.width
        self.height = event.height
        # resize the canvas 
        self.config(width=self.width, height=self.height)
        # rescale all the objects tagged with the "all" tag
        self.scale("all",0,0,wscale,hscale)

