from Globals import Globals
from GridCanvas import GridCanvas
from ColorPeg import ColorPeg

class KeyPegs():    
    peg_list = []
    hidden = False

    def init_pegs():
        KeyPegs.peg_list = []

        for ind in Globals.PEG_IND_LIST:
            KeyPegs.peg_list.append(ColorPeg(GridCanvas.peg_x_loc_list[ind], GridCanvas.key_y_loc))

    def move_pegs():
        for ind in Globals.PEG_IND_LIST:
            KeyPegs.peg_list[ind].move_peg(GridCanvas.peg_x_loc_list[ind], GridCanvas.key_y_loc)
